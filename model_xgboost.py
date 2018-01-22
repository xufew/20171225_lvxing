# =======================
# -*- coding: utf-8 -*-
# author: LONGFEI XU
# Try your best
# ============
import os
import pickle

import pandas as pd

import few_model
import Config


def predict(modelSavePath, xgboost):
    inputPath = Config.TEST_DATA_PATH
    savePath = './data/tmp_result.csv'
    comparePath = Config.RESULT_FINAL_TRANS
    finalPath = Config.RESULT_XGBOOST_C
    testX = pd.read_table(inputPath, sep=',', index_col=0)
    testX = testX.drop(['orderType'], axis=1)
    with open(modelSavePath, 'rb') as fileReader:
        gbdtModel = pickle.load(fileReader)
    predictValue = xgboost.predict(testX, gbdtModel)
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


if __name__ == '__main__':
    inputPath = Config.TRAIN_DATA_PATH
    modelSavePath = Config.MODEL_XGBOOST_C
    trainData = pd.read_table(inputPath, sep=',', index_col=0)
    trainX = trainData.drop(['orderType'], axis=1)
    trainY = trainData['orderType']
    # 开始交叉验证
    setNa = -9999999999999999999
    inputParam = {
            'eta': 0.05,
            'naData': setNa,
            'scale_pos_weight': 0.2,
            'max_depth': 8,
            'subsample': 0.5,
            'col_sample_bytree': 0.3,
            'min_child_weight': 5,
            'num_roud': 300,
            'objective': 'reg:linear',
            }
    xgboost = few_model.Xgboost(inputParam)
    # xgboost.cv(trainX, trainY)
    # 开始训练
    xgboost.train(trainX, trainY, modelSavePath)
    # 预测
    predict(modelSavePath, xgboost)
