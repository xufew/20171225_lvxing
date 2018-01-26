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


lightgbm_c_path = './model/tmp_lightgbmc.pkl'
lightgbm_r_path = './model/tmp_lightgbmr.pkl'
xgboost_c_path = './model/tmp_xgboostc.pkl'


def get_lightgbm_c():
    lightgbm_c_param = {
            'learning_rate': 0.05,
            'num_leaves': 60,
            'num_trees': 470,
            'min_sum_hessian_in_leaf': 0.2,
            'min_data_in_leaf': 70,
            'bagging_fraction': 0.5,
            'feature_fraction': 0.3,
            'lambda_l1': 0,
            'lambda_l2': 11.88,
            'num_threads': 4,
            'scale_pos_weight': 1,
            'application': 'binary',
            }
    lightgbm_c = few_model.Lightgbm(lightgbm_c_param)
    return lightgbm_c


def get_lightgbm_r():
    lightgbm_r_param = {
            'learning_rate': 0.05,
            'num_leaves': 50,
            'num_trees': 420,
            'min_sum_hessian_in_leaf': 0.0575,
            'min_data_in_leaf': 50,
            'bagging_fraction': 0.3,
            'feature_fraction': 0.5,
            'lambda_l1': 0,
            'lambda_l2': 39.11,
            'num_threads': 4,
            'scale_pos_weight': 1,
            'application': 'regression',
            }
    lightgbm_r = few_model.Lightgbm(lightgbm_r_param)
    return lightgbm_r


def get_xgboost_c():
    xgboost_c_param = {
            'eta': 0.05,
            'naData': -9999999,
            'scale_pos_weight': 1,
            'max_depth': 6,
            'subsample': 0.5,
            'col_sample_bytree': 0.4,
            'min_child_weight': 1,
            'reg_lambda': 13.25,
            'num_roud': 700,
            'objective': 'binary:logistic',
            }
    xgboost_c = few_model.Xgboost(xgboost_c_param)
    return xgboost_c


class RF:
    def __init__(self, trainX):
        param = {
                'n_estimators': 1000,
                'criterion': 'gini',
                'max_features': 'auto',
                'max_depth': None,
                'min_samples_split': 10,
                'min_samples_leaf': 2,
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


class GBDT:
    def __init__(self, trainX):
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
        self.model = few_model.GBDT(param)
        self.naProducer = few_model.Preprocessor.NaProducer()
        self.modelpath = './model/tmp_gbdt.pkl'
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


class ExtraTree:
    def __init__(self, trainX):
        param = {
                'n_estimators': 700,
                'criterion': 'gini',
                'max_features': 'auto',
                'max_depth': None,
                'min_samples_split': 10,
                'min_samples_leaf': 2,
                'min_weight_fraction_leaf': 0,
                'n_jobs': 4,
                'verbose': 1,
                }
        self.model = few_model.ExtraTree(param)
        self.naProducer = few_model.Preprocessor.NaProducer()
        self.modelpath = './model/tmp_extratree.pkl'
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


class AdaBoost:
    def __init__(self, trainX):
        param = {
                'n_estimators': 230,
                'learning_rate': 0.5,
                'algorithm': 'SAMME.R',
                'n_jobs_cv': 1,
                'nfold': 5,
                'scoring': 'roc_auc',
                }
        self.model = few_model.AdaBoost(param)
        self.naProducer = few_model.Preprocessor.NaProducer()
        self.modelpath = './model/tmp_adaboost.pkl'
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


def load_model(modelPath):
    with open(modelPath, 'rb') as fileReader:
        model = pickle.load(fileReader)
    return model


if __name__ == '__main__':
    # 第一次获取
    trainData = pd.read_table(Config.TRAIN_DATA_PATH, sep=',', index_col=0)
    kf = KFold(n_splits=5)
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
        lightgbm_c = get_lightgbm_c()
        lightgbm_r = get_lightgbm_r()
        xgboost_c = get_xgboost_c()
        rf = RF(trainX)
        extratree = ExtraTree(trainX)
        adaboost = AdaBoost(trainX)
        gbdt = GBDT(trainX)
        # 训练模型
        lightgbm_c.train(trainX.copy(), trainY, lightgbm_c_path)
        lightgbm_r.train(trainX.copy(), trainY, lightgbm_r_path)
        xgboost_c.train(trainX.copy(), trainY, xgboost_c_path)
        rf.train(trainX.copy(), trainY)
        extratree.train(trainX.copy(), trainY)
        adaboost.train(trainX.copy(), trainY)
        gbdt.train(trainX.copy(), trainY)
        # 预测的结果进行拼装，准备进行第二次训练
        predictLightgbmC = lightgbm_c.predict(
                testX, load_model(lightgbm_c_path)
                )
        predictLightgbmR = lightgbm_r.predict(
                testX, load_model(lightgbm_r_path)
                )
        predictXgboostC = xgboost_c.predict(testX, load_model(xgboost_c_path))
        predictRf = rf.predict(testX)
        predictExtratree = extratree.predict(testX)
        predictAdaboost = adaboost.predict(testX)
        predictGbdt = gbdt.predict(testX)
        # 进行拼装
        testTrain = pd.DataFrame(
                np.array(
                    [
                        predictLightgbmC,
                        predictLightgbmR,
                        predictXgboostC,
                        predictRf,
                        predictExtratree,
                        predictAdaboost,
                        predictGbdt,
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
    # # 组合模型训练
    # trainData = pd.read_table('./model/tmp_combine_train.csv', sep=',', index_col=0)
    # trainX = trainData.drop(['orderType'], axis=1)
    # trainY = trainData['orderType']
    # # param = {
    # #         'penalty': 'l2',
    # #         'tol': 0.00001,
    # #         'C': 0.1,
    # #         'class_weight': None,
    # #         'solver': 'liblinear',
    # #         'max_iter': 100,
    # #         'multi_class': 'ovr',
    # #         'n_jobs': 1,
    # #         'scoring': 'roc_auc',
    # #         'nfold': 10
    # #         }
    # # lr = few_model.LR(param)
    # # lr.cv(trainX, trainY)
    # # lr.train(trainX, trainY, Config.MODEL_COMBINE)
    # params = {
    #         'learning_rate': 0.001,
    #         'num_leaves': 3,
    #         'num_trees': 20000,
    #         # 'min_sum_hessian_in_leaf': 0.2,
    #         # 'min_data_in_leaf': 1,
    #         # 'bagging_fraction': 0.5,
    #         'lambda_l1': 0,
    #         'lambda_l2': 0,
    #         'num_threads': 4,
    #         'scale_pos_weight': 1,
    #         'application': 'binary',
    #         }
    # lightgbm = few_model.Lightgbm(params)
    # evalDic = lightgbm.cv(trainX, trainY)
    # # 进行合并结果的预测
    # predict_up(lr)
