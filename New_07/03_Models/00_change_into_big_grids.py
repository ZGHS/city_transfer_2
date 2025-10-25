import math
import os

import numpy as np
import pandas as pd

np.random.seed(0)


def change_data(m_dir, city, grids_num, side_length):
    m_target_dir = 'data/without_head/N_' + str(side_length) + '/'
    if not os.path.exists(m_target_dir):
        os.mkdir(m_target_dir)

    csv_path = m_dir + city + '.CSV'
    m_data = pd.read_csv(csv_path)
    m_data = m_data.to_numpy()
    m_res = []
    for i in range(0, grids_num - ((side_length - 1) * int(math.sqrt(grids_num)) + side_length - 1),
                   int(math.sqrt(grids_num) * side_length)):
        # print(i)
        for j in range(i, i + int(math.sqrt(grids_num) / side_length - 1) * side_length + 1, side_length):
            # print(j)
            for xx in range(0, side_length):
                for yy in range(0, side_length):
                    m_index = j + yy + xx * int(math.sqrt(grids_num))
                    m_res.append(m_data[m_index])
    pd.DataFrame(m_res).to_csv(m_target_dir + city + '.CSV', index=False, header=False)


def run():
    m_dir = '../00_Data/with_head/'
    m_pd = pd.read_csv('../00_Data/info/city.CSV')
    # m_side_length = int(input('please input the length of side:'))
    grids_num = 900
    # 2, 3, 5, 6, 10, 15,
    for m_side_length in [1, 2, 3, 5, 6, 10, 15, 30]:
        print('m_side_length', ':', m_side_length)
        for m_index in range(0, len(m_pd)):
            print(m_pd.iloc[m_index, 0])
            change_data(m_dir, m_pd.iloc[m_index, 0], grids_num, m_side_length)


if __name__ == '__main__':
    run()
