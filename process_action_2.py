# =======================
# -*- coding: utf-8 -*-
# author: LONGFEI XU
# Try your best
# ============
import pickle
import sys
from copy import deepcopy


def write_feature_name(fileWriter, pathCountDic, pathCountName):
    pathString = ''
    for thisPath in pathCountName:
        pathString += '{},'.format(thisPath+'countNum')
        pathString += '{},'.format(thisPath+'startTime')
        pathString += '{},'.format(thisPath+'endTime')
        pathString += '{},'.format(thisPath+'range')
    pathString = pathString[:-1]
    featureList = [
            'userid',
            pathString,
            ]
    fileWriter.write(
            '{}\n'.format(','.join(featureList)).encode('utf8')
            )


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


def if_in(value, valueList):
    if value in valueList:
        return 1
    else:
        return 0


if __name__ == '__main__':
    actionPath = sys.argv[1]
    outPath = sys.argv[2]
    fileWriter = open(outPath, 'wb')
    # 统计路径
    userDic = read_userDic(actionPath)
    # 读取需要统计的path路径
    pathCountList = pickle.load(open('./count_path.pkl', 'rb'))
    pathCountDic = {}
    for thisPath in pathCountList:
        pathCountDic[thisPath] = {
                'startTime': '',
                'endTime': '',
                'countNum': 0,
                'range': '',
                }
    pathCountName = pathCountDic.keys()
    # 写列名
    write_feature_name(fileWriter, pathCountDic, pathCountName)
    # 开始进行统计
    count = 0
    for userId in userDic:
        count += 1
        if count % 1000 == 0:
            print(count)
        valueDic = userDic[userId]
        timeSort = sorted(valueDic)
        valueList = list(map(lambda x, y=valueDic: valueDic[x], timeSort))
        userPathCount = deepcopy(pathCountDic)
        # 开始进行路径开始结束时间，和路径结束时间，次数统计
        for i in range(len(timeSort)-1):
            pathString = '{}'.format(valueList[i])
            startDate = timeSort[i]
            for j in range(i+1, len(timeSort)):
                if j-i > 8:
                    break
                pathString += '->{}'.format(valueList[j])
                endDate = timeSort[j]
                if pathString in userPathCount:
                    userPathCount[pathString]['countNum'] += 1
                    userPathCount[pathString]['startTime'] = startDate
                    userPathCount[pathString]['endTime'] = endDate
                    userPathCount[pathString]['range'] = \
                        int(endDate)-int(startDate)
        pathString = ''
        for thisPath in pathCountName:
            pathString += '{},'.format(userPathCount[thisPath]['countNum'])
            pathString += '{},'.format(userPathCount[thisPath]['startTime'])
            pathString += '{},'.format(userPathCount[thisPath]['endTime'])
            pathString += '{},'.format(userPathCount[thisPath]['range'])
        pathString = pathString[:-1]
        # 进行结果综合
        outList = [
                userId,
                pathString
                ]
        fileWriter.write(
                '{}\n'.format(','.join(outList)).encode('utf8')
                )
