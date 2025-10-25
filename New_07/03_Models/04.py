from PIL import Image
import os


def load_data(poi_type):
    root_dir = '1_res/2D/city/' + poi_type
    class_dirs = os.listdir(root_dir)
    for class_dir in class_dirs:
        for img_file in os.listdir(os.path.join(root_dir, class_dir)):
            im = Image.open(root_dir + '/' + class_dir + '/' + img_file)
            pixdata = im.load()
            for y in range(im.size[1]):
                for x in range(im.size[0]):
                    print(pixdata[x, y])
                    if pixdata[x, y] == (255, 255, 255, 255):
                        pixdata[x, y] = (0, 0, 0, 0)
            im.save(root_dir + '/' + class_dir + '/' + img_file)


def run():
    m_poi_type = ['food', 'hotel', 'shopping', 'life_service', 'beauty', 'view', 'entertainment', 'sport', 'edu',
                  'culture', 'medical', 'car_service', 'traffic', 'finance', 'estate', 'company', 'government',
                  'entrance', 'nature']
    for xx in m_poi_type:
        load_data(xx)


if __name__ == '__main__':
    im = Image.open('1_res/2D/city/beauty/1/Fuzhou.png')
    pixdata = im.load()
    aa = set()
    for y in range(im.size[1]):
        for x in range(im.size[0]):
            aa.add(pixdata[x, y])
            if pixdata[x, y] == (255, 255, 255, 255):
                pixdata[x, y] = (0, 0, 0, 0)
    print(aa)
    # run()
