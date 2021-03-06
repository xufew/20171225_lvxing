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


def predict(modelSavePath, gbdt, naProducer):
    inputPath = Config.TEST_DATA_PATH
    savePath = './data/tmp_result.csv'
    comparePath = Config.RESULT_FINAL_TRANS
    finalPath = Config.RESULT_GBDT
    testX = pd.read_table(inputPath, sep=',', index_col=0)
    testX = testX.apply(
            lambda x: x.fillna(naProducer.get())
            )
    with open(modelSavePath, 'rb') as fileReader:
        rfModel = pickle.load(fileReader)
    predictValue = gbdt.predict(rfModel, testX)
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
    modelPath = Config.MODEL_GBDT
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
            'n_estimators': 300,
            'learning_rate': 0.1,
            'subsample': 0.8,
            'max_features': 0.4,
            'min_samples_split': 20,
            'min_samples_leaf': 5,
            'max_depth': 5,
            'n_jobs_cv': 1,
            'verbose': 1,
            'nfold': 5,
            'scoring': 'roc_auc',
            }
    gbdt = few_model.GBDT(param)
    # gbdt.cv(trainX, trainY)
    # gbdt.line_search(trainX, trainY)
    gbdt.train(trainX, trainY, modelPath)
    predict(modelPath, gbdt, naProducer)
