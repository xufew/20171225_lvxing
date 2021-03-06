# =======================
# -*- coding: utf-8 -*-
# author: LONGFEI XU
# Try your best
# ============
import os

import numpy as np
import pandas as pd

import Config


def take_test_sample():
    '''
    将测试样本中，含有1的最近样本，都提取出来
    '''
    # 将测试样本简单的进行相加
    userIdArray = __get_test_his_sample()
    __write_value(
            Config.USER_PROFILE_TEST, Config.SAMPLE_USER_PROFILE, userIdArray
            )
    __write_value(
            Config.ORDER_HISTORY_TEST, Config.SAMPLE_ORDER_HISTORY, userIdArray
            )
    __write_value(
            Config.USER_COMMENT_TEST, Config.SAMPLE_USER_COMMENT, userIdArray
            )
    __write_value(
            Config.ACTION_TEST, Config.SAMPLE_ACTION, userIdArray
            )
    __write_value(
            '', Config.SAMPLE_LABEL, userIdArray, 1
            )


def combine_sample():
    '''
    将所有提取出来的新样本，结合到原有样本中去
    '''
    __cat_file(
            Config.USER_PROFILE_TRAIN,
            Config.SAMPLE_USER_PROFILE,
            Config.ALL_USER_PROFILE
            )
    __cat_file(
            Config.ORDER_HISTORY_TRAIN,
            Config.SAMPLE_ORDER_HISTORY,
            Config.ALL_ORDER_HISTORY
            )
    __cat_file(
            Config.USER_COMMENT_TRAIN,
            Config.SAMPLE_USER_COMMENT,
            Config.ALL_USER_COMMENT
            )
    __cat_file(
            Config.ACTION_TRAIN,
            Config.SAMPLE_ACTION,
            Config.ALL_ACTION
            )
    __cat_file(
            Config.LABEL_TRAIN,
            Config.SAMPLE_LABEL,
            Config.ALL_LABEL
            )


def __get_test_his_sample():
    labelData = pd.read_table(Config.ORDER_HISTORY_TEST, sep=',')
    labelUser = labelData.loc[labelData.orderType == 1, :].userid
    outArray = np.unique(labelUser)
    return list(outArray)


def __write_value(fileIn, fileOut, userIdArray, writeLabel=0):
    if writeLabel:
        with open(fileOut, 'wb') as fileWriter:
            for userid in userIdArray:
                fileWriter.write(
                        '{},{}\n'.format(
                            userid, 1
                            ).encode('utf8')
                        )
        return 1
    with open(fileIn, 'rb') as fileReader:
        with open(fileOut, 'wb') as fileWriter:
            count = 0
            while True:
                stringLine = fileReader.readline()
                if stringLine:
                    count += 1
                    if count == 1:
                        continue
                    else:
                        userid = stringLine.decode('utf8').split(',')[0]
                        if int(userid) in userIdArray:
                            fileWriter.write(stringLine)
                else:
                    break


def __cat_file(inputFile1, inputFile2, outFile):
    runSh = 'cat {} {} > {}'.format(
            inputFile1, inputFile2, outFile
            )
    os.system(runSh)


def __type_1_place(hisPath, idStart='987654321', addData=[]):
    '''
    记录购买精品订单1的节点，用来制造训练集
    '''
    with open(hisPath, 'rb') as fileReader:
        count = 0
        userDic = {}
        skipDic = {}
        labelDic = {}
        while True:
            stringLine = fileReader.readline()
            if stringLine:
                count += 1
                if count == 1:
                    continue
                stringList = stringLine.decode('utf8').split(',')
                userid = stringList[0]
                orderTime = int(stringList[2])
                orderType = stringList[3]
                con1 = orderType == '1'
                # con2 = int(userid) in addData
                if con1:
                    if userid not in userDic:
                        userDic[userid] = {}
                        skipDic[userid] = []
                    if orderTime not in skipDic[userid]:
                        userDic[userid][
                                '{}{}'.format(idStart, count)
                                ] = orderTime
                        skipDic[userid].append(orderTime)
                        labelDic[
                                '{}{}'.format(idStart, count)
                                ] = orderType
                    else:
                        continue
            else:
                break
    return userDic, labelDic


def __trans_action(userDic, inputPath, outPath):
    '''
    转换action模块
    '''
    with open(inputPath, 'rb') as fileReader:
        with open(outPath, 'a') as fileWriter:
            count = 0
            while True:
                stringLine = fileReader.readline()
                if stringLine:
                    count += 1
                    if count == 1:
                        continue
                    stringList = stringLine.decode('utf8').split(',')
                    userid = stringList[0]
                    actionTime = int(stringList[2].strip())
                    if userid in userDic:
                        transDic = userDic[userid]
                        for transId in transDic:
                            transTime = transDic[transId]
                            if actionTime < transTime:
                                newList = stringList.copy()
                                newList[0] = transId
                                fileWriter.write(
                                        ','.join(newList)
                                        )
                else:
                    break


def __trans_label(labelDic, outPath):
    '''
    转换标签
    '''
    with open(outPath, 'a') as fileWriter:
        for userid in labelDic:
            fileWriter.write(
                    '{},{}\n'.format(userid, labelDic[userid])
                     )


def __trans_user_profile(userDic, inputPath, outPath):
    '''
    转换用户属性
    '''
    with open(inputPath, 'rb') as fileReader:
        with open(outPath, 'a') as fileWriter:
            count = 0
            while True:
                stringLine = fileReader.readline()
                if stringLine:
                    count += 1
                    if count == 1:
                        continue
                    stringList = stringLine.decode('utf8').split(',')
                    userid = stringList[0]
                    if userid in userDic:
                        transDic = userDic[userid]
                        for transId in transDic:
                            newList = stringList.copy()
                            newList[3] = newList[3].strip()
                            newList.append(transId+'\n')
                            fileWriter.write(
                                    ','.join(newList)
                                    )
                else:
                    break


def __trans_order_his(userDic, inputPath, outPath):
    with open(inputPath, 'rb') as fileReader:
        with open(outPath, 'a') as fileWriter:
            count = 0
            while True:
                stringLine = fileReader.readline()
                if stringLine:
                    count += 1
                    if count == 1:
                        continue
                    stringList = stringLine.decode('utf8').split(',')
                    userid = stringList[0]
                    actionTime = int(stringList[2].strip())
                    if userid in userDic:
                        transDic = userDic[userid]
                        for transId in transDic:
                            transTime = transDic[transId]
                            if actionTime < transTime:
                                newList = stringList.copy()
                                newList[0] = transId
                                fileWriter.write(
                                        ','.join(newList)
                                        )
                else:
                    break


def __trans_user_comment(userDic, inputPath, outPath, idTimeDic):
    with open(inputPath, 'rb') as fileReader:
        with open(outPath, 'a') as fileWriter:
            count = 0
            while True:
                stringLine = fileReader.readline()
                if stringLine:
                    count += 1
                    if count == 1:
                        continue
                    stringList = stringLine.decode('utf8').split(',')
                    userid = stringList[0]
                    orderId = stringList[1]
                    if orderId not in idTimeDic:
                        continue
                    actionTime = int(idTimeDic[orderId])
                    if userid in userDic:
                        transDic = userDic[userid]
                        for transId in transDic:
                            transTime = transDic[transId]
                            if actionTime < transTime:
                                newList = stringList.copy()
                                newList[0] = transId
                                fileWriter.write(
                                        ','.join(newList)
                                        )
                else:
                    break


def read_id_time(userHisPath):
    '''
    读取订单id的时间
    '''
    outDic = {}
    with open(userHisPath, 'r') as fileReader:
        count = 0
        while True:
            count += 1
            if count == 1:
                continue
            stringLine = fileReader.readline()
            if stringLine:
                stringList = stringLine.split(',')
                orderid = stringList[1]
                time = stringList[2]
                outDic[orderid] = time
            else:
                break
    return outDic


if __name__ == '__main__':
    # 测试样本转为训练样本
    take_test_sample()
    # 提取已经发生的样本,训练
    hisData = pd.read_table(Config.ORDER_HISTORY_TRAIN, sep=',')
    futureData = pd.read_table(Config.LABEL_TRAIN, sep=',', index_col=0)
    hisData = hisData.groupby('userid').sum()
    hisData = hisData.loc[hisData.orderType == 0, :]
    addData = futureData.loc[hisData.index, :]
    addData = list(addData[np.array((addData == 0).values)].index)
    userDic, labelDic = __type_1_place(
            Config.ORDER_HISTORY_TRAIN, '987654321', addData
            )
    __trans_action(userDic, Config.ACTION_TRAIN, Config.SAMPLE_ACTION)
    __trans_label(labelDic, Config.SAMPLE_LABEL)
    __trans_user_profile(
            userDic, Config.USER_PROFILE_TRAIN, Config.SAMPLE_USER_PROFILE
            )
    __trans_order_his(
            userDic, Config.ORDER_HISTORY_TRAIN, Config.SAMPLE_ORDER_HISTORY
            )
    idTimeDic = read_id_time(Config.ORDER_HISTORY_TRAIN)
    __trans_user_comment(
            userDic, Config.USER_COMMENT_TRAIN, Config.SAMPLE_USER_COMMENT,
            idTimeDic
            )
    # 提取已经发生的样本,测试
    userDic, labelDic = __type_1_place(
            Config.ORDER_HISTORY_TEST, '87654321', addData
            )
    __trans_action(userDic, Config.ACTION_TEST, Config.SAMPLE_ACTION)
    __trans_label(labelDic, Config.SAMPLE_LABEL)
    __trans_user_profile(
            userDic, Config.USER_PROFILE_TEST, Config.SAMPLE_USER_PROFILE
            )
    __trans_order_his(
            userDic, Config.ORDER_HISTORY_TEST, Config.SAMPLE_ORDER_HISTORY
            )
    idTimeDic = read_id_time(Config.ORDER_HISTORY_TEST)
    __trans_user_comment(
            userDic, Config.USER_COMMENT_TEST, Config.SAMPLE_USER_COMMENT,
            idTimeDic
            )
    # 将新老样本进行拼接
    combine_sample()
