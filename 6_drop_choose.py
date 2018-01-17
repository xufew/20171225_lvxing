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
            '6To5Timemin'
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
                thisTrain, trainY, params, verbose_eval=False
                )
        maxAuc = max(evalDic['auc-mean'])
        if maxAuc > biggestAuc:
            biggestAuc = maxAuc
        else:
            initialList.remove(addFeature)
        logger.info(','.join(initialList))
        logger.info('{},{},{},{}'.format(i, addFeature, maxAuc, biggestAuc))
