# -*- coding:utf-8 -*-
from sklearn.datasets.base import Bunch
import os, os.path
import threadpool
import time
from Tools import Tools

"将分词完毕的文本持久化为bunch数据结构"
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

bunch_list = []

src_dir = "/home/panshan/PycharmProjects/DocClassify2/train_seg"
des_path = "/home/panshan/PycharmProjects/DocClassify2/train_seg_bunch.dat"
# src_dir = "/home/panshan/PycharmProjects/DocClassify2/test_seg"
# des_path = "/home/panshan/PycharmProjects/DocClassify2/test_seg_bunch.dat"


"指定类别，将类别下的所有文件转化为bunch形式，返回bunch形式"
def seg2Bunch(filelabel):
    "获取子目录"
    child_dir = os.path.join(src_dir, str(filelabel))

    "获取子目录下所有文件"
    files = os.listdir(child_dir)

    "生成bunch对象"
    bunch = Bunch(targetlabels=[], filelabels=[], filepaths=[], contents=[])

    "依次遍历该目录下所有文件"
    for file in files:
        filepath = os.path.join(child_dir, file)   #文件路径

        bunch.filelabels.append(filelabel)
        bunch.filepaths.append(filepath)

        content = ""
        with open(filepath, 'r') as fi:
            content = fi.read()
        bunch.contents.append(content)

    global bunch_list
    bunch_list.append(bunch)
    del bunch

    print filelabel," bunch successfully"

"多线程实现"
def multi_thread():
    global bunch_list

    pool = threadpool.ThreadPool(8)
    requests = threadpool.makeRequests(seg2Bunch, [num for num in range(1, 9)])
    for req in requests:
        pool.putRequest(req)
    pool.wait()

    return bunch_list

"序列化到磁盘文件"
def bunchSerialize(bunch_list):
    total = Bunch(targetlabels=[], filelabels=[], filepaths=[], contents=[])
    total.targetlabels.extend([1,2,3,4,5,6,7,8])

    "依次遍历results中的每个bunch对象，将bunch对象的内容追加到统一的bunch中"
    "选择每次弹出一个bunch，用完后删除，回收内存空间"
    while len(bunch_list) > 0:
        tmp = bunch_list.pop()
        total.filelabels.extend(tmp.filelabels)
        total.filepaths.extend(tmp.filepaths)
        total.contents.extend(tmp.contents)

        del tmp

    tool = Tools()
    tool.serialize(total, des_path)

if __name__ == '__main__':
    start = time.time()

    bunch_list = multi_thread()
    bunchSerialize(bunch_list)

    end = time.time()
    print "total times:%ds" % (end - start)