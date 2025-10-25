import os

# srcfile 需要复制、移动的文件
# dstpath 目的地址
import shutil
from glob import glob


def mycopyfile(srcfile, dstpath):  # 复制函数
    if not os.path.isfile(srcfile):
        print("%s not exist!" % (srcfile))
    else:
        fpath, fname = os.path.split(srcfile)  # 分离文件名和路径
        if not os.path.exists(dstpath):
            os.makedirs(dstpath)  # 创建路径
        shutil.copy(srcfile, dstpath + fname)  # 复制文件
        print("copy %s -> %s" % (srcfile, dstpath + fname))


root_dir = input("请输入根目录(a_15, b_10, c_6, d_3)：")
poi_type = input("请输入POI类型：")
TEMP_DIR = "labeled"
dir_str = os.path.join(root_dir, poi_type)
son_dirs = os.listdir(dir_str)
for son_dir in son_dirs:
    print(son_dir)
    pics = os.listdir(os.path.join(dir_str, son_dir))
    temp_list = []
    for pic in pics:
        city_name = os.path.splitext(pic)[0]
        temp_list.append(city_name)

        srcfile = './0csv/' + TEMP_DIR + '/' + city_name + '.CSV'
        dst_dir = './final_data/' + TEMP_DIR + '/' + poi_type + '/' + son_dir + '/'  # 目的路径记得加斜杠
        # src_file_list = glob(src_dir + '*')  # glob获得路径下所有文件，可根据需要修改
        # for srcfile in src_file_list:
        # mycopyfile(srcfile, dst_dir)  # 复制文件
    print(temp_list)
