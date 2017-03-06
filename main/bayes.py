# -*- coding:utf-8 -*-
from Tools import Tools
from sklearn.naive_bayes import MultinomialNB   #导入多项式贝叶斯算法包

"执行贝叶斯分类"

if __name__ == '__main__':
    train_tfidfspace_path = "/home/panshan/PycharmProjects/DocClassify2/train_tfidfspace.dat"
    test_tfidfspace_path = "/home/panshan/PycharmProjects/DocClassify2/test_tfidfspace.dat"

    "导入训练集/测试集词袋"
    tool = Tools()
    train_tfidfspace = tool.deSerialize(train_tfidfspace_path)
    test_tfidfspace = tool.deSerialize(test_tfidfspace_path)

    "应用朴素贝叶斯算法，训练分类器"
    # alpha:0.001   alpha越小，迭代次数越多，精度越高
    clf = MultinomialNB(alpha=0.01).fit(train_tfidfspace.tdm, train_tfidfspace.filelabels)

    "预测分类结果"
    predicted = clf.predict(test_tfidfspace.tdm)
    total_num = len(predicted)
    error_num = 0

    for filelabel, filepath, predictlabel in zip(test_tfidfspace.filelabels, test_tfidfspace.filepaths, predicted):
        if filelabel != predictlabel:
            error_num += 1
            print filepath,":实际类别:",filelabel,"预测类别:",predictlabel

    print "error rate:", float(error_num)*100/total_num,"%"