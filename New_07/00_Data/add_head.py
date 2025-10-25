import pandas as pd

import os

m_dir = 'without_head/'
files = os.listdir(m_dir)
for file in files:
    if not os.path.exists('with_head/' + file):
        print(file)
        m_data = pd.read_csv(m_dir + file,
                             names=['food', 'edu', 'sport', 'nature', 'shopping', 'car_service', 'beauty', 'culture',
                                    'entrance',
                                    'life_service', 'entertainment', 'company', 'finance', 'view', 'hotel', 'estate',
                                    'traffic',
                                    'government',
                                    'medical'])
        m_data.to_csv('with_head/' + file, index=False)
