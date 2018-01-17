# =======================
# -*- coding: utf-8 -*-
# author: LONGFEI XU
# Try your best
# ============
import pandas as pd

import few_model


def read_data(inputPath):
    data = pd.read_table(inputPath, sep=',', index_col=0)
    return data


def log_square_use(trainData):
    logList = [
            'continueVar5', 'go9Time', 'continueVar1',
            'recent4', '6To10Timemin', 'recentDis4', 'type8Per'
            ]
    logData = trainData.loc[:, logList].copy()
    logData.columns = list(map(lambda x: x+'_log', logList))
    squareList = ['9To10Timemin', '8To10Timemin']
    squareData = trainData.loc[:, squareList].copy()
    squareData.columns = list(map(lambda x: x+'_square', squareList))
    addData = pd.merge(
            logData, squareData, how='outer',
            left_index=True, right_index=True
            )
    trainData = pd.merge(
            trainData, addData, how='outer',
            left_index=True, right_index=True
            )
    trainData = trainData.drop(logList+squareList, axis=1)
    return trainData


def add_mul_one(trainData, colName, useType):
    if useType == 'add':
        initialData = trainData.copy()
        useCol = initialData[colName].copy()
        for thisCol in initialData.columns:
            initialData[thisCol] = initialData[thisCol] + useCol
        initialData = pd.merge(
                trainData, initialData, how='outer',
                left_index=True, right_index=True
                )
        return initialData
    elif useType == 'mul':
        initialData = trainData.copy()
        useCol = initialData[colName].copy()
        for thisCol in initialData.columns:
            initialData[thisCol] = initialData[thisCol] * useCol
        initialData = pd.merge(
                trainData, initialData, how='outer',
                left_index=True, right_index=True
                )
        return initialData


if __name__ == '__main__':
    trainPath = './data/train_use/label_train_drop.csv'
    testPath = './data/test_use/label_test_drop.csv'
    outTrain = './data/train_use/label_train_combine.csv'
    outTest = './data/test_use/label_test_combine.csv'
    modelPath = './tmp_test.pkl'
    #
    trainData = read_data(trainPath)
    trainX = trainData.drop(['orderType'], axis=1)
    trainY = trainData['orderType']
    # 训练相关
    params_1 = {
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
    params = few_model.Lightgbm.set_param(params_1)
    changeData = add_mul_one(trainX, 'type8Per_log', 'add')
    # evalDic = few_model.Lightgbm.cv(
    #         changeData, trainY, params, verbose_eval=True
    #         )
    trainModel = few_model.Lightgbm.train(
            changeData, trainY, params, modelPath
            )
    with open('./tmp_feature_im', 'wb') as fileWriter:
        for thisIndex in trainModel.featureIm.index:
            value = trainModel.featureIm[thisIndex]
            fileWriter.write(
                    '{}\t==={}===\n'.format(thisIndex, value).encode('utf8')
                    )
