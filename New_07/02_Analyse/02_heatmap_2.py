import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import os

np.random.seed(0)


def analyse_data(m_dir, m_col_num, m_col_name):
    m_pd = pd.read_csv('../00_Data/info/city.CSV')
    plt.figure(figsize=(12, 12))
    for m_index in range(0, len(m_pd)):
        city = m_pd.iloc[m_index, 0]
        csv_path = m_dir + city + '.CSV'
        m_data = pd.read_csv(csv_path)
        # 热力图========================================
        ax = plt.subplot(5, 5, m_index + 1)
        m_row_num = int(len(m_data) / m_col_num)
        m_arr = np.array(m_data[m_col_name]).reshape(m_row_num, m_col_num)
        plt.title(city)
        # sns.heatmap(m_arr, cmap='YlGnBu', linewidths=1, cbar=True, xticklabels=False, yticklabels=False,
        #             square=True, ax=ax)
        sns.heatmap(m_arr, cmap='hot_r', linewidths=1, cbar=True, xticklabels=False, yticklabels=False,
                    square=True, ax=ax)
    plt.savefig('heatmap/' + m_col_name + '.png', transparent=False, dpi=800, bbox_inches="tight")
    plt.show()


def run():
    m_dir = '../00_Data/with_head/'
    print('all col names:',
          ['food', 'edu', 'sport', 'nature', 'shopping', 'car_service', 'beauty', 'culture', 'entrance',
           'life_service', 'entertainment', 'company', 'finance', 'view', 'hotel', 'estate', 'traffic',
           'government',
           'medical'])
    m_col_name = input('please input col name to draw heatmap:')
    analyse_data(m_dir, 30, m_col_name)


def run2():
    m_dir = '../00_Data/with_head/'
    m_list = ['food', 'edu', 'sport', 'nature', 'shopping', 'car_service', 'beauty', 'culture', 'entrance',
              'life_service', 'entertainment', 'company', 'finance', 'view', 'hotel', 'estate', 'traffic',
              'government',
              'medical']
    for m_col_name in m_list:
        print(m_col_name)
        analyse_data(m_dir, 30, m_col_name)


if __name__ == '__main__':
    run2()
