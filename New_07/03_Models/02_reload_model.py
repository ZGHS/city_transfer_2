import os

import numpy as np
import tensorflow as tf
from PIL import Image


def load_data(poi_type):
    root_dir = '1_res/2D/city/' + poi_type
    class_dirs = os.listdir(root_dir)
    m_labels = []
    m_images = []
    for class_dir in class_dirs:
        for img_file in os.listdir(os.path.join(root_dir, class_dir)):
            m_labels.append(int(class_dir))
            im = Image.open(root_dir + '/' + class_dir + '/' + img_file)
            im = np.array(im)
            m_images.append(im)
    return np.array(m_images), np.array(m_labels)


def run():
    loaded_model = tf.keras.models.load_model('./tf_models/m_model.h5')

    m_poi_type = ['food', 'hotel', 'shopping', 'life_service', 'beauty', 'view', 'entertainment', 'sport', 'edu',
                  'culture', 'medical', 'car_service', 'traffic', 'finance', 'estate', 'company', 'government',
                  'entrance', 'nature']
    print(m_poi_type)
    m_poi = input('please input poi type:')
    m_images, m_labels = load_data(m_poi)
    for i in range(0, len(m_images)):
        m_image = m_images[i]
        m_image = tf.expand_dims(m_image, 0)
        m_res = loaded_model.predict(m_image)
        m_res = np.argmax(m_res)
        print(m_res == m_labels[i])


if __name__ == '__main__':
    run()
