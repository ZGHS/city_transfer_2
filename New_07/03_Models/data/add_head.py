import pandas as pd

import os

source_root = 'without_head/'
dirs = os.listdir(source_root)

for dir in dirs:
    m_files = os.listdir(source_root + dir + '/')
    for file in m_files:
        if not os.path.exists('with_head/' + dir + '/'):
            os.mkdir('with_head/' + dir + '/')

        if not os.path.exists('with_head/' + dir + '/' + file):
            print(file)
            m_data = pd.read_csv(source_root + dir + '/' + file,
                                 names=['food', 'edu', 'sport', 'nature', 'shopping', 'car_service', 'beauty',
                                        'culture',
                                        'entrance',
                                        'life_service', 'entertainment', 'company', 'finance', 'view', 'hotel',
                                        'estate',
                                        'traffic',
                                        'government',
                                        'medical'])
            m_data.to_csv('with_head/' + dir + '/' + file, index=False)
