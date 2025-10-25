import numpy as np
import pandas as pd
import os

file_names = os.listdir('./')
m_pd = pd.DataFrame()
for file_name in file_names:
    m_name = os.path.splitext(file_name)[0]
    m_type = os.path.splitext(file_name)[1]
    if m_type == '.CSV':
        m_data = np.loadtxt(file_name, delimiter=',', dtype='str')
        # m_data[1, 0] = m_name
        m_pd[m_name] = m_data[1:, 0]
    m_pd.to_csv('A_food.CSV', index=False)
