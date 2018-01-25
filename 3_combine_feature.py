# =======================
# -*- coding: utf-8 -*-
# author: LONGFEI XU
# Try your best
# ============
import pandas as pd


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
    '''
    读取需要进行加减乘除的纬度
    '''
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


featureList = [
        'orderType', 'typeDismax6', 'recentmin5', '1To6Timemin',
        'type5Per', '5To6Timemin', 'recentmax5',
        '1To1Timemin', 'typeDismin5', '5To1Timemin',
        '6To5Timemin', 'typeDismax6', 'recentmin5', '1To6Timemin',
        'type5Per', '5To6Timemin', 'recentmax5', '1To1Timemin',
        'typeDismin5', '5To1Timemin', '6To5Timemin', '女',
        'orderNum', 'superNum', 'superPer', 'cityPer', 'recent6',
        'recent7', 'recent8', 'recentDis1', 'recentDis2', 'recentDis3',
        'recentDis4', 'recentDis5', 'recentDis6', 'recentDis7',
        'recentVar1', 'recentVar2', 'recentVar5', 'recentVar7',
        'recentVar8', 'recentAv1', 'lastType6_add_recentmin1',
        'lastType6_add_typeDismax5', 'lastType6_add_typeDismin6',
        'lastType6_add_recent1', 'lastType6_add_typeDismin5',
        'lastType6_add_5To6Timemin', 'lastType6_add_type6Per',
        'lastType6_add_continueAv5', 'lastType6_add_continueMax6',
        'lastType6_add_6To1Timemin', 'lastType6_add_6To6Timemax',
        'lastType6_add_6To1Timemax', 'lastType6_add_typeDismax7',
        'lastType6_add_居民消费价格指数(上年同月=100)_2017年11月',
        'lastType6_add_6To5Timemax',
        'lastType6_add_商品零售价格指数(上年同月=100)_2017年11月',
        'lastType6_add_typeDismin7', 'lastType6_add_specialLen',
        'lastType6_add_continueVar6', 'lastType6_add_1To2Timemin',
        'lastType6_add_1To1Timemax', 'lastType6_add_国内生产总值(亿元)_2014年',
        'lastType6_add_recentVar5', 'lastType6_add_1To5Timemax',
        'lastType6_add_社会商品零售总额(亿元)_2015年',
        'lastType6_add_5To10Timemin', 'lastType6_add_recentmin4',
        'recentDis10_add_recent10', 'recentDis10_add_recentDis1',
        'orderNum_add_recentmin5', 'orderNum_add_recentmax6',
        'orderNum_add_5To10Timemin', 'orderNum_add_5To6Timemin',
        'orderNum_add_countryPer', 'orderNum_add_type8Per',
        'orderNum_add_6To10Timemax', 'orderNum_add_recentmin4',
        'cityPer_add_recentVar8', '男', '重庆', 'lastThreeType5',
        'lastThreeType6', '4To5Timemax', 'continueVar3',
        'nearSuper_add_type6Per', 'simplePer_add_recentDis1',
        'simpleNum_add_recentmin9', 'lastType6_add_go9Time',
        'recentDis1_mul_continueMin6', 'recentDis1_mul_recent5',
        'finalTypeDate1', 'finalTypeDate3', 'finalTypeDate4',
        'finalTypeDate5', 'finalTypeDate6', 'finalTypeDate8',
        'finalTypeDate9',
        ]


if __name__ == '__main__':
    trainPath = './data/train_use/label_train_drop.csv'
    testPath = './data/test_use/label_test_drop.csv'
    outTrain = './data/train_use/label_train_select.csv'
    outTest = './data/test_use/label_test_select.csv'
    # 处理训练数据
    trainData = read_data(trainPath)
    trainData = log_square_use(trainData)
    trainData = add_feature(trainData)
    trainData = trainData.loc[:, featureList]
    trainData.to_csv(outTrain, sep=',')
    # 处理预测数据
    testData = read_data(testPath)
    testData = log_square_use(testData)
    testData = add_feature(testData)
    testData = testData.loc[:, featureList]
    testData = testData.to_csv(outTest, sep=',')
