import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pandas.plotting import scatter_matrix

np.random.seed(0)


def analyse_data(m_dir, city):
    csv_path = m_dir + city + '.CSV'
    m_data = pd.read_csv(csv_path)
    # print(m_data.head())
    # print(m_data.columns)
    # print(list(m_data))
    # print(m_data.info())
    # print(m_data['food'].value_counts())
    print(m_data.describe())
    # m_data.hist(bins=50, figsize=(20, 15))
    # m_grids_num = len(m_data)
    m_data.hist(bins=50, figsize=(20, 15))

    # 寻找数据相关性
    # m_data['food_shopping'] = m_data['food'] + m_data['shopping']
    # m_data['food_shopping_lifeService'] = m_data['food'] + m_data['shopping'] + m_data['life_service']
    m_corr_matrix = m_data.corr()
    # m_corr_matrix.to_csv('corr/' + city + '.CSV')

    m_food_corr = m_corr_matrix['food'].sort_values(ascending=False)
    print(m_food_corr)
    # m_food_corr.to_csv('corr/food/' + city + '.CSV')
    m_shopping_corr = m_corr_matrix['shopping'].sort_values(ascending=False)

    # print(m_corr_matrix['life_service'].sort_values(ascending=False).head(4))

    # print(m_corr_matrix['food_shopping'].sort_values(ascending=False))
    # print(m_corr_matrix['food_shopping_lifeService'].sort_values(ascending=False))
    # print(m_corr_matrix['estate'].sort_values(ascending=False))
    # print(m_corr_matrix['company'].sort_values(ascending=False))

    # m_data.plot(kind='scatter', x='food', y='shopping')
    # plt.show()
    m_attr = ['food', 'shopping', 'life_service', 'traffic']
    scatter_matrix(m_data[m_attr], figsize=(12, 8))
    # plt.xlabel(fontdict={'family': 'Times New Roman', 'size': '14'})
    # plt.ylabel(fontdict={'family': 'Times New Roman', 'size': '14'})
    # plt.xticks(fontproperties='Times New Roman', size='14')
    # plt.yticks(fontproperties='Times New Roman', size='14')
    # plt.title(city, fontdict={'family': 'Times New Roman', 'size': '14'})

    plt.savefig('X/svg/' + city + '.svg', transparent=False, dpi=800, bbox_inches="tight")
    # plt.show()


def run():
    m_dir = '../00_Data/with_head/'
    m_pd = pd.read_csv('../00_Data/info/city.CSV')
    print('all col names:',
          ['food', 'edu', 'sport', 'nature', 'shopping', 'car_service', 'beauty', 'culture', 'entrance',
           'life_service', 'entertainment', 'company', 'finance', 'view', 'hotel', 'estate', 'traffic',
           'government',
           'medical'])
    for m_index in range(0, len(m_pd)):
        print(m_pd.iloc[m_index, 0] + '-------------------------------------------------')
        analyse_data(m_dir, m_pd.iloc[m_index, 0])
    # city = input('please input city name:')
    # analyse_data(m_dir, city)


if __name__ == '__main__':
    run()
