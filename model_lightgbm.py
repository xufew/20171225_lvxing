# =======================
# -*- coding: utf-8 -*-
# author: LONGFEI XU
# Try your best
# ============
import os
import pickle

import pandas as pd

import few_model


def predict(modelPath):
    inputPath = './data/test_use/label_test_combine.csv'
    savePath = './data/tmp_result.csv'
    comparePath = './data/result_compare.csv'
    finalPath = './data/result_lightgbm.csv'
    testX = pd.read_table(inputPath, sep=',', index_col=0)
    testX = testX.drop(['orderType'], axis=1)
    with open(modelPath, 'rb') as fileReader:
        gbmModel = pickle.load(fileReader)
    predictValue = few_model.Lightgbm.predict(testX, gbmModel)
    with open(savePath, 'wb') as fileWriter:
        fileWriter.write('userid,orderType\n'.encode('utf8'))
        for i in range(len(testX.index)):
            fileWriter.write(
                    '{},{}\n'.format(
                        testX.index[i], predictValue[i]
                        ).encode('utf8')
                    )
    runAwk = "awk -F',' -v OFS=',' '{if(NR==FNR){a[$1]=$2}else{if(a[$1]){print $1,a[$1]}}}' %s %s > %s" % (savePath, comparePath, finalPath)
    print(runAwk)
    os.system(runAwk)


if __name__ == '__main__':
    inputPath = './data/train_use/label_train_combine.csv'
    modelPath = './model/lightgbm.pkl'
    trainData = pd.read_table(inputPath, sep=',', index_col=0)
    # 删除无用纬度和数据
    trainX = trainData.drop(['orderType'], axis=1)
    trainY = trainData['orderType']
    params = {
            'learning_rate': 0.05,
            'num_leaves': 70,
            'num_trees': 470,
            'min_sum_hessian_in_leaf': 0.1,
            'min_data_in_leaf': 50,
            'feature_fraction': 0.3,
            'bagging_fraction': 0.5,
            'lambda_l1': 0,
            'lambda_l2': 10,
            'num_threads': 4,
            }
    params = few_model.Lightgbm.set_param(params)
    # # 交叉验证
    # evalDic = few_model.Lightgbm.cv(trainX, trainY, params)
    # 开始训练
    trainModel = few_model.Lightgbm.train(trainX, trainY, params, modelPath)
    with open('./tmp_feature_im', 'wb') as fileWriter:
        for thisIndex in trainModel.featureIm.index:
            value = trainModel.featureIm[thisIndex]
            fileWriter.write(
                    '{}\t==={}===\n'.format(thisIndex, value).encode('utf8')
                    )
    # 预测
    predict(modelPath)
