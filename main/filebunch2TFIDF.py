# -*- coding:utf-8 -*-
import sys
import time

from Tools import Tools

from sklearn.datasets.base import Bunch
from sklearn.feature_extraction.text import TfidfTransformer, TfidfVectorizer

#配置UTF8输出环境
reload(sys)
sys.setdefaultencoding('utf-8')

"""
将分词后bunch结构的文本转换为tfidf词向量空间对象
"""


"获取停用词文件，转换为停用词表"
def getStopWords(stop_words_paths = []):
    stop_words = list()

    for stop_words_path in stop_words_paths:
        with open(stop_words_path, 'r') as fi:
            content = fi.read().splitlines()
            stop_words.extend(content)
            del content

    stop_words = list(set(stop_words))  #去重复
    return stop_words

"生成训练集的TF-IDF词向量空间对象"
def createTrainTFIDF(train_seg_bunch, stop_words):
    train_tfidfspace = Bunch(targetlabels = train_seg_bunch.targetlabels, filelabels = train_seg_bunch.filelabels, filepaths = train_seg_bunch.filepaths, tdm = [], vocab = {})
    vectorizer = TfidfVectorizer(stop_words = stop_words, sublinear_tf = True, max_df = 0.5)

    "将文本转化为词频矩阵，单独保存字典文件"
    train_tfidfspace.tdm = vectorizer.fit_transform(train_seg_bunch.contents)
    train_tfidfspace.vocab = vectorizer.vocabulary_

    return train_tfidfspace

"生成测试集的TF-IDF词向量空间对象"
def createTestTFIDF(test_seg_bunch, train_tfidfspace, stop_words):
    test_tfidfspace = Bunch(targetlabels = test_seg_bunch.targetlabels, filelabels = test_seg_bunch.filelabels, filepaths = test_seg_bunch.filepaths, tdm = [], vocab = {})
    vectorizer = TfidfVectorizer(stop_words = stop_words, sublinear_tf = True, max_df = 0.5, vocabulary = train_tfidfspace.vocab)

    "将文本转化为词频矩阵，单独保存字典文件"
    test_tfidfspace.tdm = vectorizer.fit_transform(test_seg_bunch.contents)
    test_tfidfspace.vocab = train_tfidfspace.vocab

    return test_tfidfspace


if __name__ == '__main__':
    start = time.time()

    "定义路径"
    stop_words_paths = ["/home/panshan/PycharmProjects/DocClassify2/stop_words1.txt",
                        "/home/panshan/PycharmProjects/DocClassify2/stop_words2.txt"]

    train_seg_bunch_path = "/home/panshan/PycharmProjects/DocClassify2/train_seg_bunch.dat"
    train_tfidfspace_path = "/home/panshan/PycharmProjects/DocClassify2/train_tfidfspace.dat"
    test_seg_bunch_path = "/home/panshan/PycharmProjects/DocClassify2/test_seg_bunch.dat"
    test_tfidfspace_path = "/home/panshan/PycharmProjects/DocClassify2/test_tfidfspace.dat"

    "获取停用词列表"
    stop_words = getStopWords(stop_words_paths)

    "反序列化得到seg_bunch对象"
    tool = Tools()
    train_seg_bunch = tool.deSerialize(train_seg_bunch_path)
    test_seg_bunch = tool.deSerialize(test_seg_bunch_path)

    "生成TF-IDF词向量空间对象"
    train_tfidfspace = createTrainTFIDF(train_seg_bunch, stop_words)
    test_tfidfspace = createTestTFIDF(test_seg_bunch, train_tfidfspace, stop_words)

    "序列tfidfspace化到文件"
    tool.serialize(train_tfidfspace, train_tfidfspace_path)
    tool.serialize(test_tfidfspace, test_tfidfspace_path)

    end = time.time()
    print "total times:%ds" % (end - start)