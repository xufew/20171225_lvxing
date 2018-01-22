# =======================
# -*- coding: utf-8 -*-
# author: LONGFEI XU
# Try your best
# ============
import os
import pickle

import numpy as np
import pandas as pd
from sklearn.model_selection import KFold

import few_model
import Config


class Lightgbm_c:
    def __init__(self):
        params = {
                'learning_rate': 0.05,
                'num_leaves': 70,
                'num_trees': 370,
                'min_sum_hessian_in_leaf': 0.1,
                'min_data_in_leaf': 50,
                'feature_fraction': 0.3,
                'bagging_fraction': 0.5,
                'lambda_l1': 0,
                'lambda_l2': 10,
                'num_threads': 4,
                }
        self.params = few_model.Lightgbm.set_param(params)
        self.modelpath = './model/tmp_lightgbmc.pkl'

    def cv(self, trainX, trainY):
        few_model.Lightgbm.cv(trainX, trainY, self.params)

    def train(self, trainX, trainY):
        few_model.Lightgbm.train(
                trainX, trainY, self.params, self.modelpath
                )

    def predict(self, testX):
        with open(self.modelpath, 'rb') as fileReader:
            model = pickle.load(fileReader)
        predictValue = few_model.Lightgbm.predict(testX, model)
        return predictValue


class Xgboost_c:
    def __init__(self):
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
        self.model = few_model.Xgboost(inputParam)
        self.modelpath = './model/tmp_xgboostc.pkl'

    def cv(self, trainX, trainY):
        trainX = trainX.fillna(self.param['naData'])
        self.model.cv(trainX, trainY)

    def train(self, trainX, trainY):
        self.model.train(trainX, trainY, self.modelpath)

    def predict(self, testX):
        with open(self.modelpath, 'rb') as fileReader:
            model = pickle.load(fileReader)
        predictValue = self.model.predict(testX, model)
        return predictValue


class RF:
    def __init__(self, trainX):
        param = {
                'n_estimators': 300,
                'criterion': 'gini',
                'max_features': 'auto',
                'max_depth': None,
                'min_samples_split': 15,
                'min_samples_leaf': 5,
                'min_weight_fraction_leaf': 0,
                'n_jobs': 4,
                'verbose': 1,
                }
        self.model = few_model.RF(param)
        self.naProducer = few_model.Preprocessor.NaProducer()
        self.modelpath = './model/tmp_rf.pkl'
        trainX = trainX.apply(
                lambda x: x.fillna(self.naProducer.produce(x, 1, 0))
                )

    def cv(self, trainX, trainY):
        trainX = trainX.apply(
                lambda x: x.fillna(self.naProducer.get())
                )
        self.model.cv(trainX, trainY)

    def train(self, trainX, trainY):
        trainX = trainX.apply(
                lambda x: x.fillna(self.naProducer.get())
                )
        self.model.train(trainX, trainY, self.modelpath)

    def predict(self, testX):
        with open(self.modelpath, 'rb') as fileReader:
            model = pickle.load(fileReader)
        testX = testX.apply(
                lambda x: x.fillna(self.naProducer.get())
                )
        predictValue = self.model.predict(model, testX)
        return predictValue


def predict_up(lr):
    # 进行结果拼接
    reLightgbmC = pd.read_table(Config.RESULT_LIGHTGBM_CL, sep=',')
    reXgboostC = pd.read_table(Config.RESULT_XGBOOST_C, sep=',')
    reList = [reLightgbmC, reXgboostC]
    predictX = []
    for result in reList:
        if len(predictX) == 0:
            predictX = result
        else:
            predictX = pd.merge(
                    predictX, result, how='outer',
                    left_on='userid', right_on='userid'
                    )
    predictX = predictX.set_index('userid')
    # 进行预测存储
    predictY = lr.predict(lr.model, predictX)
    predictY = (0.8*predictX.iloc[:, 0] + 0.2*predictX.iloc[:, 1]).values
    with open('./data/tmp_result.csv', 'wb') as fileWriter:
        fileWriter.write('userid,orderType\n'.encode('utf8'))
        for i in range(len(predictX.index)):
            fileWriter.write(
                    '{},{}\n'.format(
                        predictX.index[i], predictY[i]
                        ).encode('utf8')
                    )
    runAwk = "awk -F',' -v OFS=',' '{if(NR==FNR){a[$1]=$2}else{if($1 in a){print $1,a[$1]}}}' %s %s > %s" % (
            './data/tmp_result.csv', Config.RESULT_FINAL_TRANS, Config.RESULT_COMBINE
            )
    os.system(runAwk)


if __name__ == '__main__':
    # 第一次获取
    trainData = pd.read_table(Config.TRAIN_DATA_PATH, sep=',', index_col=0)
    kf = KFold(n_splits=10)
    combineDic = {}
    for train_index, test_index in kf.split(trainData):
        # 获取每次的训练测试数据
        train = trainData.iloc[train_index, :].copy()
        test = trainData.iloc[test_index, :].copy()
        trainX = train.drop(['orderType'], axis=1)
        trainY = train['orderType']
        testX = test.drop(['orderType'], axis=1)
        testY = test['orderType']
        # 初始化模型
        lightgbmC = Lightgbm_c()
        xgboostC = Xgboost_c()
        rf = RF(trainX)
        # 训练模型
        # lightgbmC.cv(trainX, trainY)
        lightgbmC.train(trainX.copy(), trainY)
        # xgboostC.cv(trainX, trainY)
        xgboostC.train(trainX.copy(), trainY)
        # rf.cv(trainX, trainY)
        rf.train(trainX.copy(), trainY)
        # 预测的结果进行拼装，准备进行第二次训练
        predictLightgbmC = lightgbmC.predict(testX)
        predictXgboostC = xgboostC.predict(testX)
        predictRf = rf.predict(testX)
        # 进行拼装
        testTrain = pd.DataFrame(
                np.array(
                    [
                        predictLightgbmC,
                        predictXgboostC,
                        predictRf,
                        ]
                    ).T,
                index=list(testX.index)
                )
        if len(combineDic) == 0:
            combineDic = testTrain
        else:
            combineDic = pd.concat([combineDic, testTrain])
    trainX = combineDic.loc[trainData.index, :]
    trainY = trainData['orderType']
    saveX = trainX.copy()
    saveX['orderType'] = trainY
    saveX.to_csv('./model/tmp_combine_train.csv', sep=',')
    # 组合模型训练
    param = {
            'penalty': 'l2',
            'tol': 0.00001,
            'C': 0.1,
            'class_weight': None,
            'solver': 'liblinear',
            'max_iter': 100,
            'multi_class': 'ovr',
            'n_jobs': 1,
            'scoring': 'roc_auc',
            'nfold': 10
            }
    lr = few_model.LR(param)
    lr.cv(trainX, trainY)
    lr.train(trainX, trainY, Config.MODEL_COMBINE)
    # # 进行合并结果的预测
    # predict_up(lr)
