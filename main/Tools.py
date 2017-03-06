# -*- coding:utf-8 -*-
import cPickle

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

"""
工具类，提供序列化/反序列化方法

"""
class Tools:
    def __init__(self):
        pass

    def serialize(self, obj, des_path):
        fo = open(des_path, 'w')
        cPickle.dump(obj, fo)
        fo.close()

        print "serialize successfully"

    def deSerialize(self, src_path):
        fi = open(src_path, 'r')
        obj = cPickle.load(fi)
        fi.close()

        return obj
