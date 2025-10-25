import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import os

np.random.seed(0)


# def analyse_data_2(m_dir, city, m_col_num, m_col_name):
#     csv_path = m_dir + city + '.CSV'
#     m_data = pd.read_csv(csv_path)
#
#     # 热力图========================================
#     m_row_num = int(len(m_data) / m_col_num)
#     m_arr = np.array(m_data[m_col_name]).reshape(m_row_num, m_col_num)
#     plt.title(city, fontsize=14)
#     fig = sns.heatmap(m_arr, cmap='YlGnBu', linewidths=1, cbar=True, xticklabels=False, yticklabels=False, square=True)
#     m_fig = fig.get_figure()
#     if not os.path.exists('heatmap/' + m_col_name + '/'):
#         os.mkdir('heatmap/' + m_col_name + '/')
#     # m_fig.savefig('heatmap/' + m_col_name + '/' + city + '.png')
#     # Uncomment this line to save the figure.
#     m_fig.savefig('heatmap/' + m_col_name + '/' + city + '.png', transparent=False, dpi=800, bbox_inches="tight")
#     plt.show()


def analyse_data(m_dir, city, m_col_num, m_col_name):
    csv_path = m_dir + city + '.CSV'
    m_data = pd.read_csv(csv_path)

    # 热力图========================================
    m_row_num = int(len(m_data) / m_col_num)
    m_arr = np.array(m_data[m_col_name]).reshape(m_row_num, m_col_num)
    plt.title(city, fontsize=14)
    fig = sns.heatmap(m_arr, cmap='YlGnBu', linewidths=1, cbar=True, xticklabels=False, yticklabels=False, square=True)
    # fig = sns.heatmap(m_arr, cmap='hot_r', linewidths=1, cbar=True, xticklabels=False, yticklabels=False, square=True)
    m_fig = fig.get_figure()
    if not os.path.exists('heatmap/' + m_col_name + '/'):
        os.mkdir('heatmap/' + m_col_name + '/')
    # m_fig.savefig('heatmap/' + m_col_name + '/' + city + '.png')
    # Uncomment this line to save the figure.
    # plt.xlabel(fontdict={'family': 'Times New Roman', 'size': '14'})
    # plt.ylabel(fontdict={'family': 'Times New Roman', 'size': '14'})
    # plt.xticks(fontproperties='Times New Roman', size='14')
    # plt.yticks(fontproperties='Times New Roman', size='14')
    plt.title(city, fontdict={'family': 'Times New Roman', 'size': '14'})
    # plt.legend(prop={'family': 'Times New Roman', 'size': '14'})
    m_fig.savefig('heatmap/' + m_col_name + '/' + city + '.svg', transparent=False, dpi=800, bbox_inches="tight")
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
        analyse_data(m_dir, m_pd.iloc[m_index, 0], 30, m_col_name)


def run2():
    m_dir = '../00_Data/with_head/'
    m_pd = pd.read_csv('../00_Data/info/city.CSV')
    m_list = ['food', 'edu', 'sport', 'nature', 'shopping', 'car_service', 'beauty', 'culture', 'entrance',
              'life_service', 'entertainment', 'company', 'finance', 'view', 'hotel', 'estate', 'traffic',
              'government',
              'medical']
    for m_index in range(0, len(m_pd)):
        print(m_pd.iloc[m_index, 0])
        for m_col_name in m_list:
            analyse_data(m_dir, m_pd.iloc[m_index, 0], 30, m_col_name)


if __name__ == '__main__':
    run()
