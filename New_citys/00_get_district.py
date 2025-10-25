# -*- coding:UTF-8 -*-
import os
import time

import pandas as pd
import requests
from bs4 import BeautifulSoup


def get_return(m_website):
    try:
        time.sleep(1)
        req = requests.get(url=m_website)
        req.encoding = 'gb2312'  # 编码转换
    except Exception as e:
        print('无效网址!!!')
        return None
    html = req.text
    bf = BeautifulSoup(html, features="lxml")
    return bf


def get_province_https_dict(m_website):
    bf = get_return(m_website)
    if bf is None:
        return []
    m_res = []
    m_province_names = []
    m_trs = bf.find_all('tr',
                        class_='provincetr')
    for m_tr in m_trs:
        m_tds = m_tr.find_all('td')
        for m_td in m_tds:
            m_a = m_td.find('a')
            if m_a is None:
                break
            m_res.append(m_website[0:m_website.rfind('/') + 1] + m_a['href'])
            m_province_names.append(m_a.text)
    m_dict = dict(list(zip(m_province_names, m_res)))
    return m_dict


def get_city_https_dict(m_website):
    bf = get_return(m_website)
    if bf is None:
        return []
    m_res = []
    m_city_names = []
    m_trs = bf.find_all('tr', class_='citytr')
    for m_tr in m_trs:
        m_as = m_tr.find_all('a')
        m_res.append(m_website[0:m_website.rfind('/') + 1] + m_as[1]['href'])
        m_city_names.append(m_as[1].text)
    m_dict = dict(list(zip(m_city_names, m_res)))
    return m_dict


def get_district_https_dict(m_website):
    bf = get_return(m_website)
    if bf is None:
        return []
    m_res = []
    m_district_names = []
    m_trs = bf.find_all('tr', class_='countytr')
    for m_tr in m_trs:
        m_as = m_tr.find_all('a')
        if len(m_as) != 0:
            m_res.append(m_website[0:m_website.rfind('/') + 1] + m_as[1]['href'])
            m_district_names.append(m_as[1].text)
    m_dict = dict(list(zip(m_district_names, m_res)))
    return m_dict


def run():
    m_province_https_dict = get_province_https_dict(
        'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2020/index.html')
    m_root_dir = 'citys/'
    for m_item in m_province_https_dict:
        if not os.path.exists(m_root_dir + m_item):
            os.mkdir(m_root_dir + m_item)

        m_city_https_dict = get_city_https_dict(m_province_https_dict[m_item])
        print(list(m_city_https_dict.keys()))
        for m_item_x in m_city_https_dict:
            m_district_https_dict = get_district_https_dict(m_city_https_dict[m_item_x])
            print(list(m_district_https_dict.keys()))
            if m_item_x == '市辖区':
                pd.DataFrame(m_district_https_dict.keys()).to_csv(m_root_dir + m_item + '/' + m_item + '.CSV',
                                                                  index=False, header=False)
            else:
                pd.DataFrame(m_district_https_dict.keys()).to_csv(m_root_dir + m_item + '/' + m_item_x + '.CSV',
                                                                  index=False, header=False)


if __name__ == '__main__':
    run()
