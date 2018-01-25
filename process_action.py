# =======================
# -*- coding: utf-8 -*-
# author: LONGFEI XU
# Try your best
# ============
import sys

import numpy as np

import few_model


typeDic = {
        '1': 0,
        '2': 1,
        '3': 2,
        '4': 3,
        '5': 4,
        '6': 5,
        '7': 6,
        '8': 7,
        '9': 8,
        }


def if_value_in(typeNum, valueDic):
    if typeNum in valueDic:
        outValue = valueDic[typeNum]
    else:
        outValue = 0
    return outValue


def if_value_dic(typeNum, valueDic):
    if typeNum in valueDic:
        outValue = valueDic[typeNum]
    else:
        outValue = ''
    return outValue


def if_second_in(typeNum, valueDic, valueName):
    if typeNum in valueDic:
        outValue = valueDic[typeNum][valueName]
    else:
        outValue = ''
    return outValue


def get_recent_dic(valueDic, timeSort):
    '''
    获取每个类别状态:
    距离最近时间的时间差
    最开始的时间差
    '''
    recentDic = {}
    nowTime = int(timeSort[-1])
    firstTime = int(timeSort[0])
    for thisTime in timeSort:
        thisType = valueDic[thisTime]
        rangeTime = nowTime-int(thisTime)
        rangeFirst = int(thisTime)-firstTime
        recentDic[thisType] = {
                'nowTime': rangeTime,
                'firstTime': rangeFirst,
                }
    return recentDic


def get_recent_dis(valueDic, timeSort):
    '''
    离最近的操作距离
    '''
    recentDic = {}
    nowIndex = timeSort.index(timeSort[-1])
    for thisTime in timeSort:
        thisType = valueDic[thisTime]
        thisDis = nowIndex-timeSort.index(thisTime)
        if thisType not in recentDic:
            recentDic[thisType] = thisDis
        else:
            if recentDic[thisType] > thisDis:
                recentDic[thisType] = thisDis
    return recentDic


def get_range(valueDic, timeSort):
    '''
    计算离每个type的平均，方差的时间间隔
    '''
    recentDic = {}
    for thisTime in timeSort:
        thisType = valueDic[thisTime]
        totalRange = 0
        varRange = 0
        comepareNum = 0
        rangeList = []
        for compareTime in timeSort:
            comepareNum += 1
            thisRange = int(compareTime)-int(thisTime)
            totalRange += thisRange
            varRange += pow(int(compareTime)-int(thisTime), 2)
            if thisRange > 0:
                rangeList.append(thisRange)
        if comepareNum-1 > 0:
            avRange = totalRange/float(comepareNum-1)
            varRange = varRange/float(comepareNum-1)
        else:
            avRange = ''
            varRange = ''
        minRange = min(rangeList) if len(rangeList) > 0 else ''
        maxRange = max(rangeList) if len(rangeList) > 0 else ''
        recentDic[thisType] = {
                'av': avRange,
                'var': varRange,
                'min': minRange,
                'max': maxRange,
                }
    return recentDic


def trans_type_to_string(processDic, tranType):
    transList = map(
            lambda x: str(x),
            few_model.Preprocessor.one_hot(processDic, tranType)
            )
    transString = ','.join(transList)
    return transString


def get_hot_name(processDic, addName=''):
    transName = ','.join(
            few_model.Preprocessor.get_one_hot_name(typeDic, addName)
            )
    return transName


def type_to_type():
    '''
    类别到类别之间的统计
    '''
    def get_one():
        oneDic = {
                '1': {'min': '', 'max': '', 'av': '', 'num': 0},
                '2': {'min': '', 'max': '', 'av': '', 'num': 0},
                '3': {'min': '', 'max': '', 'av': '', 'num': 0},
                '4': {'min': '', 'max': '', 'av': '', 'num': 0},
                '5': {'min': '', 'max': '', 'av': '', 'num': 0},
                '6': {'min': '', 'max': '', 'av': '', 'num': 0},
                '7': {'min': '', 'max': '', 'av': '', 'num': 0},
                '8': {'min': '', 'max': '', 'av': '', 'num': 0},
                '9': {'min': '', 'max': '', 'av': '', 'num': 0},
                }
        return oneDic
    outDic = {
            '1': get_one(),
            '2': get_one(),
            '3': get_one(),
            '4': get_one(),
            '5': get_one(),
            '6': get_one(),
            '7': get_one(),
            '8': get_one(),
            '9': get_one(),
            }
    return outDic


if __name__ == '__main__':
    actionPath = sys.argv[1]
    outPath = sys.argv[2]
    fileWriter = open(outPath, 'wb')
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
    typeToTypeName = ''
    for i in range(1, 10):
        i = str(i)
        for j in range(1, 10):
            j = str(j)
            for k in ['min', 'max']:
                typeToTypeName += '{}To{}Time{},'.format(j, i, k)
    typeToTypeName = typeToTypeName.strip(',')
    nameList = [
            'userid',
            get_hot_name(typeDic, 'lastType'),
            'avBrowse',
            'minBrowse',
            'lastBrowse',
            'varBrowse',
            get_hot_name(typeDic, 'firstType'),
            'firstBrowse',
            'browseLastTwo',
            'browseLastThree',
            'browseLastFour',
            get_hot_name(typeDic, 'lastTwoType'),
            get_hot_name(typeDic, 'lastThreeType'),
            'threeAv',
            'threeVar',
            'type1Per',
            'type2Per',
            'type3Per',
            'type4Per',
            'type5Per',
            'type6Per',
            'type7Per',
            'type8Per',
            'type9Per',
            'type1Num',
            'type2Num',
            'type3Num',
            'type4Num',
            'type5Num',
            'type6Num',
            'type7Num',
            'type8Num',
            'type9Num',
            'recent1',
            'recent2',
            'recent3',
            'recent4',
            'recent5',
            'recent6',
            'recent7',
            'recent8',
            'recent9',
            'recentDis1',
            'recentDis2',
            'recentDis3',
            'recentDis4',
            'recentDis5',
            'recentDis6',
            'recentDis7',
            'recentDis8',
            'recentDis9',
            'recentVar1',
            'recentVar2',
            'recentVar3',
            'recentVar4',
            'recentVar5',
            'recentVar6',
            'recentVar7',
            'recentVar8',
            'recentVar9',
            'recentAv1',
            'recentAv2',
            'recentAv3',
            'recentAv4',
            'recentAv5',
            'recentAv6',
            'recentAv7',
            'recentAv8',
            'recentAv9',
            'recentmin1',
            'recentmin2',
            'recentmin3',
            'recentmin4',
            'recentmin5',
            'recentmin6',
            'recentmin7',
            'recentmin8',
            'recentmin9',
            'recentmax1',
            'recentmax2',
            'recentmax3',
            'recentmax4',
            'recentmax5',
            'recentmax6',
            'recentmax7',
            'recentmax8',
            'recentmax9',
            typeToTypeName,
            ]
    fileWriter.write(
            '{}\n'.format(','.join(nameList)).encode('utf8')
            )
    count = 0
    for userId in userDic:
        count += 1
        if count % 1000 == 0:
            print(count)
        valueDic = userDic[userId]
        timeSort = sorted(valueDic)
        # 浏览的最后一个type
        browseLen = len(timeSort)
        lastType = trans_type_to_string(typeDic, valueDic[timeSort[-1]])
        firstType = trans_type_to_string(typeDic, valueDic[timeSort[0]])
        if browseLen >= 2:
            lastTwoType = trans_type_to_string(typeDic, valueDic[timeSort[-2]])
        else:
            lastTwoType = trans_type_to_string(typeDic, '')
        if browseLen >= 3:
            lastThreeType = trans_type_to_string(
                    typeDic, valueDic[timeSort[-3]]
                    )
        else:
            lastThreeType = trans_type_to_string(typeDic, '')
        # 统计间隔时间list
        browseNum = 0
        rangeList = []
        for i in range(browseLen-1):
            browseNum += 1
            rangeList.append(int(timeSort[i+1])-int(timeSort[i]))
        # 提取间隔相关信息
        if browseNum == 0:
            avBrowse = ''
            minBrowse = ''
            lastBrowse = ''
            varBrowse = ''
            firstBrowse = ''
        else:
            avBrowse = sum(rangeList)/float(browseNum)
            minBrowse = min(rangeList)
            lastBrowse = rangeList[-1]
            varBrowse = np.cov(rangeList)
            firstBrowse = rangeList[0]
        if browseNum >= 2:
            browseLastTwo = rangeList[-2]
        else:
            browseLastTwo = ''
        if browseNum >= 3:
            browseLastThree = rangeList[-3]
        else:
            browseLastThree = ''
        if browseNum >= 4:
            browseLastFour = rangeList[-4]
        else:
            browseLastFour = ''
        # 如果操作type比较多，计算最后一段时间
        if browseNum >= 3:
            threeAv = sum(rangeList[-3:])
            threeVar = np.cov(rangeList[-3:])
        else:
            threeAv = ''
            threeVar = ''
        # 点击类型比例
        valueCount = np.unique(list(valueDic.values()), return_counts=True)
        valueCountDic = dict(list(zip(valueCount[0], valueCount[1])))
        totalCount = float(sum(valueCountDic.values()))
        type1Per = if_value_in('1', valueCountDic)/totalCount
        type2Per = if_value_in('2', valueCountDic)/totalCount
        type3Per = if_value_in('3', valueCountDic)/totalCount
        type4Per = if_value_in('4', valueCountDic)/totalCount
        type5Per = if_value_in('5', valueCountDic)/totalCount
        type6Per = if_value_in('6', valueCountDic)/totalCount
        type7Per = if_value_in('7', valueCountDic)/totalCount
        type8Per = if_value_in('8', valueCountDic)/totalCount
        type9Per = if_value_in('9', valueCountDic)/totalCount
        type1Num = if_value_in('1', valueCountDic)
        type2Num = if_value_in('2', valueCountDic)
        type3Num = if_value_in('3', valueCountDic)
        type4Num = if_value_in('4', valueCountDic)
        type5Num = if_value_in('5', valueCountDic)
        type6Num = if_value_in('6', valueCountDic)
        type7Num = if_value_in('7', valueCountDic)
        type8Num = if_value_in('8', valueCountDic)
        type9Num = if_value_in('9', valueCountDic)
        # 离最近的时间
        recentTimeDic = get_recent_dic(valueDic, timeSort)
        recent1 = if_second_in('1', recentTimeDic, 'nowTime')
        recent2 = if_second_in('2', recentTimeDic, 'nowTime')
        recent3 = if_second_in('3', recentTimeDic, 'nowTime')
        recent4 = if_second_in('4', recentTimeDic, 'nowTime')
        recent5 = if_second_in('5', recentTimeDic, 'nowTime')
        recent6 = if_second_in('6', recentTimeDic, 'nowTime')
        recent7 = if_second_in('7', recentTimeDic, 'nowTime')
        recent8 = if_second_in('8', recentTimeDic, 'nowTime')
        recent9 = if_second_in('9', recentTimeDic, 'nowTime')
        # 离最近的距离
        recentDisDic = get_recent_dis(valueDic, timeSort)
        recentDis1 = if_value_dic('1', recentDisDic)
        recentDis2 = if_value_dic('2', recentDisDic)
        recentDis3 = if_value_dic('3', recentDisDic)
        recentDis4 = if_value_dic('4', recentDisDic)
        recentDis5 = if_value_dic('5', recentDisDic)
        recentDis6 = if_value_dic('6', recentDisDic)
        recentDis7 = if_value_dic('7', recentDisDic)
        recentDis8 = if_value_dic('8', recentDisDic)
        recentDis9 = if_value_dic('9', recentDisDic)
        # 方差均值
        recentRangeDic = get_range(valueDic, timeSort)
        recentVar1 = if_second_in('1', recentRangeDic, 'var')
        recentVar2 = if_second_in('2', recentRangeDic, 'var')
        recentVar3 = if_second_in('3', recentRangeDic, 'var')
        recentVar4 = if_second_in('4', recentRangeDic, 'var')
        recentVar5 = if_second_in('5', recentRangeDic, 'var')
        recentVar6 = if_second_in('6', recentRangeDic, 'var')
        recentVar7 = if_second_in('7', recentRangeDic, 'var')
        recentVar8 = if_second_in('8', recentRangeDic, 'var')
        recentVar9 = if_second_in('9', recentRangeDic, 'var')
        recentAv1 = if_second_in('1', recentRangeDic, 'av')
        recentAv2 = if_second_in('2', recentRangeDic, 'av')
        recentAv3 = if_second_in('3', recentRangeDic, 'av')
        recentAv4 = if_second_in('4', recentRangeDic, 'av')
        recentAv5 = if_second_in('5', recentRangeDic, 'av')
        recentAv6 = if_second_in('6', recentRangeDic, 'av')
        recentAv7 = if_second_in('7', recentRangeDic, 'av')
        recentAv8 = if_second_in('8', recentRangeDic, 'av')
        recentAv9 = if_second_in('9', recentRangeDic, 'av')
        recentmin1 = if_second_in('1', recentRangeDic, 'min')
        recentmin2 = if_second_in('2', recentRangeDic, 'min')
        recentmin3 = if_second_in('3', recentRangeDic, 'min')
        recentmin4 = if_second_in('4', recentRangeDic, 'min')
        recentmin5 = if_second_in('5', recentRangeDic, 'min')
        recentmin6 = if_second_in('6', recentRangeDic, 'min')
        recentmin7 = if_second_in('7', recentRangeDic, 'min')
        recentmin8 = if_second_in('8', recentRangeDic, 'min')
        recentmin9 = if_second_in('9', recentRangeDic, 'min')
        recentmax1 = if_second_in('1', recentRangeDic, 'max')
        recentmax2 = if_second_in('2', recentRangeDic, 'max')
        recentmax3 = if_second_in('3', recentRangeDic, 'max')
        recentmax4 = if_second_in('4', recentRangeDic, 'max')
        recentmax5 = if_second_in('5', recentRangeDic, 'max')
        recentmax6 = if_second_in('6', recentRangeDic, 'max')
        recentmax7 = if_second_in('7', recentRangeDic, 'max')
        recentmax8 = if_second_in('8', recentRangeDic, 'max')
        recentmax9 = if_second_in('9', recentRangeDic, 'max')
        # 类别到类9别之间的信息
        typeToTypeDic = type_to_type()
        for i in range(1, len(timeSort)):
            for j in range(0, i):
                toType = valueDic[timeSort[i]]
                startType = valueDic[timeSort[j]]
                typeDis = int(timeSort[i])-int(timeSort[j])
                typeToTypeDic[toType][startType]['num'] += 1
                if typeToTypeDic[toType][startType]['max'] == '':
                    typeToTypeDic[toType][startType]['max'] = typeDis
                elif typeToTypeDic[toType][startType]['max'] < typeDis:
                    typeToTypeDic[toType][startType]['max'] = typeDis
                if typeToTypeDic[toType][startType]['min'] == '':
                    typeToTypeDic[toType][startType]['min'] = typeDis
                elif typeToTypeDic[toType][startType]['min'] > typeDis:
                    typeToTypeDic[toType][startType]['min'] = typeDis
                if typeToTypeDic[toType][startType]['av'] == '':
                    typeToTypeDic[toType][startType]['av'] = typeDis
                else:
                    typeToTypeDic[toType][startType]['av'] + typeDis
        typeToTypeValue = ''
        for i in range(1, 10):
            i = str(i)
            for j in range(1, 10):
                j = str(j)
                for k in ['min', 'max']:
                    typeToTypeValue += '{},'.format(typeToTypeDic[i][j][k])
        typeToTypeValue = typeToTypeValue.strip(',')
        outList = [
                userId,
                lastType,                   # 最后一个类型
                str(avBrowse),              # 平均浏览时间间隔
                str(minBrowse),             # 最短浏览时间间隔
                str(lastBrowse),            # 最后一次浏览时间间隔
                str(varBrowse),             # 方差浏览
                firstType,                  # 第一个类型
                str(firstBrowse),           # 第一个时间间隔
                str(browseLastTwo),         # 倒数第二个间隔
                str(browseLastThree),       # 倒数第三个间隔
                str(browseLastFour),        # 倒数第四个间隔
                lastTwoType,                # 倒数第二个类型
                lastThreeType,              # 倒数第三个类型
                str(threeAv),               # 最后三个的均值
                str(threeVar),              # 最后三个的方差
                str(type1Per),              # 类型1所占比例
                str(type2Per),              # 类型2所占比例
                str(type3Per),              # 类型3所占比例
                str(type4Per),              # 类型4所占比例
                str(type5Per),              # 类型5所占比例
                str(type6Per),              # 类型6所占比例
                str(type7Per),              # 类型7所占比例
                str(type8Per),              # 类型8所占比例
                str(type9Per),              # 类型9所占比例
                str(type1Num),              # 类型1数量
                str(type2Num),              # 类型2数量
                str(type3Num),              # 类型3数量
                str(type4Num),              # 类型4数量
                str(type5Num),              # 类型5数量
                str(type6Num),              # 类型6数量
                str(type7Num),              # 类型7数量
                str(type8Num),              # 类型8数量
                str(type9Num),              # 类型9数量
                str(recent1),               # 距离最近一次1的时间
                str(recent2),               # 距离最近一次2的时间
                str(recent3),               # 距离最近一次3的时间
                str(recent4),               # 距离最近一次4的时间
                str(recent5),               # 距离最近一次5的时间
                str(recent6),               # 距离最近一次6的时间
                str(recent7),               # 距离最近一次7的时间
                str(recent8),               # 距离最近一次8的时间
                str(recent9),               # 距离最近一次9的时间
                str(recentDis1),            # 距离最近一次1的操作距离
                str(recentDis2),            # 距离最近一次2的操作距离
                str(recentDis3),            # 距离最近一次3的操作距离
                str(recentDis4),            # 距离最近一次4的操作距离
                str(recentDis5),            # 距离最近一次5的操作距离
                str(recentDis6),            # 距离最近一次6的操作距离
                str(recentDis7),            # 距离最近一次7的操作距离
                str(recentDis8),            # 距离最近一次8的操作距离
                str(recentDis9),            # 距离最近一次9的操作距离
                str(recentVar1),            # 距离最近一次1时间方差
                str(recentVar2),            # 距离最近一次2时间方差
                str(recentVar3),            # 距离最近一次3时间方差
                str(recentVar4),            # 距离最近一次4时间方差
                str(recentVar5),            # 距离最近一次5时间方差
                str(recentVar6),            # 距离最近一次6时间方差
                str(recentVar7),            # 距离最近一次7时间方差
                str(recentVar8),            # 距离最近一次8时间方差
                str(recentVar9),            # 距离最近一次9时间方差
                str(recentAv1),             # 距离最近一次1时间均值
                str(recentAv2),             # 距离最近一次2时间均值
                str(recentAv3),             # 距离最近一次3时间均值
                str(recentAv4),             # 距离最近一次4时间均值
                str(recentAv5),             # 距离最近一次5时间均值
                str(recentAv6),             # 距离最近一次6时间均值
                str(recentAv7),             # 距离最近一次7时间均值
                str(recentAv8),             # 距离最近一次8时间均值
                str(recentAv9),             # 距离最近一次9时间均值
                str(recentmin1),             # 距离最近一次1最短间隔
                str(recentmin2),             # 距离最近一次2最短间隔
                str(recentmin3),             # 距离最近一次3最短间隔
                str(recentmin4),             # 距离最近一次4最短间隔
                str(recentmin5),             # 距离最近一次5最短间隔
                str(recentmin6),             # 距离最近一次6最短间隔
                str(recentmin7),             # 距离最近一次7最短间隔
                str(recentmin8),             # 距离最近一次8最短间隔
                str(recentmin9),             # 距离最近一次9最短间隔
                str(recentmax1),             # 距离最近一次1最长间隔
                str(recentmax2),             # 距离最近一次2最长间隔
                str(recentmax3),             # 距离最近一次3最长间隔
                str(recentmax4),             # 距离最近一次4最长间隔
                str(recentmax5),             # 距离最近一次5最长间隔
                str(recentmax6),             # 距离最近一次6最长间隔
                str(recentmax7),             # 距离最近一次7最长间隔
                str(recentmax8),             # 距离最近一次8最长间隔
                str(recentmax9),             # 距离最近一次9最长间隔
                typeToTypeValue,
                ]
        fileWriter.write(
                '{}\n'.format(','.join(outList)).encode('utf8')
                )
