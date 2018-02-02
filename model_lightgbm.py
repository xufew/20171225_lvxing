# =======================
# -*- coding: utf-8 -*-
# author: LONGFEI XU
# Try your best
# ============
import os
import pickle

import numpy as np
import pandas as pd

import few_model
import Config


def predict(modelPath):
    inputPath = Config.TEST_DATA_PATH
    savePath = './data/tmp_result.csv'
    comparePath = Config.RESULT_FINAL_TRANS
    finalPath = Config.RESULT_LIGHTGBM_CL
    testX = pd.read_table(inputPath, sep=',', index_col=0)
    with open(modelPath, 'rb') as fileReader:
        gbmModel = pickle.load(fileReader)
    predictValue = lightgbm.predict(testX, gbmModel)
    with open(savePath, 'wb') as fileWriter:
        fileWriter.write('userid,orderType\n'.encode('utf8'))
        for i in range(len(testX.index)):
            fileWriter.write(
                    '{},{}\n'.format(
                        testX.index[i], predictValue[i]
                        ).encode('utf8')
                    )
    runAwk = "awk -F',' -v OFS=',' '{if(NR==FNR){a[$1]=$2}else{if($1 in a){print $1,a[$1]}}}' %s %s > %s" % (savePath, comparePath, finalPath)
    os.system(runAwk)


def line_search(trainX, trainY):
    searchDic = {
            'learning_rate': [0.05],
            'num_leaves': list(range(100, 30, -10)),
            'bagging_fraction': [0.8],
            'feature_fraction': [0.4],
            'bagging_freq': [1],
            'lambda_l2': np.linspace(1, 50, 10),
            'min_data_in_leaf': list(range(50, 150, 20)),
            'min_sum_hessian_in_leaf': np.linspace(0.01, 5, 5),
            'num_trees': [1000],
            'application': ['binary'],
            }
    lightgbm.line_search(trainX, trainY, searchDic)


if __name__ == '__main__':
    inputPath = Config.TRAIN_DATA_PATH
    modelPath = Config.MODEL_LIGHTGBM_CL
    trainData = pd.read_table(inputPath, sep=',', index_col=0)
    # 删除无用纬度和数据
    trainX = trainData.drop(['orderType'], axis=1)
    trainY = trainData['orderType']
    params = {
            'learning_rate': 0.05,
            'num_leaves': 60,
            'num_trees': 490,
            'min_sum_hessian_in_leaf': 0.2,
            'min_data_in_leaf': 70,
            'bagging_fraction': 0.5,
            'feature_fraction': 0.3,
            'lambda_l1': 0,
            'lambda_l2': 11.88,
            'num_threads': 4,
            'scale_pos_weight': 1,
            'application': 'binary',
            }
    lightgbm = few_model.Lightgbm(params)
    # # 交叉验证
    # evalDic = lightgbm.cv(trainX, trainY)
    # 开始训练
    trainModel = lightgbm.train(trainX, trainY, modelPath)
    with open('./tmp_feature_im', 'wb') as fileWriter:
        for thisIndex in trainModel.featureIm.index:
            value = trainModel.featureIm[thisIndex]
            fileWriter.write(
                    '{}\t==={}===\n'.format(thisIndex, value).encode('utf8')
                    )
    # 预测
    predict(modelPath)
    # # 寻找最优变量
    # line_search(trainX, trainY)
