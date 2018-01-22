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
    return trainData


def input_dic():
    addDic = {}
    mulDic = {}
    with open('./logger_combine.log', 'rb') as fileReader:
        while True:
            stringLine = fileReader.readline()
            if stringLine:
                stringList = stringLine.strip().decode('utf8').split('\t')
                orFeature = stringList[0]
                comebineFeature = stringList[1]
                useType = stringList[2]
                if useType == 'add':
                    if orFeature not in addDic:
                        addDic[orFeature] = []
                    addDic[orFeature].append(comebineFeature)
                elif useType == 'mul':
                    if orFeature not in mulDic:
                        mulDic[orFeature] = []
                    mulDic[orFeature].append(comebineFeature)
            else:
                break
    return addDic, mulDic


def add_feature(inputData):
    '''
    将字典相关的feture进行对应的运算，加入到原始data里面
    '''
    orData = inputData.copy()
    addDic, mulDic = input_dic()
    for orFeature in addDic:
        addFrame = inputData.loc[:, addDic[orFeature]].copy()
        for thisCol in addFrame.columns:
            addFrame[thisCol] = addFrame[thisCol] + inputData[orFeature]
        addFrame.columns = list(
                map(
                    lambda x, y=orFeature: '{}_add_{}'.format(orFeature, x),
                    addFrame.columns
                    )
                )
        orData = pd.merge(
                orData, addFrame, how='outer',
                left_index=True, right_index=True
                )
    for orFeature in mulDic:
        addFrame = inputData.loc[:, mulDic[orFeature]].copy()
        for thisCol in addFrame.columns:
            addFrame[thisCol] = addFrame[thisCol] * inputData[orFeature]
        addFrame.columns = list(
                map(
                    lambda x, y=orFeature: '{}_mul_{}'.format(orFeature, x),
                    addFrame.columns
                    )
                )
        orData = pd.merge(
                orData, addFrame, how='outer',
                left_index=True, right_index=True
                )
    return orData


if __name__ == '__main__':
    trainPath = './data/train_use/label_train_drop.csv'
    testPath = './data/test_use/label_test_drop.csv'
    outTrain = './data/train_use/label_train_combine.csv'
    outTest = './data/test_use/label_test_combine.csv'
    modelPath = './tmp_test.pkl'
    # 进行保存
    trainData = read_data(trainPath)
    trainData = log_square_use(trainData)
    trainData = add_feature(trainData)
    trainData.to_csv(outTrain, sep=',')
    # 测试数据处理
    testData = read_data(testPath)
    testData = log_square_use(testData)
    testData = add_feature(testData)
    testData.to_csv(outTest, sep=',')
    # trainX = trainData.drop(['orderType'], axis=1)
    # trainY = trainData['orderType']
    # # 将放在字典里合并纬度，加到数据里
    # trainX = log_square_use(trainX)
    # trainX = add_feature(trainX)
    # # 训练相关
    # params_1 = {
    #         'learning_rate': 0.05,
    #         'num_leaves': 70,
    #         'num_trees': 470,
    #         'min_sum_hessian_in_leaf': 0.1,
    #         'min_data_in_leaf': 50,
    #         'feature_fraction': 0.3,
    #         'bagging_fraction': 0.5,
    #         'lambda_l1': 0,
    #         'lambda_l2': 10,
    #         'num_threads': 4,
    #         }
    # params = few_model.Lightgbm.set_param(params_1)
    # evalDic = few_model.Lightgbm.cv(
    #         trainX, trainY, params, verbose_eval=True
    #         )
