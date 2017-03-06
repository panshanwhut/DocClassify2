# -*- coding:utf-8 -*-
import sys, os, jieba
import threadpool
import time

"使用jieba进行中文分词"

reload(sys)
sys.setdefaultencoding("utf-8")


"对指定目录下的文件进行分词"
def process(num):
    # src_dir = os.path.join("/home/panshan/PycharmProjects/DocClassify2/train_raw", str(num))
    # des_dir = os.path.join("/home/panshan/PycharmProjects/DocClassify2/train_seg", str(num))
    src_dir = os.path.join("/home/panshan/PycharmProjects/DocClassify2/test_raw", str(num))
    des_dir = os.path.join("/home/panshan/PycharmProjects/DocClassify2/test_seg", str(num))

    if not os.path.exists(des_dir):
        os.mkdir(des_dir)

    "列出指定目录下的所有文件"
    files = os.listdir(src_dir)

    for file in files:
        src_path = os.path.join(src_dir, str(file))
        des_path = os.path.join(des_dir, str(file))

        content_seg = read(src_path)
        write(content_seg, des_path)

"根据文件名读取文件，分词处理，返回分词后的字符串"
def read(src_path):
    content_seg = ""
    with open(src_path, 'r') as fi:
        content = fi.read()
        content = content.replace("\r\n", "").replace(" ", "")
        seg_list = jieba.cut(content, cut_all=False)
        content_seg = " ".join(seg_list)

    return content_seg

"存储分词后的结果至指定文件"
def write(content_seg, des_path):
    with open(des_path, 'w') as fo:
        fo.write(content_seg)

    print "save successfully"

"多线程处理"
def multi_thread():
    pool = threadpool.ThreadPool(8)
    requests = threadpool.makeRequests(process, [num for num in range(1,9)])
    for req in requests:
        pool.putRequest(req)

    pool.wait()

if __name__ == '__main__':
    start = time.time()

    multi_thread()

    end = time.time()
    print end-start