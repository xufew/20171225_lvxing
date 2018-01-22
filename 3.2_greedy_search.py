# =======================
# -*- coding: utf-8 -*-
# author: LONGFEI XU
# Try your best
# ============
import pandas as pd

import few_model
import few_base


def read_data(inputPath):
    data = pd.read_table(inputPath, sep=',', index_col=0)
    return data


if __name__ == '__main__':
    trainPath = './data/train_use/label_train_combine.csv'
    trainData = read_data(trainPath)
    trainX = trainData.drop(['orderType'], axis=1)
    trainY = trainData['orderType']
    #
    initialList = [
            'typeDismax6', 'recentmin5', '1To6Timemin',
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
            ]
    initialData = trainX.drop(initialList, axis=1)
    #
    params_1 = {
            'learning_rate': 0.05,
            'num_leaves': 70,
            'num_trees': 700,
            'min_sum_hessian_in_leaf': 0.1,
            'min_data_in_leaf': 50,
            'feature_fraction': 0.3,
            'bagging_fraction': 0.5,
            'lambda_l1': 0,
            'lambda_l2': 10,
            'num_threads': 4,
            }
    addList = ['skipit']+list(initialData.columns)
    biggestAuc = 0
    logger = few_base.Logger('logger_use.log').get_logger()
    for i, addFeature in enumerate(addList):
        if addFeature != 'skipit':
            initialList.append(addFeature)
        thisTrain = trainX.loc[:, initialList]
        params = few_model.Lightgbm.set_param(params_1)
        evalDic = few_model.Lightgbm.cv(
                thisTrain, trainY, params, verbose_eval=True
                )
        maxAuc = max(evalDic['auc-mean'])
        if maxAuc > biggestAuc:
            biggestAuc = maxAuc
        else:
            initialList.remove(addFeature)
        logger.info(','.join(initialList))
        logger.info('{},{},{},{}'.format(i, addFeature, maxAuc, biggestAuc))
