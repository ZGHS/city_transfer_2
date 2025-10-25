import os

import pandas as pd
import xlrd


def readExcel(file):
    data = xlrd.open_workbook(file)
    rtable = data.sheets()[0]
    row_v = rtable.row_values
    col_v = rtable.col_values
    return row_v, col_v


def write_into_csv(dir_name, all_cols):
    m_array = []
    for i in range(0, len(all_cols[0](1))):
        temp_row_list = []
        for cols in all_cols:
            temp_row_list.append(cols(1)[i])
        m_array.append(temp_row_list)
    pd.DataFrame(m_array).to_csv(dir_name, header=False, index=False)
    print('导出完成:', dir_name)
    return


def m_function(city):
    list_names = ['food', 'edu', 'sport', 'nature', 'shopping', 'car_service', 'beauty', 'culture', 'entrance',
                  'life_service', 'entertainment', 'company', 'finance', 'view', 'hotel', 'estate', 'traffic',
                  'government',
                  'medical']
    all_cols = []
    print(list_names)
    for list_name in list_names:
        data = readExcel('scrap_res/' + city + '/' + list_name + '.xls')
        cols_v = data[1]
        all_cols.append(cols_v)
    print('总共', len(all_cols), '列')
    write_into_csv('merge_res/' + city + '.CSV', all_cols)
    if not os.path.exists('../00_Data/without_head/' + city + '.CSV'):
        write_into_csv('../00_Data/without_head/' + city + '.CSV', all_cols)


def run():
    city_names = pd.read_csv('../00_Data/info/city.CSV')
    city_names = list(city_names['city'].to_numpy())

    for city in city_names:
        if not os.path.exists('merge_res/' + city + '.CSV'):
            m_function(city)


if __name__ == '__main__':
    run()
