# =======================
# -*- coding: utf-8 -*-
# author: LONGFEI XU
# Try your best
# ============
import sys


def process_line(stringList, userDic):
    userId = stringList[0]
    orderId = stringList[1]
    orderTime = stringList[2]
    orderType = stringList[3]
    city = stringList[4]
    country = stringList[5]
    continent = stringList[6]
    if userId not in userDic:
        userDic[userId] = __init_user()
    # 完成单量
    userDic[userId]['orderNum'] += 1
    # 精品单量
    if orderType == '1':
        userDic[userId]['superNum'] += 1
    if orderType == '0':
        userDic[userId]['simpleNum'] += 1
    # 统计去过城市次数
    if continent not in userDic[userId]['continentDic']:
        userDic[userId]['continentDic'][continent] = 0
    userDic[userId]['continentDic'][continent] += 1
    # 最近下单的时间
    if int(orderTime) > int(userDic[userId]['nearestTime']):
        userDic[userId]['nearestTime'] = orderTime
        if orderType == '1':
            userDic[userId]['nearSuper'] = 1
        else:
            userDic[userId]['nearSuper'] = 0


def __init_user():
    outDic = {
            'orderNum': 0,          # 所下总订单数量
            'superNum': 0,          # 精品订单数量
            'continentDic': {},     # 旅游去过的大陆
            'nearestTime': 0,       # 最近下单时间
            'nearSuper': 0,         # 最近一次下单是否为精品订单
            'simpleNum': 0,         # 普通单数量
            }
    return outDic


if __name__ == '__main__':
    orderHistoryPath = sys.argv[1]
    outPath = sys.argv[2]
    with open(orderHistoryPath, 'rb') as fileReader:
        count = 0
        userDic = {}
        while True:
            stringLine = fileReader.readline()
            if stringLine:
                count += 1
                if count == 1:
                    continue
                stringList = stringLine.strip().decode('utf8').split(',')
                process_line(stringList, userDic)
            else:
                break
    fileWriter = open(outPath, 'wb')
    count = 0
    for userId in userDic:
        count += 1
        if count == 1:
            nameList = [
                    'userid',
                    'orderNum',
                    'superNum',
                    'superPer',
                    'nearSuper',
                    'simpleNum',
                    'simplePer',
                    ]
            fileWriter.write(
                    '{}\n'.format(','.join(nameList)).encode('utf8')
                    )
        infoDic = userDic[userId]
        orderNum = infoDic['orderNum']
        superNum = infoDic['superNum']
        nearSuper = infoDic['nearSuper']
        simpleNum = infoDic['simpleNum']
        # 精品订单占比
        superPer = superNum/float(orderNum)
        outList = [
                userId,
                str(orderNum),
                str(superNum),
                str(superPer),
                str(nearSuper),
                str(simpleNum),
                str(simpleNum/float(orderNum))
                ]
        fileWriter.write(
                '{}\n'.format(','.join(outList)).encode('utf8')
                )
