import os
import shutil

import joblib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.cluster import KMeans
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


def get_label_res(X, n_clusters, model_dir):
    m_kmeans = KMeans(n_clusters=n_clusters, random_state=1)
    m_kmeans.fit(X)
    joblib.dump(m_kmeans, model_dir)
    m_predict = m_kmeans.predict(X)
    return m_predict


# start=============================================================================
def classify_res(m_clusters, side_length):
    m_list = ['food', 'edu', 'sport', 'nature', 'shopping', 'car_service', 'beauty', 'culture', 'entrance',
              'life_service', 'entertainment', 'company', 'finance', 'view', 'hotel', 'estate', 'traffic',
              'government',
              'medical']
    m_city_class_num_list = [4, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3]
    plt.figure(figsize=(24, 16))

    m_all_big_grid_labels = []
    m_all_big_grid_data = []
    m_all_big_grid_city_names = []
    m_all_city_class = []

    for i in range(0, len(m_list)):
        cluster_condition = m_list[i]
        m_data, m_city_names = get_data(cluster_condition, side_length)
        m_labels = get_label_res(m_data, m_clusters, 'model_files/big_grid_models/' + cluster_condition + '.pkl')

        m_all_big_grid_labels.append(m_labels)
        m_all_big_grid_data.append(m_data)
        m_all_big_grid_city_names.append(m_city_names)

        labels = m_labels.reshape(
            (int(len(m_labels) / (int(30 / side_length) * int(30 / side_length))),
             int(30 / side_length) * int(30 / side_length)))
        city_class = get_label_res(labels, m_city_class_num_list[i],
                                   'model_files/city_class_models/' + cluster_condition + '.pkl')
        m_all_city_class.append(city_class)

        print(cluster_condition, ':', city_class)

        m_csv_np_a = np.array(m_city_names)
        m_csv_np_b = np.array(city_class)
        m_csv_np = np.c_[m_csv_np_a, labels]
        m_csv_np = np.c_[m_csv_np, m_csv_np_b]
        pd.DataFrame(m_csv_np).to_csv('1_res/2D/csv/' + cluster_condition + '.CSV',
                                      index=False)

        m_dim = down_dim(labels)
        # print(m_dim)
        m_dim = pd.DataFrame(m_dim, index=city_class)

        plt.subplot(4, 5, i + 1)
        plt.title(cluster_condition)
        m_markers = ['o', '^', '*', 'h', 'P', 'd', '2', 'p', 's', 'X']
        for i in range(0, m_city_class_num_list[i]):
            d = m_dim.loc[i]
            # plt.scatter(d[0], d[1], marker=m_markers[i], label=str(i), alpha=1 / 5)
            plt.plot(d[0], d[1], marker=m_markers[i], label=str(i))
        plt.legend()
        # plt.xlabel('y', m_font)
        # plt.ylabel('x', m_font)

    plt.tight_layout()
    plt.savefig('1_res/2D/city_class_2D.png', transparent=False, dpi=800, bbox_inches="tight")
    plt.show()

    draw_big_grid_class(m_all_big_grid_labels, m_all_big_grid_data, m_clusters)
    flag = input('是否继续visualize_city：yes ，no:')
    if flag != 'yes':
        return
    visualize_city(m_list, m_all_big_grid_city_names, m_all_big_grid_labels, m_all_city_class, m_city_class_num_list,
                   side_length)


# end =============================================================================

def visualize_city(m_list, m_all_big_grid_city_names, m_all_big_grid_labels, m_all_city_class, m_city_class_num_list,
                   side_length):
    for ii in os.listdir('1_res/2D/city'):
        shutil.rmtree(os.path.join('1_res/2D/city', ii))
    for j in range(0, len(m_list)):
        cluster_condition = m_list[j]
        m_labels = m_all_big_grid_labels[j]
        city = m_all_big_grid_city_names[0]
        m_city_nums = pd.read_csv('../00_Data/info/city.CSV').to_numpy().shape[0]
        m_unit = int(len(m_labels) / m_city_nums)
        for i in range(0, m_city_nums):
            m_arr = m_labels[i * m_unit: (i + 1) * m_unit]
            m_arr = np.array(m_arr).reshape(int(30 / side_length), int(30 / side_length))
            sns.heatmap(m_arr, vmin=0, vmax=2, annot=False, cmap='YlGnBu', linewidths=0, cbar=False, xticklabels=False,
                        yticklabels=False,
                        square=True)
            # plt.title(city[i])
            if not os.path.exists('1_res/2D/city/' + cluster_condition):
                os.mkdir('1_res/2D/city/' + cluster_condition)
            for mm in range(0, m_city_class_num_list[j]):
                if not os.path.exists('1_res/2D/city/' + cluster_condition + '/' + str(mm)):
                    os.mkdir('1_res/2D/city/' + cluster_condition + '/' + str(mm))
            # plt.tight_layout()
            plt.savefig(
                '1_res/2D/city/' + cluster_condition + '/' + str(m_all_city_class[j][i]) + '/' + city[i] + '.png',
                transparent=False, dpi=10,
                bbox_inches="tight")
            plt.show()


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
        m_dim = pd.DataFrame(m_dim, index=m_labels)

        plt.subplot(4, 5, i + 1)
        m_markers = ['o', '^', '*', 'h', '+', 'x', '2', 'p', 's', 'd']
        for i in range(0, n_clusters):
            d = m_dim.loc[i]
            # plt.scatter(d[0], d[1], marker=m_markers[i], label=str(i), alpha=1 / 5)
            plt.plot(d[0], d[1], marker=m_markers[i], label=str(i))
        plt.title(cluster_condition)
        plt.legend()

    plt.savefig('1_res/2D/big_grids_class_2D.png', transparent=False, dpi=800, bbox_inches="tight")
    plt.show()


def down_dim(m_data):
    m_pca = PCA(n_components=2)
    m_data = m_pca.fit_transform(m_data)
    return m_data


def run():
    m_side_length = int(input('please input the length of side:'))
    n_clusters = int(input('please input the n_clusters:'))
    classify_res(n_clusters, m_side_length)


if __name__ == '__main__':
    run()
