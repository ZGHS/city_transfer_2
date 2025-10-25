import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os
from mpl_toolkits.mplot3d import Axes3D

def draw_3d(m_dir, city, m_col_num, m_col_name):
    csv_path = m_dir + city + '.CSV'
    m_data = pd.read_csv(csv_path)

    m_arr = np.array(m_data[m_col_name])
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    xpos = []
    ypos = []
    for i in range(0, m_col_num):
        xpos += [i for x in range(0, m_col_num)]
        ypos += [x for x in range(0, m_col_num)]
    ax.set_title(city)
    ax.bar3d(xpos, ypos, 0, 1, 1, m_arr, zsort='average')
    if not os.path.exists('3d_bar/' + m_col_name + '/'):
        os.mkdir('3d_bar/' + m_col_name + '/')
    # plt.savefig('3d_bar/' + m_col_name + '/' + city + '.png')
    plt.savefig('3d_bar/' + m_col_name + '/' + city + '.png', transparent=False, dpi=800, bbox_inches="tight")
    plt.show()


def run():
    m_dir = '../00_Data/with_head/'
    m_pd = pd.read_csv('../00_Data/info/city.CSV')
    print('all col names:',
          ['food', 'edu', 'sport', 'nature', 'shopping', 'car_service', 'beauty', 'culture', 'entrance',
           'life_service', 'entertainment', 'company', 'finance', 'view', 'hotel', 'estate', 'traffic',
           'government',
           'medical'])
    m_col_name = input('please input col name to draw heatmap:')
    for m_index in range(0, len(m_pd)):
        print(m_pd.iloc[m_index, 0])
        draw_3d(m_dir, m_pd.iloc[m_index, 0], 30, m_col_name)


def run2():
    m_dir = '../00_Data/with_head/'
    m_pd = pd.read_csv('../00_Data/info/city.CSV')
    m_list = ['food', 'edu', 'sport', 'nature', 'shopping', 'car_service', 'beauty', 'culture', 'entrance',
              'life_service', 'entertainment', 'company', 'finance', 'view', 'hotel', 'estate', 'traffic',
              'government',
              'medical']

    for m_index in range(0, len(m_pd)):
        print(m_pd.iloc[m_index, 0])
        for cluster_condition in m_list:
            draw_3d(m_dir, m_pd.iloc[m_index, 0], 30, cluster_condition)


if __name__ == '__main__':
    run()
