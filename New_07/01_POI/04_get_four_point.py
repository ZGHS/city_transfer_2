import pandas as pd


def get_range(x, y, unit_x, unit_y, no, cols):
    xx = x + no % cols * unit_x
    yy = y - no / cols * unit_y
    return round(xx, 5), round(yy - unit_y, 5), round(xx + unit_x, 5), round(yy, 5)


def get_param(center_x, center_y, rows, cols):
    unit_x = 0.02
    # unit_y = 0.017
    unit_y = 0.02
    x_cost = cols / 2 * unit_x
    y_cost = rows / 2 * unit_y
    left_top_x = round(center_x - x_cost, 5)
    left_top_y = round(center_y + y_cost, 5)
    para = [left_top_x, left_top_y, unit_x, unit_y, cols, rows * cols]
    return para


def run2():
    m_data = pd.read_csv('center_point.CSV')
    m_data = m_data.to_numpy()
    m_res = []
    for m_row in m_data:
        city_name = m_row[0]
        center_x = round(m_row[1], 5)
        center_y = round(m_row[2], 5)

        m_para = get_param(center_x, center_y, 30, 30)
        top_left_x = m_para[0]
        top_left_y = m_para[1]

        m_range = get_range(top_left_x, top_left_y, m_para[2], m_para[3], 29, 30)
        top_right_x = m_range[2]
        top_right_y = m_range[3]
        m_range = get_range(top_left_x, top_left_y, m_para[2], m_para[3], 870, 30)
        bottom_left_x = m_range[0]
        bottom_left_y = m_range[1]
        m_range = get_range(top_left_x, top_left_y, m_para[2], m_para[3], 899, 30)
        bottom_right_x = m_range[2]
        bottom_right_y = m_range[1]

        print(city_name, center_x, center_y, top_left_x, top_left_y, top_right_x, top_right_y, bottom_left_x,
              bottom_left_y,
              bottom_right_x, bottom_right_y)
        m_res.append([city_name, center_x, center_y, top_left_x, top_left_y, top_right_x, top_right_y, bottom_right_x,
                      bottom_right_y, bottom_left_x,
                      bottom_left_y])
    m_res = pd.DataFrame(m_res, columns=['city_name', 'center_x', 'center_y', 'top_left_x', 'top_left_y', 'top_right_x',
                                         'top_right_y',
                                         'bottom_left_x',
                                         'bottom_left_y',
                                         'bottom_right_x', 'bottom_right_y'])
    m_res.to_csv('res.CSV', index=False)


def run():
    m_data = pd.read_csv('center_point.CSV')
    m_data = m_data.to_numpy()
    m_res = []
    for m_row in m_data:
        city_name = m_row[0]
        center_x = round(m_row[1], 5)
        center_y = round(m_row[2], 5)

        m_para = get_param(center_x, center_y, 30, 30)
        top_left_x = m_para[0]
        top_left_y = m_para[1]

        m_range = get_range(top_left_x, top_left_y, m_para[2], m_para[3], 29, 30)
        top_right_x = m_range[2]
        top_right_y = m_range[3]
        m_range = get_range(top_left_x, top_left_y, m_para[2], m_para[3], 870, 30)
        bottom_left_x = m_range[0]
        bottom_left_y = m_range[1]
        m_range = get_range(top_left_x, top_left_y, m_para[2], m_para[3], 899, 30)
        bottom_right_x = m_range[2]
        bottom_right_y = m_range[1]

        print(city_name, center_x, center_y, top_left_x, top_left_y, top_right_x, top_right_y, bottom_left_x,
              bottom_left_y,
              bottom_right_x, bottom_right_y)
        m_res.append([city_name, top_left_x, top_left_y, top_right_x, top_right_y, bottom_right_x,
                      bottom_right_y, bottom_left_x,
                      bottom_left_y, top_left_x, top_left_y])
    m_res = pd.DataFrame(m_res, columns=['city_name', 'top_left_x', 'top_left_y', 'top_right_x',
                                         'top_right_y',
                                         'bottom_left_x',
                                         'bottom_left_y',
                                         'bottom_right_x', 'bottom_right_y', 'top_left_x', 'top_left_y'])
    m_res.to_csv('four_points.CSV', index=False)


if __name__ == '__main__':
    run()
