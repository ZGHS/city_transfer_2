import random

import joblib
import pandas as pd


def get_model(model_dir):
    m_kmeans = joblib.load(model_dir)
    return m_kmeans


def run():
    poi_type = 'beauty'
    # m_array = [[1, 1, 1, 1, 2, 1, 1, 1, 1], [None, None, 1, 1, 2, 1, 1, 1, 1]]
    # m_array = np.array(m_array)
    # imp = SimpleImputer(missing_values=np.nan, strategy='mean')
    # m_array = imp.fit_transform(m_array)
    # print(m_array)

    model_dir = 'model_files/city_class_models/' + poi_type + '.pkl'
    m_model = get_model(model_dir)

    file_dir = '1_res/2D/0csv/' + poi_type + '.CSV'
    m_data = pd.read_csv(file_dir)
    print(m_data)
    print(random.randrange(1, 5))
    print(random.randint(1, 5))
    print(random.sample([i for i in range(0, 9)], 3))

    m_data = m_data.iloc[0, :].to_numpy()
    m_data = list(m_data)
    print(m_data)
    m_city_name = m_data[0]
    m_city_class = m_data[-1]
    print(m_city_name)
    print(m_city_class)
    m_data = m_data[1:-1]
    print(m_data)

    # m_time = 0
    # for i in range(0, 100):
    #     m_random_a = random.sample([i for i in range(0, 9)], 1)
    #     m_data[m_random_a[0]] = random.choice([i for i in range(0, 3)])
    #     # m_data[m_random_a[1]] = random.choice([i for i in range(0, 3)])
    #     # m_data[m_random_a[2]] = random.choice([i for i in range(0, 3)])
    #     m_res = m_model.predict([m_data])
    #     if m_res == m_city_class:
    #         m_time += 1
    # print("{:.2%}".format(m_time / 100))




if __name__ == '__main__':
    run()
