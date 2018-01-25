# =======================
# -*- coding: utf-8 -*-
# author: LONGFEI XU
# Try your best
# ============
import os
import pickle

import pandas as pd

import Config
import few_model


def predict(modelSavePath, rf, naProducer):
    inputPath = Config.TEST_DATA_PATH
    savePath = './data/tmp_result.csv'
    comparePath = Config.RESULT_FINAL_TRANS
    finalPath = Config.RESULT_RF
    testX = pd.read_table(inputPath, sep=',', index_col=0)
    testX = testX.drop(['orderType'], axis=1)
    testX = testX.apply(
            lambda x: x.fillna(naProducer.get())
            )
    with open(modelSavePath, 'rb') as fileReader:
        rfModel = pickle.load(fileReader)
    predictValue = rf.predict(rfModel, testX)
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
    modelPath = Config.MODEL_RF
    trainData = pd.read_table(inputPath, sep=',', index_col=0)
    # 删除无用纬度和数据
    trainX = trainData.drop(['orderType'], axis=1)
    trainY = trainData['orderType']
    # 处理空缺值
    naProducer = few_model.Preprocessor.NaProducer()
    trainX = trainX.apply(
            lambda x: x.fillna(naProducer.produce(x, 1, 0))
            )
    param = {
            'n_estimators': 700,
            'criterion': 'gini',
            'max_features': 'auto',
            'max_depth': None,
            'min_samples_split': 2,
            'min_samples_leaf': 2,
            'min_weight_fraction_leaf': 0,
            'n_jobs': 4,
            'verbose': 1,
            }
    rf = few_model.RF(param)
    # rf.cv(trainX, trainY)
    rf.line_search(trainX, trainY)
    # rf.train(trainX, trainY, modelPath)
    # predict(modelPath, rf, naProducer)
