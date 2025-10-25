import os

import numpy as np
import pandas as pd
import tensorflow as tf
from PIL import Image
from matplotlib import pyplot as plt
from sklearn.model_selection import train_test_split

CLASS_NUM = 4


def load_data(poi_type):
    root_dir = '1_res/2D/city/' + poi_type
    class_dirs = os.listdir(root_dir)
    m_labels = []
    m_images = []
    for class_dir in class_dirs:
        for img_file in os.listdir(os.path.join(root_dir, class_dir)):
            m_labels.append(int(class_dir))
            im = Image.open(root_dir + '/' + class_dir + '/' + img_file)
            # im = im.convert('L')
            # print(im.format, im.size, im.mode)
            im = np.array(im)
            print(im.shape)
            m_images.append(im)
    return np.array(m_images), np.array(m_labels)


def split_data(poi_type):
    m_images, m_labels = load_data(poi_type)
    x_train, x_test, y_train, y_test = train_test_split(m_images, m_labels, test_size=0.2, random_state=42)
    return x_train, x_test, y_train, y_test


def get_model():
    input_xs = tf.keras.Input([38, 38, 4])
    conv = tf.keras.layers.Conv2D(32, 3, padding='SAME', activation=tf.nn.relu)(input_xs)
    conv = tf.keras.layers.BatchNormalization()(conv)
    conv = tf.keras.layers.Conv2D(64, 3, padding='SAME', activation=tf.nn.relu)(conv)
    conv = tf.keras.layers.MaxPooling2D(strides=[1, 1])(conv)
    conv = tf.keras.layers.Conv2D(128, 3, padding='SAME', activation=tf.nn.relu)(conv)
    flat = tf.keras.layers.Flatten()(conv)
    dense = tf.keras.layers.Dense(512, activation=tf.nn.relu)(flat)
    logits = tf.keras.layers.Dense(CLASS_NUM, activation=tf.nn.softmax)(dense)
    model = tf.keras.Model(input_xs, logits)
    return model


def plot_history(history):
    hist = pd.DataFrame(history.history)
    hist['epoch'] = history.epoch
    # print(hist.columns)
    # print(list(hist))
    plt.figure()
    plt.xlabel('Epoch')
    # plt.ylabel('accuracy')
    plt.plot(hist['epoch'], hist['accuracy'],
             label='accuracy')
    plt.plot(hist['epoch'], hist['loss'],
             label='loss')
    plt.ylim([0, 1])
    plt.legend()
    plt.show()


def run():
    np.set_printoptions(threshold=np.inf)
    m_poi_type = ['food', 'hotel', 'shopping', 'life_service', 'beauty', 'view', 'entertainment', 'sport', 'edu',
                  'culture', 'medical', 'car_service', 'traffic', 'finance', 'estate', 'company', 'government',
                  'entrance', 'nature']
    print(m_poi_type)
    m_poi = input('please input poi type:')
    train_x, test_x, train_y, test_y = split_data(m_poi)
    train_y = np.array(tf.keras.utils.to_categorical(train_y, num_classes=CLASS_NUM))
    test_y = np.array(tf.keras.utils.to_categorical(test_y, num_classes=CLASS_NUM))

    batch_size = 16
    train_dataset = tf.data.Dataset.from_tensor_slices((train_x, train_y)).batch(batch_size).shuffle(batch_size)
    train_dataset = train_dataset.repeat(10)
    test_dataset = tf.data.Dataset.from_tensor_slices((test_x, test_y)).batch(batch_size).shuffle(batch_size)

    model = get_model()
    model.compile(tf.optimizers.Adam(1e-3), tf.losses.categorical_crossentropy, ['accuracy'])
    m_history = model.fit(train_dataset, epochs=4)
    plot_history(m_history)
    model.save('tf_models/m_model.h5')
    score = model.evaluate(test_dataset)
    print(model.summary())
    print('last score:', score)


if __name__ == '__main__':
    run()
