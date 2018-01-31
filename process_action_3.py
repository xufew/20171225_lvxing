# =======================
# -*- coding: utf-8 -*-
# author: LONGFEI XU
# Try your best
# ============
import sys
import datetime

import few_base


def write_feature_name(fileWriter):
    featureList = [
            'userid',
            'finalYear',
            'finalmonth',
            'finalHour',
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
        # 进行结果综合
        outList = [
                userId,
                str(finalYear),
                str(finalmonth),
                str(finalHour),
                ]
        fileWriter.write(
                '{}\n'.format(','.join(outList)).encode('utf8')
                )
