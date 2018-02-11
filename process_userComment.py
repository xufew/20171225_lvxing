# =======================
# -*- coding: utf-8 -*-
# author: LONGFEI XU
# Try your best
# ============
import sys


def process_line(stringList, userDic, idTimeDic):
    userId = stringList[0]
    orderId = stringList[1]
    score = stringList[2]
    tag = stringList[3]
    comment = stringList[4:]
    if userId not in userDic:
        userDic[userId] = __init_user()
    # 好评论次数
    if float(score) >= 4:
        userDic[userId]['goodScoreTime'] += 1
    # 差评论次数
    if float(score) < 4:
        userDic[userId]['badScoreTime'] += 1
    # 包含特殊语句
    if '行程安排有惊喜' in tag:
        userDic[userId]['jingxiword'] = 1
    # 提取短语长度
    userDic[userId]['specialLen'] = len(comment)
    # 评论订单id
    userDic[userId]['pinglunTime'] = orderId
    # if userDic[userId]['pinglunTime'] == '':
    #     userDic[userId]['pinglunTime'] = orderId
    # elif int(userDic[userId]['pinglunTime']) < int(orderId):
    #     userDic[userId]['pinglunTime'] = orderId
    # 评论时间
    if userDic[userId]['pinglunDate'] == '':
        if orderId in idTimeDic:
            userDic[userId]['pinglunDate'] = idTimeDic[orderId]
    elif int(userDic[userId]['pinglunDate']) < int(idTimeDic[orderId]):
        if orderId in idTimeDic:
            userDic[userId]['pinglunDate'] = idTimeDic[orderId]


def __init_user():
    outDic = {
            'badScoreTime': 0,
            'goodScoreTime': 0,
            'jingxiword': 0,
            'specialLen': '',
            'pinglunTime': '',
            'pinglunDate': '',
            }
    return outDic


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
    userCommentPath = sys.argv[1]
    outPath = sys.argv[2]
    userHisPath = sys.argv[3]
    idTimeDic = read_id_time(userHisPath)
    with open(userCommentPath, 'rb') as fileReader:
        count = 0
        userDic = {}
        while True:
            stringLine = fileReader.readline()
            if stringLine:
                count += 1
                if count == 1:
                    continue
                stringList = stringLine.strip().decode('utf8').split(',')
                process_line(stringList, userDic, idTimeDic)
            else:
                break
    fileWriter = open(outPath, 'wb')
    count = 0
    for userId in userDic:
        count += 1
        if count == 1:
            nameList = [
                    'userid',
                    'badScoreTime',
                    'goodScoreTime',
                    'jingxiword',
                    'specialLen',
                    'pinglunTime',
                    'pinglunDate',
                    ]
            fileWriter.write(
                    '{}\n'.format(','.join(nameList)).encode('utf8')
                    )
        infoDic = userDic[userId]
        badScoreTime = infoDic['badScoreTime']
        goodScoreTime = infoDic['goodScoreTime']
        jingxiword = infoDic['jingxiword']
        specialLen = infoDic['specialLen']
        pinglunTime = infoDic['pinglunTime']
        pinglunDate = infoDic['pinglunDate']
        outList = [
                userId,
                str(badScoreTime),
                str(goodScoreTime),
                str(jingxiword),
                str(specialLen),
                str(pinglunTime),
                str(pinglunDate),
                ]
        fileWriter.write(
                '{}\n'.format(','.join(outList)).encode('utf8')
                )
