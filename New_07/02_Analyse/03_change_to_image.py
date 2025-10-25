import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

np.random.seed(0)


def analyse_data(m_dir, city, m_col_num, m_col_name):
    csv_path = m_dir + city + '.CSV'
    m_data = pd.read_csv(csv_path)

    m_row_num = int(len(m_data) / m_col_num)
    m_arr = np.array(m_data[m_col_name]).reshape(m_row_num, m_col_num)
    plt.title(city, fontsize=14)
    plt.imshow(m_arr / 255)
    # plt.imshow(m_arr % 255, cmap='gray', vmin=0, vmax=255)
    # plt.imshow(m_arr, cmap='gray')
    # plt.imshow(m_arr)
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


if __name__ == '__main__':
    run()
