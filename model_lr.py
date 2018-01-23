# =======================
# -*- coding: utf-8 -*-
# author: LONGFEI XU
# Try your best
# ============
import pandas as pd

import Config
import few_model


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
    # 进行标准化处理
    normalizer = few_model.Preprocessor.Normalizer()
    trainX = normalizer.z_score_first(trainX)
    # 开始训练
    param = {
            'penalty': 'l2',
            'tol': 0.00001,
            'C': 100,
            'class_weight': None,
            'solver': 'liblinear',
            'max_iter': 100,
            'multi_class': 'ovr',
            'n_jobs': 1,
            'scoring': 'roc_auc',
            'nfold': 5,
            'verbose': 1,
            }
    lr = few_model.LR(param)
    lr.cv(trainX, trainY)
    # lr.train(trainX, trainY, modelPath)
