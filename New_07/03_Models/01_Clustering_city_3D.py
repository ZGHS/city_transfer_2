import os

import joblib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.decomposition import PCA


def get_data(cluster_condition, side_length):
    m_root_dir = 'data/with_head/N_' + str(side_length) + '/'
    all_city_file_names = os.listdir(m_root_dir)
    m_res = []
    m_city_names = []
    for m_name in all_city_file_names:
        m_city_names.append(os.path.splitext(m_name)[0])
        m_temp = pd.read_csv(m_root_dir + m_name)[[cluster_condition]].to_numpy()
        for i in range(0, 900 - side_length, side_length * side_length):
            m_x = m_temp[i:i + side_length * side_length].reshape((1, side_length * side_length))
            m_res.append(list(m_x[0]))
    m_res = np.array(m_res)
    return m_res, m_city_names


def down_dim(m_data):
    m_pca = PCA(n_components=3)
    m_data = m_pca.fit_transform(m_data)
    return m_data


def get_label_res(X, model_dir):
    m_kmeans = joblib.load(model_dir)
    labels = m_kmeans.predict(X)
    return labels


# start=============================================================================
def classify_city(m_clusters, side_length):
    m_list = ['food', 'edu', 'sport', 'nature', 'shopping', 'car_service', 'beauty', 'culture', 'entrance',
              'life_service', 'entertainment', 'company', 'finance', 'view', 'hotel', 'estate', 'traffic',
              'government',
              'medical']
    m_city_class_num_list = [4, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3]
    plt.figure(figsize=(24, 16))

    m_all_big_grid_labels = []
    m_all_big_grid_data = []
    m_all_big_grid_city_names = []

    for i in range(0, len(m_list)):
        cluster_condition = m_list[i]
        m_data, m_city_names = get_data(cluster_condition, side_length)

        m_labels = get_label_res(m_data, 'model_files/big_grid_models/' + cluster_condition + '.pkl')

        m_all_big_grid_labels.append(m_labels)
        m_all_big_grid_data.append(m_data)
        m_all_big_grid_city_names.append(m_city_names)

        labels = m_labels.reshape(
            (int(len(m_labels) / (int(30 / side_length) * int(30 / side_length))),
             int(30 / side_length) * int(30 / side_length)))
        city_class = get_label_res(labels, 'model_files/city_class_models/' + cluster_condition + '.pkl')
        print(cluster_condition, ':', city_class)

        m_csv_np_a = np.array(m_city_names)
        m_csv_np_b = np.array(city_class)
        m_csv_np = np.c_[m_csv_np_a, labels]
        m_csv_np = np.c_[m_csv_np, m_csv_np_b]
        pd.DataFrame(m_csv_np).to_csv('1_res/3D/0csv/' + cluster_condition + '.CSV',
                                      index=False)

        m_dim = down_dim(labels)
        m_dim = pd.DataFrame(m_dim, index=city_class)

        plt.subplot(4, 5, i + 1, projection='3d')
        plt.title(cluster_condition)
        m_markers = ['o', '^', '*', 'h', '+', 'x', '2', 'p', 's', 'd']
        for i in range(0, m_city_class_num_list[i]):
            d = m_dim.loc[i]
            if len(d.shape) == 1:
                d = pd.DataFrame(d.to_numpy().reshape((1, 3)))
            plt.plot(d[0], d[1], d[2], marker=m_markers[i], label=str(i))
        plt.legend()

    plt.tight_layout()
    plt.savefig('1_res/3D/city_class_3D.png', transparent=False, dpi=800, bbox_inches="tight")
    plt.show()

    draw_big_grid_class(m_all_big_grid_labels, m_all_big_grid_data, m_clusters)
    flag = input('是否继续visualize_city：yes ，no:')
    if flag != 'yes':
        return
    # visualize_city(m_list, m_all_big_grid_city_names, m_all_big_grid_labels, side_length)


# def visualize_city(m_list, m_all_big_grid_city_names, m_all_big_grid_labels, side_length):
#     for j in range(0, len(m_list)):
#         cluster_condition = m_list[j]
#         m_labels = m_all_big_grid_labels[j]
#         city = m_all_big_grid_city_names[0]
#
#         m_city_nums = pd.read_csv('../00_Data/info/city.CSV').to_numpy().shape[0]
#         m_unit = int(len(m_labels) / m_city_nums)
#         for i in range(0, m_city_nums):
#             m_arr = m_labels[i * m_unit: (i + 1) * m_unit]
#             m_arr = np.array(m_arr).reshape(int(30 / side_length), int(30 / side_length))
#             sns.heatmap(m_arr, annot=True, cmap='YlGnBu', linewidths=1, cbar=True, xticklabels=False, yticklabels=False,
#                         square=True)
#             plt.title(city[i])
#             if not os.path.exists('1_res/3D/city/' + cluster_condition):
#                 os.mkdir('1_res/3D/city/' + cluster_condition)
#             plt.savefig('1_res/3D/city/' + cluster_condition + '/' + city[i] + '.png', transparent=False, dpi=800,
#                         bbox_inches="tight")
#             plt.show()


def draw_big_grid_class(m_all_big_grid_labels, m_all_big_grid_data, n_clusters):
    m_list = ['food', 'edu', 'sport', 'nature', 'shopping', 'car_service', 'beauty', 'culture', 'entrance',
              'life_service', 'entertainment', 'company', 'finance', 'view', 'hotel', 'estate', 'traffic',
              'government',
              'medical']
    plt.figure(figsize=(28, 16))
    for i in range(0, len(m_list)):
        cluster_condition = m_list[i]

        m_data = m_all_big_grid_data[i]
        m_labels = m_all_big_grid_labels[i]

        print(cluster_condition, ':', m_labels)

        m_dim = down_dim(m_data)
        # print(m_dim)
        m_dim = pd.DataFrame(m_dim, index=m_labels)

        plt.subplot(4, 5, i + 1, projection='3d')

        # ax.scatter(m_dim[:, 0], m_dim[:, 0], m_dim[:, 0], marker='o')

        m_markers = ['o', '^', '*', 'h', '+', 'x', '2', 'p', 's', 'd']
        for i in range(0, n_clusters):
            d = m_dim.loc[i]
            if len(d.shape) == 1:
                d = pd.DataFrame(d.to_numpy().reshape((1, 3)))
            # ax.scatter3D(d[0], d[1], d[2], marker=m_markers[i], label=str(i))
            plt.plot(d[0], d[1], d[2], marker=m_markers[i], label=str(i))
        plt.title(cluster_condition)
        plt.legend()
    plt.savefig('1_res/3D/big_grids_class_3D.png', transparent=False, dpi=800, bbox_inches="tight")
    plt.show()


def run():
    m_side_length = int(input('please input the length of side:'))
    n_clusters = int(input('please input the n_clusters:'))
    classify_city(n_clusters, m_side_length)


if __name__ == '__main__':
    run()
