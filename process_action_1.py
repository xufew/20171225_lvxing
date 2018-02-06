# =======================
# -*- coding: utf-8 -*-
# author: LONGFEI XU
# Try your best
# ============
import sys
import datetime
import copy

import numpy as np
import tushare as ts

import few_base


def write_feature_name(fileWriter):
    typeToTypeName = ''
    for i in [10, 11]:
        i = str(i)
        for j in range(1, 12):
            j = str(j)
            for k in ['min', 'max']:
                typeToTypeName += '{}To{}Time{},'.format(j, i, k)
    typeToTypeName = typeToTypeName[:-1]
    #
    firstTypeDateString = ''
    for i in range(1, 13, 1):
        i = str(i)
        for thisDetail in [
                'firstYear', 'firstmonth', 'firstHour', 'firstDate'
                ]:
            firstTypeDateString += '{}_{},'.format(
                    thisDetail, i
                    )
    firstTypeDateString = firstTypeDateString[:-1]
    finalTypeDateString = ''
    for i in range(1, 13, 1):
        i = str(i)
        for thisDetail in [
                'finalYear', 'finalmonth', 'finalHour', 'finalDate'
                ]:
            finalTypeDateString += '{}_{},'.format(
                    thisDetail, i
                    )
    finalTypeDateString = finalTypeDateString[:-1]
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
            'continueVar1',
            'continueVar2',
            'continueVar3',
            'continueVar4',
            'continueVar5',
            'continueVar6',
            'continueVar7',
            'continueVar8',
            'continueVar9',
            'continueAv1',
            'continueAv2',
            'continueAv3',
            'continueAv4',
            'continueAv5',
            'continueAv6',
            'continueAv7',
            'continueAv8',
            'continueAv9',
            'typeDismin1',
            'typeDismin2',
            'typeDismin3',
            'typeDismin4',
            'typeDismin5',
            'typeDismin6',
            'typeDismin7',
            'typeDismin8',
            'typeDismin9',
            'typeDismax1',
            'typeDismax2',
            'typeDismax3',
            'typeDismax4',
            'typeDismax5',
            'typeDismax6',
            'typeDismax7',
            'typeDismax8',
            'typeDismax9',
            'recent10',
            'recent11',
            'type10Per',
            'type11Per',
            'type10Num',
            'type11Num',
            'recentDis10',
            'recentDis11',
            typeToTypeName,
            'recentVar10',
            'recentVar11',
            'recentAv10',
            'recentAv11',
            'recentmin10',
            'recentmin11',
            'firstDate',
            'finalDate',
            'finalSecondDate',
            'finalThirdDate',
            'lastDayNum',
            'lastDayActionNum1',
            'lastDayActionNum2',
            'lastDayActionNum3',
            'lastDayActionNum4',
            'lastDayActionNum5',
            'lastDayActionNum6',
            'lastDayActionNum7',
            'lastDayActionNum8',
            'lastDayActionNum9',
            'lastDayActionNum10',
            'lastDayActionNum11',
            'lastDayActionNum12',
            'gupiaoOpen',
            'gupiaoChange',
            firstTypeDateString,
            finalTypeDateString
            ]
    fileWriter.write(
            '{}\n'.format(','.join(featureList)).encode('utf8')
            )


def if_second_in(typeNum, valueDic, valueName):
    if typeNum in valueDic:
        outValue = valueDic[typeNum][valueName]
    else:
        outValue = ''
    return outValue


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


def read_userDic(actionPath):
    with open(actionPath, 'rb') as fileReader:
        count = 0
        userDic = {}
        instead9Dic = {}
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
                    instead9Dic[userId] = {'9': [], '10': [], '11': []}
                if actionTime in userDic[userId]:
                    while True:
                        actionTime = str(int(actionTime)+1)
                        if actionTime not in userDic[userId]:
                            userDic[userId][actionTime] = actionType
                            if (actionType == '9') or (actionType == '10') or (
                                    actionType == '11'
                                    ):
                                instead9Dic[userId][actionType].append(
                                        actionTime
                                        )
                            break
                else:
                    userDic[userId][actionTime] = actionType
                    if (actionType == '9') or (actionType == '10') or (
                            actionType == '11'
                            ):
                        instead9Dic[userId][actionType].append(
                                actionTime
                                )
            else:
                break
    # 进行9的时间合并
    for userid in instead9Dic:
        insteadDic = instead9Dic[userid]
        timeDic = userDic[userid]
        for nineTime in insteadDic['9']:
            nineTime = int(nineTime)
            # 合并10
            ifContinue = True
            for tenTime in copy.deepcopy(insteadDic['10']):
                tenTime = int(tenTime)
                thisRange = abs(nineTime - tenTime)
                if thisRange < 200:
                    changeTime = str(max(nineTime, tenTime))
                    timeDic.pop(str(nineTime))
                    if changeTime in timeDic:
                        while True:
                            changeTime = str(int(changeTime)+1)
                            if changeTime not in timeDic:
                                timeDic[changeTime] = '9'
                                break
                    else:
                        timeDic[changeTime] = '9'
                    insteadDic['10'].remove(str(tenTime))
                    ifContinue = False
                    break
            if ifContinue:
                # 合并11
                for eleTime in copy.deepcopy(insteadDic['11']):
                    eleTime = int(eleTime)
                    thisRange = abs(nineTime - eleTime)
                    if thisRange < 200:
                        changeTime = str(max(nineTime, eleTime))
                        timeDic.pop(str(nineTime))
                        if changeTime in timeDic:
                            while True:
                                changeTime = str(int(changeTime)+1)
                                if changeTime not in timeDic:
                                    timeDic[changeTime] = '9'
                                    break
                        else:
                            timeDic[changeTime] = '9'
                        insteadDic['11'].remove(str(eleTime))
                        break
        # 将没有任何操作的填入当做9
        if len(insteadDic['10']) != 0:
            for addTime in insteadDic['10']:
                if addTime in timeDic:
                    while True:
                        addTime = str(int(addTime)+1)
                        if addTime not in timeDic:
                            timeDic[addTime] = '9'
                            break
                else:
                    timeDic[addTime] = '9'
        if len(insteadDic['11']) != 0:
            for addTime in insteadDic['11']:
                timeDic[addTime] = '9'
                if addTime in timeDic:
                    while True:
                        addTime = str(int(addTime)+1)
                        if addTime not in timeDic:
                            timeDic[addTime] = '9'
                            break
                else:
                    timeDic[addTime] = '9'
    return userDic


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
            '10': [],
            '11': [],
            }
    return outDic


def continue_return_value(useType, valueType, valueDic):
    '''
    返回连续命中的相关值
    '''
    valueList = valueDic[useType]
    if len(valueList) == 0:
        return ''
    else:
        if valueType == 'min':
            outValue = min(valueList)
        elif valueType == 'max':
            outValue = max(valueList)
        elif valueType == 'av':
            outValue = sum(valueList)/float(len(valueList))
        elif valueType == 'var':
            outValue = np.var(valueList)
        return outValue


def to_type_time():
    '''
    距离不同type的最短和最长时间间隔
    '''
    outDic = {
            '1': {'min': '', 'max': ''},
            '2': {'min': '', 'max': ''},
            '3': {'min': '', 'max': ''},
            '4': {'min': '', 'max': ''},
            '5': {'min': '', 'max': ''},
            '6': {'min': '', 'max': ''},
            '7': {'min': '', 'max': ''},
            '8': {'min': '', 'max': ''},
            '9': {'min': '', 'max': ''},
            '10': {'min': '', 'max': ''},
            '11': {'min': '', 'max': ''},
            }
    return outDic


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
                '10': {'min': '', 'max': '', 'av': '', 'num': 0},
                '11': {'min': '', 'max': '', 'av': '', 'num': 0},
                }
        return oneDic
    outDic = {
            '10': get_one(),
            '11': get_one(),
            }
    return outDic


def get_range(valueDic, timeSort):
    '''
    计算离每个type的平均，方差的时间间隔
    '''
    recentDic = {}
    for thisTime in timeSort:
        thisType = valueDic[thisTime]
        con1 = thisType == '10'
        con2 = thisType == '11'
        if con1 or con2:
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
            recentDic[thisType] = {
                    'av': avRange,
                    'var': varRange,
                    'min': minRange,
                    }
    return recentDic


def final_type_date():
    '''
    最终最近一次的，不同type的具体时间
    '''
    def one_dic():
        return {
                'finalYear': '',
                'finalmonth': '',
                'finalHour': '',
                'finalWeekend': '',
                'finalDate': '',
                }
    finalTypeDate = {
            '1': one_dic(),
            '2': one_dic(),
            '3': one_dic(),
            '4': one_dic(),
            '5': one_dic(),
            '6': one_dic(),
            '7': one_dic(),
            '8': one_dic(),
            '9': one_dic(),
            '10': one_dic(),
            '11': one_dic(),
            '12': one_dic(),
            }
    return finalTypeDate


def cal_detail_date(dateUnix):
    finalYear = int(timer.trans_unix_to_string(dateUnix, '%Y'))
    finalmonth = int(timer.trans_unix_to_string(dateUnix, '%m'))
    finalHour = int(timer.trans_unix_to_string(dateUnix, '%H'))
    finalDay = timer.trans_unix_to_string(dateUnix, '%Y%m%d')
    finalWeek = datetime.datetime.strptime(finalDay, '%Y%m%d').weekday()
    if finalWeek == 6 or finalWeek == 7:
        finalWeekend = 1
    else:
        finalWeekend = 0
    return {
            'finalYear': finalYear,
            'finalmonth': finalmonth,
            'finalHour': finalHour,
            'finalWeekend': finalWeekend,
            'finalDate': dateUnix,
            }


def first_type_date():
    '''
    最终最近一次的，不同type的具体时间
    '''
    def one_dic():
        return {
                'finalYear': '',
                'finalmonth': '',
                'finalHour': '',
                'finalWeekend': '',
                'finalDate': '',
                }
    firstTypeDate = {
            '1': one_dic(),
            '2': one_dic(),
            '3': one_dic(),
            '4': one_dic(),
            '5': one_dic(),
            '6': one_dic(),
            '7': one_dic(),
            '8': one_dic(),
            '9': one_dic(),
            '10': one_dic(),
            '11': one_dic(),
            '12': one_dic(),
            }
    return firstTypeDate


def last_day_action():
    lastDayActionNum = {
            '1': 0,
            '2': 0,
            '3': 0,
            '4': 0,
            '5': 0,
            '6': 0,
            '7': 0,
            '8': 0,
            '9': 0,
            '10': 0,
            '11': 0,
            '12': 0,
            }
    return lastDayActionNum


if __name__ == '__main__':
    actionPath = sys.argv[1]
    outPath = sys.argv[2]
    fileWriter = open(outPath, 'wb')
    timer = few_base.Timer()
    allgupiao = ts.get_hist_data('sh', end='2018-01-10')
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
        typeDisDic = to_type_time()
        finalTypeDate = final_type_date()
        firstTypeDate = first_type_date()
        lastDayActionNum = last_day_action()
        lastDay = timer.trans_unix_to_string(timeSort[-1], format='%Y%m%d')
        lastDayNum = 0
        for i, thisTime in enumerate(timeSort):
            thisType = valueDic[thisTime]
            con1 = thisType == '9'
            con2 = i == totalNum-1
            con3 = i < totalNum-1
            go9Dis += 1
            # 统计每种type最后一次出现的时间
            if len(finalTypeDate[thisType]['finalDate']) == 0:
                finalTypeDate[thisType] = cal_detail_date(thisTime)
            else:
                if int(thisTime) > int(finalTypeDate[thisType]['finalDate']):
                    finalTypeDate[thisType] = cal_detail_date(thisTime)
                if (thisType == '9') or (thisType == '10') or (
                        thisType == '11'
                        ):
                    if len(finalTypeDate['12']['finalDate']) == 0:
                        finalTypeDate['12'] = cal_detail_date(thisTime)
                    else:
                        if int(thisTime) > int(
                                finalTypeDate['12']['finalDate']
                                ):
                            finalTypeDate['12'] = cal_detail_date(thisTime)
            if len(firstTypeDate[thisType]['finalDate']) == 0:
                firstTypeDate[thisType] = cal_detail_date(thisTime)
            else:
                if int(thisTime) < int(firstTypeDate[thisType]['finalDate']):
                    firstTypeDate[thisType] = cal_detail_date(thisTime)
                if (thisType == '9') or (thisType == '10') or (
                        thisType == '11'
                        ):
                    if len(firstTypeDate['12']['finalDate']) == 0:
                        firstTypeDate['12'] = cal_detail_date(thisTime)
                    else:
                        if int(thisTime) < int(
                                firstTypeDate['12']['finalDate']
                                ):
                            firstTypeDate['12'] = cal_detail_date(thisTime)
            # 统计最后一天发生了多少次action操作
            thisDay = timer.trans_unix_to_string(thisTime, format='%Y%m%d')
            if int(thisDay) == int(lastDay):
                lastDayNum += 1
                lastDayActionNum[thisType] += 1
                if (thisType == '9') or (thisType == '10') or (
                        thisType == '11'
                        ):
                    lastDayActionNum['12'] += 1
            if con3:
                go9Time += int(timeSort[i+1])-int(timeSort[i])
            if con1 or con2:
                go9DisList.append(go9Dis)
                go9TimeList.append(go9Time/float(go9Dis))
                go9Dis = 0
                go9Time = 0
            if con3:
                # 统计连续命中情况
                nextType = valueDic[timeSort[i+1]]
                if nextType == thisType:
                    continueDic[nextType].append(
                            int(timeSort[i+1])-int(timeSort[i])
                            )
            if con3:
                # 统计到不同类型最近一次操作最短和最长时间
                useType = valueDic[timeSort[i+1]]
                typeDis = int(timeSort[i+1])-int(timeSort[i])
                if typeDisDic[useType]['max'] == '':
                    typeDisDic[useType]['max'] = typeDis
                elif typeDisDic[useType]['max'] < typeDis:
                    typeDisDic[useType]['max'] = typeDis
                if typeDisDic[useType]['min'] == '':
                    typeDisDic[useType]['min'] = typeDis
                elif typeDisDic[useType]['min'] > typeDis:
                    typeDisDic[useType]['min'] = typeDis
        # 最后和最开始时间的细化结合
        firstTypeDateString = ''
        for i in range(1, 13, 1):
            i = str(i)
            for thisDetail in [
                    'finalYear', 'finalmonth', 'finalHour', 'finalDate'
                    ]:
                firstTypeDateString += '{},'.format(
                        firstTypeDate[i][thisDetail]
                        )
        firstTypeDateString = firstTypeDateString[:-1]
        finalTypeDateString = ''
        for i in range(1, 13, 1):
            i = str(i)
            for thisDetail in [
                    'finalYear', 'finalmonth', 'finalHour', 'finalDate'
                    ]:
                finalTypeDateString += '{},'.format(
                        finalTypeDate[i][thisDetail]
                        )
        finalTypeDateString = finalTypeDateString[:-1]
        # 离最近的时间
        recentTimeDic = get_recent_dic(valueDic, timeSort)
        recent10 = if_second_in('10', recentTimeDic, 'nowTime')
        recent11 = if_second_in('11', recentTimeDic, 'nowTime')
        # 点击类型比例
        valueCount = np.unique(list(valueDic.values()), return_counts=True)
        valueCountDic = dict(list(zip(valueCount[0], valueCount[1])))
        totalCount = float(sum(valueCountDic.values()))
        type10Per = if_value_in('10', valueCountDic)/totalCount
        type11Per = if_value_in('11', valueCountDic)/totalCount
        type10Num = if_value_in('10', valueCountDic)
        type11Num = if_value_in('11', valueCountDic)
        # 离最近的距离
        recentDisDic = get_recent_dis(valueDic, timeSort)
        recentDis10 = if_value_dic('10', recentDisDic)
        recentDis11 = if_value_dic('11', recentDisDic)
        # 类别到类别之间的信息
        typeToTypeDic = type_to_type()
        for i in range(1, len(timeSort)):
            for j in range(0, i):
                toType = valueDic[timeSort[i]]
                con1 = toType == '10'
                con2 = toType == '11'
                if con1 or con2:
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
        for i in [10, 11]:
            i = str(i)
            for j in range(1, 12):
                j = str(j)
                for k in ['min', 'max']:
                    typeToTypeValue += '{},'.format(typeToTypeDic[i][j][k])
        typeToTypeValue = typeToTypeValue[:-1]
        # 方差均值
        recentRangeDic = get_range(valueDic, timeSort)
        recentVar10 = if_second_in('10', recentRangeDic, 'var')
        recentVar11 = if_second_in('11', recentRangeDic, 'var')
        recentAv10 = if_second_in('10', recentRangeDic, 'av')
        recentAv11 = if_second_in('11', recentRangeDic, 'av')
        recentmin10 = if_second_in('10', recentRangeDic, 'min')
        recentmin11 = if_second_in('11', recentRangeDic, 'min')
        # 第一次的时间，最后一次的时间
        firstDate = timeSort[0]
        if len(timeSort) >= 2:
            finalSecondDate = timeSort[-2]
        else:
            finalSecondDate = ''
        if len(timeSort) >= 3:
            finalThirdDate = timeSort[-3]
        else:
            finalThirdDate = ''
        finalDate = timeSort[-1]
        checkDate = finalDate
        while True:
            checkDate = int(checkDate)-86400
            finalDateString = timer.trans_unix_to_string(checkDate, '%Y-%m-%d')
            try:
                gupiaoOpen = allgupiao.loc[finalDateString, 'open']
                gupiaoChange = allgupiao.loc[finalDateString, 'price_change']
                break
            except Exception:
                pass
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
                str(continue_return_value('1', 'var', continueDic)),
                str(continue_return_value('2', 'var', continueDic)),
                str(continue_return_value('3', 'var', continueDic)),
                str(continue_return_value('4', 'var', continueDic)),
                str(continue_return_value('5', 'var', continueDic)),
                str(continue_return_value('6', 'var', continueDic)),
                str(continue_return_value('7', 'var', continueDic)),
                str(continue_return_value('8', 'var', continueDic)),
                str(continue_return_value('9', 'var', continueDic)),
                str(continue_return_value('1', 'av', continueDic)),
                str(continue_return_value('2', 'av', continueDic)),
                str(continue_return_value('3', 'av', continueDic)),
                str(continue_return_value('4', 'av', continueDic)),
                str(continue_return_value('5', 'av', continueDic)),
                str(continue_return_value('6', 'av', continueDic)),
                str(continue_return_value('7', 'av', continueDic)),
                str(continue_return_value('8', 'av', continueDic)),
                str(continue_return_value('9', 'av', continueDic)),
                str(typeDisDic['1']['min']),
                str(typeDisDic['2']['min']),
                str(typeDisDic['3']['min']),
                str(typeDisDic['4']['min']),
                str(typeDisDic['5']['min']),
                str(typeDisDic['6']['min']),
                str(typeDisDic['7']['min']),
                str(typeDisDic['8']['min']),
                str(typeDisDic['9']['min']),
                str(typeDisDic['1']['max']),
                str(typeDisDic['2']['max']),
                str(typeDisDic['3']['max']),
                str(typeDisDic['4']['max']),
                str(typeDisDic['5']['max']),
                str(typeDisDic['6']['max']),
                str(typeDisDic['7']['max']),
                str(typeDisDic['8']['max']),
                str(typeDisDic['9']['max']),
                str(recent10),
                str(recent11),
                str(type10Per),
                str(type11Per),
                str(type10Num),
                str(type11Num),
                str(recentDis10),
                str(recentDis11),
                typeToTypeValue,
                str(recentVar10),
                str(recentVar11),
                str(recentAv10),
                str(recentAv11),
                str(recentmin10),
                str(recentmin11),
                str(firstDate),
                str(finalDate),
                str(finalSecondDate),
                str(finalThirdDate),
                str(lastDayNum),                    # 最后一天发生了多少次action操作
                str(lastDayActionNum['1']),
                str(lastDayActionNum['2']),
                str(lastDayActionNum['3']),
                str(lastDayActionNum['4']),
                str(lastDayActionNum['5']),
                str(lastDayActionNum['6']),
                str(lastDayActionNum['7']),
                str(lastDayActionNum['8']),
                str(lastDayActionNum['9']),
                str(lastDayActionNum['10']),
                str(lastDayActionNum['11']),
                str(lastDayActionNum['12']),
                str(gupiaoOpen),
                str(gupiaoChange),
                firstTypeDateString,
                finalTypeDateString
                ]

        fileWriter.write(
                '{}\n'.format(','.join(outList)).encode('utf8')
                )
