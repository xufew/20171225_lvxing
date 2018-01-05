# =======================
# -*- coding: utf-8 -*-
# author: LONGFEI XU
# Try your best
# ============
import sys
import json

import pandas as pd


def read_userDic(actionPath):
    with open(actionPath, 'rb') as fileReader:
        count = 0
        userDic = {}
        while True:
            stringLine = fileReader.readline()
            if stringLine:
                count += 1
                if count == 1:
                    continue
                stringList = stringLine.strip().decode('utf8').split(',')
                userId = stringList[0]
                actionType = stringList[1]
                actionTime = stringList[2]
                if userId not in userDic:
                    userDic[userId] = {}
                userDic[userId][actionTime] = actionType
            else:
                break
    return userDic


def write_feature_name(fileWriter):
    featureList = [
            'userid',
            'justType1',
            'justType2',
            'justType3',
            'justType4',
            'justType6',
            'go9Dis',
            'go9Time',
            'continueMin1',
            'continueMin2',
            'continueMin3',
            'continueMin4',
            'continueMin5',
            'continueMin6',
            'continueMin7',
            'continueMin8',
            'continueMin9',
            'continueMax1',
            'continueMax2',
            'continueMax3',
            'continueMax4',
            'continueMax5',
            'continueMax6',
            'continueMax7',
            'continueMax8',
            'continueMax9',
            ]
    fileWriter.write(
            '{}\n'.format(','.join(featureList)).encode('utf8')
            )


def continue_dic():
    '''
    统计连续相同type的相关信息
    '''
    outDic = {
            '1': [],
            '2': [],
            '3': [],
            '4': [],
            '5': [],
            '6': [],
            '7': [],
            '8': [],
            '9': [],
            }
    return outDic


def continue_return_value(useType, valueType, valueDic):
    valueList = valueDic[useType]
    if len(valueList) == 0:
        return ''
    else:
        if valueType == 'min':
            outValue = min(valueList)
        elif valueType == 'max':
            outValue = max(valueList)
        return outValue


if __name__ == '__main__':
    actionPath = sys.argv[1]
    outPath = sys.argv[2]
    fileWriter = open(outPath, 'wb')
    # 读取全部信息
    userDic = read_userDic(actionPath)
    # 写feature名
    write_feature_name(fileWriter)
    # 进行feature统计
    count = 0
    for userId in userDic:
        count += 1
        if count % 1000 == 0:
            print(count)
        valueDic = userDic[userId]
        timeSort = sorted(valueDic)
        # 只包含一些特殊
        justType1 = 0
        justType2 = 0
        justType3 = 0
        justType4 = 0
        justType6 = 0
        if len(valueDic) == 1:
            useTime = list(valueDic.keys())[0]
            hasType = valueDic[useTime]
            if hasType == '1':
                justType1 = 1
            if hasType == '2':
                justType2 = 1
            if hasType == '3':
                justType3 = 1
            if hasType == '4':
                justType4 = 1
            if hasType == '6':
                justType6 = 1
        # 进行一次循环的统计
        totalNum = len(timeSort)
        go9Dis = 0
        go9Time = 0
        go9DisList = []
        go9TimeList = []
        continueDic = continue_dic()
        for i, thisTime in enumerate(timeSort):
            thisType = valueDic[thisTime]
            con1 = thisType == '9'
            con2 = i == totalNum-1
            con3 = i < totalNum-1
            go9Dis += 1
            if con3:
                go9Time += int(timeSort[i+1])-int(timeSort[i])
            if con1 or con2:
                go9DisList.append(go9Dis)
                go9TimeList.append(go9Time/float(go9Dis))
                go9Dis = 0
                go9Time = 0
            if con3:
                nextType = valueDic[timeSort[i+1]]
                if nextType == thisType:
                    continueDic[nextType].append(
                            int(timeSort[i+1])-int(timeSort[i])
                            )
        # 储存
        outList = [
                userId,
                str(justType1),
                str(justType2),
                str(justType3),
                str(justType4),
                str(justType6),
                str(max(go9DisList)),
                str(max(go9TimeList)),
                str(continue_return_value('1', 'min', continueDic)),
                str(continue_return_value('2', 'min', continueDic)),
                str(continue_return_value('3', 'min', continueDic)),
                str(continue_return_value('4', 'min', continueDic)),
                str(continue_return_value('5', 'min', continueDic)),
                str(continue_return_value('6', 'min', continueDic)),
                str(continue_return_value('7', 'min', continueDic)),
                str(continue_return_value('8', 'min', continueDic)),
                str(continue_return_value('9', 'min', continueDic)),
                str(continue_return_value('1', 'max', continueDic)),
                str(continue_return_value('2', 'max', continueDic)),
                str(continue_return_value('3', 'max', continueDic)),
                str(continue_return_value('4', 'max', continueDic)),
                str(continue_return_value('5', 'max', continueDic)),
                str(continue_return_value('6', 'max', continueDic)),
                str(continue_return_value('7', 'max', continueDic)),
                str(continue_return_value('8', 'max', continueDic)),
                str(continue_return_value('9', 'max', continueDic)),
                ]
        fileWriter.write(
                '{}\n'.format(','.join(outList)).encode('utf8')
                )
