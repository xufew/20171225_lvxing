# =======================
# -*- coding: utf-8 -*-
# author: LONGFEI XU
# Try your best
# ============
import sys


def write_feature_name(fileWriter):
    featureList = [
            'userid',
            '1in',
            '2in',
            '3in',
            '4in',
            '5in',
            '6in',
            '7in',
            '8in',
            '9in',
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
    write_feature_name(fileWriter)
    userDic = read_userDic(actionPath)
    count = 0
    for userId in userDic:
        count += 1
        if count % 1000 == 0:
            print(count)
        valueDic = userDic[userId]
        timeSort = sorted(valueDic)
        valueList = list(map(lambda x, y=valueDic: valueDic[x], timeSort))
        outList = [
                userId,
                str(if_in('1', valueList)),
                str(if_in('2', valueList)),
                str(if_in('3', valueList)),
                str(if_in('4', valueList)),
                str(if_in('5', valueList)),
                str(if_in('6', valueList)),
                str(if_in('7', valueList)),
                str(if_in('8', valueList)),
                str(if_in('9', valueList)),
                ]
        fileWriter.write(
                '{}\n'.format(','.join(outList)).encode('utf8')
                )
