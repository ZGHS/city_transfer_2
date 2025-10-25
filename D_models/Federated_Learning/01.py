import collections
import os

import nest_asyncio
import numpy as np
import pandas as pd
import tensorflow as tf
import tensorflow_federated as tff
from tensorflow.keras.layers import Attention
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from tensorflow_model_optimization.python.core.internal import tensor_encoding as te
import gc

nest_asyncio.apply()

# 对X01_Data中的60个城市进行联邦学习
M_DIR = '../Data/final_data/z/'

# 训练轮数（210效果最佳）
NUM_ROUNDS = 210


def split_data():
    m_dir = M_DIR + 'x/'
    files = os.listdir(m_dir)
    train_data = []
    test_data = []
    for file in files:
        m_temp = pd.read_csv(m_dir + file).to_numpy()
        m_x = m_temp[:, :18]
        m_y = m_temp[:, -1]
        x_train, x_test, y_train, y_test = train_test_split(m_x, m_y, test_size=0.3, random_state=42)
        train_data.append([{
            'x':
                x_train,
            'y':
                y_train
        }])
        test_data.append([{
            'x':
                x_test,
            'y':
                y_test
        }])
    return train_data, test_data


train_data, test_data = split_data()

# # federated_train_data 中有 10 个小列表，代表标签为 0, 1, 2, ..., 9 的样本数据集
# # 每个小列表中有 10 个集合，键值分别为 'x' 和 'y'，每个集合中都包含 100 个样本


BATCH_SPEC = collections.OrderedDict(
    x=tf.TensorSpec(shape=[None, 18], dtype=tf.float32),
    y=tf.TensorSpec(shape=[None], dtype=tf.int32))
BATCH_TYPE = tff.to_type(BATCH_SPEC)


# def create_keras_model():
#     return tf.keras.models.Sequential([
#         tf.keras.layers.Dense(18, activation=tf.nn.relu, input_shape=(18,)),  # 需要给出输入的形式
#         tf.keras.layers.Dense(13, activation=tf.nn.relu),
#         tf.keras.layers.Dense(13, activation=tf.nn.relu),
#         tf.keras.layers.Dense(13, activation=tf.nn.relu),
#         tf.keras.layers.Dense(3)
#         # tf.keras.layers.Softmax()
#     ])

def create_keras_model():
    return tf.keras.models.Sequential([
        tf.keras.layers.Dense(18, activation=tf.nn.relu, input_shape=(18,)),  # 需要给出输入的形式
        tf.keras.layers.Dense(10, kernel_initializer='zeros'),
        Attention(10, 1),
        tf.keras.layers.Softmax(),
    ])


def model_fn():
    keras_model = create_keras_model()
    return tff.learning.from_keras_model(
        keras_model,
        input_spec=BATCH_TYPE,
        loss=tf.keras.losses.SparseCategoricalCrossentropy(),
        metrics=[tf.keras.metrics.SparseCategoricalAccuracy()])


# 服务端向客户端广播模型参数时，应用的压缩函数
# value表示针对模型参数中的每个值进行处理
def broadcast_encoder_fn(value):
    """Function for building encoded broadcast."""
    spec = tf.TensorSpec(value.shape, value.dtype)
    if value.shape.num_elements() > 10000:
        # 均匀量化压缩
        return te.encoders.as_simple_encoder(
            te.encoders.uniform_quantization(bits=8), spec)
    else:
        # 应用恒等式
        return te.encoders.as_simple_encoder(te.encoders.identity(), spec)


# 广播压缩处理函数
encoded_broadcast_process = (
    tff.learning.framework.build_encoded_broadcast_process_from_model(
        model_fn, broadcast_encoder_fn))


# 客户端向服务端上传模型参数时，使用的压缩函数
def mean_encoder_fn(value):
    """Function for building encoded mean."""
    spec = tf.TensorSpec(value.shape, value.dtype)
    if value.shape.num_elements() > 10000:
        return te.encoders.as_gather_encoder(
            te.encoders.uniform_quantization(bits=8), spec)
    else:
        return te.encoders.as_gather_encoder(te.encoders.identity(), spec)


# 聚合压缩处理函数
encoded_mean_process = (
    tff.learning.framework.build_encoded_mean_process_from_model(
        model_fn, mean_encoder_fn))

# 创建联邦平均聚合算法
trainer = tff.learning.build_federated_averaging_process(
    model_fn,
    client_optimizer_fn=lambda: tf.keras.optimizers.SGD(learning_rate=0.02),
    server_optimizer_fn=lambda: tf.keras.optimizers.SGD(learning_rate=1.0),
    broadcast_process=encoded_broadcast_process,
    aggregation_process=encoded_mean_process)

# 联邦平均算法初始化
state = trainer.initialize()

logdir_for_compression = "./logs/"
summary_writer = tf.summary.create_file_writer(logdir_for_compression)
with summary_writer.as_default():
    # 基础训练测试
    for i in range(NUM_ROUNDS + 1):
        state, metrics = trainer.next(state, train_data)
        test_state, test_metrics = trainer.next(state, test_data)

        print('第', i, '轮训练')
        print('train_data 模型loss：', metrics['train']['loss'], '准确率：', metrics['train']['sparse_categorical_accuracy'])
        tf.summary.scalar('train_loss', metrics['train']['loss'], step=i)
        tf.summary.scalar('train_acc', metrics['train']['sparse_categorical_accuracy'], step=i)

        print('test_data  模型loss：', test_metrics['train']['loss'], '准确率：',
              test_metrics['train']['sparse_categorical_accuracy'],
              '\n')
        tf.summary.scalar('test_loss', test_metrics['train']['loss'], step=i)
        tf.summary.scalar('test_acc', test_metrics['train']['sparse_categorical_accuracy'], step=i)

        summary_writer.flush()

evaluation = tff.learning.build_federated_evaluation(model_fn)

train_metrics = evaluation(state.model, train_data)
print('train_metrics:' + str(train_metrics))

test_metrics = evaluation(state.model, test_data)
print('test_metrics:' + str(test_metrics))

gc.collect()
