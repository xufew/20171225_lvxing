# =======================
# -*- coding: utf-8 -*-
# author: LONGFEI XU
# Try your best
# ============
import os
import pickle

import pandas as pd

import few_model


def predict(modelSavePath, param):
    inputPath = './data/test_use/label_test.csv'
    savePath = './data/tmp_result.csv'
    comparePath = './data/result_compare.csv'
    finalPath = './data/result.csv'
    testX = pd.read_table(inputPath, sep=',', index_col=0)
    testX = testX.drop(['orderType'], axis=1)
    with open(modelSavePath, 'rb') as fileReader:
        gbdtModel = pickle.load(fileReader)
    predictValue = few_model.Xgboost.predict(testX, gbdtModel, param)
    with open(savePath, 'wb') as fileWriter:
        fileWriter.write('userid,orderType\n'.encode('utf8'))
        for i in range(len(testX.index)):
            fileWriter.write(
                    '{},{}\n'.format(
                        testX.index[i], predictValue[i]
                        ).encode('utf8')
                    )
    runAwk = "awk -F',' -v OFS=',' '{if(NR==FNR){a[$1]=$2}else{if(a[$1]){print $1,a[$1]}}}' %s %s > %s" % (savePath, comparePath, finalPath)
    os.system(runAwk)


if __name__ == '__main__':
    inputPath = './data/train_use/label_train.csv'
    modelSavePath = './model/gbdt_c.pkl'
    trainData = pd.read_table(inputPath, sep=',', index_col=0)
    trainX = trainData.drop(['orderType'], axis=1)
    trainY = trainData['orderType']
    # 开始交叉验证
    setNa = -9999999999999999999
    inputParam = {
            'naData': setNa,
            'scale_pos_weight': 0.2,
            'max_depth': 8,
            'subsample': 1,
            'col_sample_bytree': 1,
            'min_child_weight': 5,
            'num_roud': 90,
            }
    param = few_model.Xgboost.set_param(inputParam)
    trainX = trainX.fillna(setNa)
    few_model.Xgboost.cross_validation(trainX, trainY, param)
    # # 开始训练
    # few_model.Xgboost.train(trainX, trainY, param, modelSavePath)
    # 预测
    # predict(modelSavePath, param)
