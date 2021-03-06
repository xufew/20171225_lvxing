# =======================
# -*- coding: utf-8 -*-
# author: LONGFEI XU
# Try your best
# ============
import pandas as pd


COLUMN_PER = 1                   # 剔除的列含na量
ROW_PER = 0.9                    # 剔除的行含na量


DELETE_DIC = {
        'row': [],
        'column': []
        }


def read_data(inputPath):
    data = pd.read_table(inputPath, sep=',', index_col=0)
    return data


def delete_na(inputData):
    '''
    去除na过多的数据
    '''
    # 列
    columnNaNum = inputData.isnull().sum()
    columnNaPer = columnNaNum/float(inputData.shape[0])
    deleteCol = list(columnNaPer[columnNaPer >= COLUMN_PER].index)
    DELETE_DIC['column'] += deleteCol
    # 行
    rowNaNum = inputData.isnull().sum(axis=1)
    rowNaPer = rowNaNum/float(inputData.shape[1])
    deleteRow = list(rowNaPer[rowNaPer >= ROW_PER].index)
    DELETE_DIC['row'] += deleteRow
    print(DELETE_DIC)


def drop(inputData, dropType='train'):
    '''
    丢弃数据
    '''
    if dropType == 'train':
        dropCol = inputData.drop(DELETE_DIC['column'], axis=1)
        dropRow = dropCol.drop(DELETE_DIC['row'], axis=0)
        return dropRow
    elif dropType == 'test':
        dropCol = inputData.drop(DELETE_DIC['column'], axis=1)
        return dropCol


if __name__ == '__main__':
    trainPath = './data/train_use/label_train.csv'
    testPath = './data/test_use/label_test.csv'
    outTrain = './data/train_use/label_train_drop.csv'
    outTest = './data/test_use/label_test_drop.csv'
    # 处理na
    trainData = read_data(trainPath)
    DELETE_DIC['row'] += list(
            trainData.loc[trainData.totalAction.isnull(), :].index
            )
    DELETE_DIC['row'] += list(
            trainData.loc[trainData.totalAction > 800, :].index
            )
    DELETE_DIC['column'] += ['totalAction']
    delete_na(trainData)
    trainData = drop(trainData)
    trainData.to_csv(outTrain, sep=',')
    testData = read_data(testPath)
    testData = drop(testData, 'test')
    testData.to_csv(outTest, sep=',')
