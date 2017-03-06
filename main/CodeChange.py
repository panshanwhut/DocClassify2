# -*- coding:utf-8 -*-
import chardet,sys
import os, os.path
import threadpool
import time


reload(sys)
sys.setdefaultencoding('utf-8')

"""
change the files' code from GBK to UTF-8
"""

def gbk2utf8(dir_num):
    src_dir = os.path.join("/home/panshan/PycharmProjects/DocClassify2/traindata", str(dir_num))
    des_dir = os.path.join("/home/panshan/PycharmProjects/DocClassify2/train_raw", str(dir_num))
    # src_dir = os.path.join("/home/panshan/PycharmProjects/DocClassify2/testdata", str(dir_num))
    # des_dir = os.path.join("/home/panshan/PycharmProjects/DocClassify2/test_raw", str(dir_num))

    if not os.path.exists(des_dir):
        os.mkdir(des_dir)

    "指定目录下的所有文件"
    files = os.listdir(src_dir)

    "依次遍历所有文件，将文件转码，并写入指定目录下，文件名保持不变"
    for file in files:
        src_path = os.path.join(src_dir, str(file))
        des_path = os.path.join(des_dir, str(file))

        page = ""
        with open(src_path, 'r') as fi:
            page = fi.read()

        page = page.decode("GBK",'ignore').encode('utf-8')
        with open(des_path, 'w') as fo:
            fo.write(page)

        print "successfully:"+str(file)


"多线程执行"
def multiThread():
    pool = threadpool.ThreadPool(8)
    requests = threadpool.makeRequests(gbk2utf8, [num for num in range(1, 9)])
    for req in requests:
        pool.putRequest(req)

    pool.wait()


if __name__ == '__main__':
    start = time.time()

    multiThread()

    end = time.time()
    print end - start