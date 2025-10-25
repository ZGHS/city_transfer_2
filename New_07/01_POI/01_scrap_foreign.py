import os

import requests
import xlwt


def get_mercator(types, a, b, c, d):
    num = 0

    # Zhangganghua
    api_addr = "http://api.map.baidu.com/place_abroad/v1/search?query=" + types + "&bounds=" + str(b) + "," + str(
        a) + "," + str(d) + "," + str(
        c) + "&page_num=" + str(num) + "&output=json&page_size=1&ak=4zeudMeNzQoMGmA9yrQG4EafijW5PVHl"
    req = requests.get(api_addr)
    content = req.json()
    if content['status'] == 0:
        return content['total']
    if content['status'] == 302:
        return -2
    return -1


def get_range(x, y, unit_x, unit_y, no, cols):
    xx = x + no % cols * unit_x
    yy = y - no / cols * unit_y
    return round(xx, 5), round(yy - unit_y, 5), round(xx + unit_x, 5), round(yy, 5)
    # return xx, yy - unit_y, xx + unit_x, yy


def write_into_excel(dir_name, m_type, x, y, unit_x, unit_y, cols, grids):
    print('*******', m_type, '*******')
    print('start……')
    workbook = xlwt.Workbook(encoding='utf-8')
    worksheet = workbook.add_sheet('My worksheet', cell_overwrite_ok=True)

    row = 0
    for no in range(grids):
        re = get_range(x, y, unit_x, unit_y, no, cols)
        xx = get_mercator(m_type, re[0], re[1], re[2], re[3])
        if xx == -1:
            xx = 0
        if xx == -2:
            print("超额")
            return
        print(xx)
        worksheet.write(row, 0, no)
        worksheet.write(row, 1, xx)
        row = row + 1

    workbook.save(dir_name)
    print('finished……')
    return


# start （通过经纬度，获取参数的部分）==========================================================================================
def get_param(center_x, center_y, rows, cols):
    unit_x = 0.02
    # unit_y = 0.017
    unit_y = 0.02
    x_cost = cols / 2 * unit_x
    y_cost = rows / 2 * unit_y
    left_top_x = round(center_x - x_cost, 5)
    left_top_y = round(center_y + y_cost, 5)
    para = [left_top_x, left_top_y, unit_x, unit_y, cols, rows * cols]
    print(para)
    return para


# end==========================================================================================


def run():
    city_name = input('城市英文名称：')
    pre_dir = 'scrap_res/'
    target_dir = pre_dir + city_name + '/'
    if not os.path.isdir(target_dir):
        os.mkdir(target_dir)
        print('目录不存在，已经创建。')
    m_center_input = input('目标城市的中心坐标：')
    center_x = float(m_center_input[:m_center_input.find(',')])
    center_y = float(m_center_input[m_center_input.find(',') + 1:])
    print(city_name, ':', '中心坐标 ', center_x, ',', center_y)
    para = get_param(center_x, center_y, 30, 30)

    flag = input('是否继续：yes ，no:')
    if flag != 'yes':
        return
    m_poi_name = ['美食', '酒店', '购物', '生活服务', '丽人', '旅游景点', '休闲娱乐', '运动健身', '教育培训', '文化传媒', '医疗', '汽车服务', '交通设施', '金融',
                  '房地产', '公司企业', '政府机构', '出入口', '自然地物']
    m_poi_type = ['food', 'hotel', 'shopping', 'life_service', 'beauty', 'view', 'entertainment', 'sport', 'edu',
                  'culture', 'medical', 'car_service', 'traffic', 'finance', 'estate', 'company', 'government',
                  'entrance', 'nature']
    # for i in range(1, len(m_poi_type)):
    for i in range(12, 13):
        print(i)
        write_into_excel(target_dir + m_poi_type[i] + '.xls', m_poi_name[i],
                         para[0],
                         para[1],
                         para[2],
                         para[3], para[4], para[5])


# 美食 food ***
# 酒店 hotel
# 购物 shopping ***
# 生活服务 life_service
# 丽人  beauty
# 旅游景点 view
# 休闲娱乐  entertainment
# 运动健身 sport
# 教育培训 edu
# 文化传媒  culture
# 医疗   medical
# 汽车服务   car_service
# 交通设施  traffic
# 金融  finance
# 房地产  estate ###
# 公司企业  company ###
# 政府机构   government
# 出入口   entrance
# 自然地物  nature


if __name__ == '__main__':
    run()
