# =======================
# -*- coding: utf-8 -*-
# author: LONGFEI XU
# Try your best
# ============
import sys
import datetime
import copy
import math

import few_base


def write_feature_name(fileWriter):
    featureList = [
            'userid',
            'finalYear',
            'finalmonth',
            'finalHour',
            'totalAction',
            'rangePer1',
            'rangePer2',
            'rangePer3',
            'rangePer4',
            'rangePer5',
            'rangePer6',
            'rangePer7',
            'rangePer8',
            'rangePer9',
            'rangePer10',
            'rangePer11',
            'rangeNum9',
            'dateLow',
            'dateHigh',
            'dateContinue',
            'dateCut',
            ]
    fileWriter.write(
            '{}\n'.format(','.join(featureList)).encode('utf8')
            )


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


def if_in(value, valueList):
    if value in valueList:
        return 1
    else:
        return 0


def range_day_action():
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
            'total': 0,
            }
    return lastDayActionNum


if __name__ == '__main__':
    actionPath = sys.argv[1]
    outPath = sys.argv[2]
    fileWriter = open(outPath, 'wb')
    timer = few_base.Timer()
    # 统计路径
    userDic = read_userDic(actionPath)
    # 写列名
    write_feature_name(fileWriter)
    # 开始进行统计
    count = 0
    for userId in userDic:
        count += 1
        if count % 1000 == 0:
            print(count)
        valueDic = userDic[userId]
        timeSort = sorted(valueDic)
        valueList = list(map(lambda x, y=valueDic: valueDic[x], timeSort))
        # 最后一次操作发生月份，白天还是晚上，周中还是周末
        finalDate = timeSort[-1]
        finalYear = int(timer.trans_unix_to_string(finalDate, '%Y'))
        finalmonth = int(timer.trans_unix_to_string(finalDate, '%m'))
        finalHour = int(timer.trans_unix_to_string(finalDate, '%H'))
        finalDay = timer.trans_unix_to_string(finalDate, '%Y%m%d')
        finalWeek = datetime.datetime.strptime(finalDay, '%Y%m%d').weekday()
        if finalWeek == 6 or finalWeek == 7:
            finalWeekend = 1
        else:
            finalWeekend = 0
        totalAction = len(timeSort)
        # 最近一段时间发生过的行为
        finalDate = int(timeSort[-1])
        rangeNumDic = range_day_action()
        for thisTime in timeSort:
            thisTime = int(thisTime)
            if finalDate-thisTime > 1209600:
                # 大于这个时间的不进行统计
                continue
            thisAction = valueDic[str(thisTime)]
            rangeNumDic[thisAction] += 1
            rangeNumDic['total'] += 1
        # 最近的时间处于哪个时间节点内
        finalDate = int(timeSort[-1])
        if finalDate < 1.4782*math.pow(10, 9):
            dateLow = 1
        else:
            dateLow = 0
        con1 = finalDate >= 1.4782*math.pow(10, 9)
        con2 = finalDate < 1.491*math.pow(10, 9)
        if con1 and con2:
            dateHigh = 1
        else:
            dateHigh = 0
        con1 = finalDate >= 1.491*math.pow(10, 9)
        con2 = finalDate < 1.503*math.pow(10, 9)
        if con1 and con2:
            dateContinue = 1
        else:
            dateContinue = 0
        con1 = finalDate >= 1.503*math.pow(10, 9)
        if con1:
            dateCut = 1
        else:
            dateCut = 0
        # 进行结果综合
        outList = [
                userId,
                str(finalYear),
                str(finalmonth),
                str(finalHour),
                str(totalAction),
                str(rangeNumDic['1']/float(rangeNumDic['total'])),
                str(rangeNumDic['2']/float(rangeNumDic['total'])),
                str(rangeNumDic['3']/float(rangeNumDic['total'])),
                str(rangeNumDic['4']/float(rangeNumDic['total'])),
                str(rangeNumDic['5']/float(rangeNumDic['total'])),
                str(rangeNumDic['6']/float(rangeNumDic['total'])),
                str(rangeNumDic['7']/float(rangeNumDic['total'])),
                str(rangeNumDic['8']/float(rangeNumDic['total'])),
                str(rangeNumDic['9']/float(rangeNumDic['total'])),
                str(rangeNumDic['10']/float(rangeNumDic['total'])),
                str(rangeNumDic['11']/float(rangeNumDic['total'])),
                str(rangeNumDic['9']),
                str(dateLow),
                str(dateHigh),
                str(dateContinue),
                str(dateCut),
                ]
        fileWriter.write(
                '{}\n'.format(','.join(outList)).encode('utf8')
                )
