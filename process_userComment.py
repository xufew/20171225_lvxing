# =======================
# -*- coding: utf-8 -*-
# author: LONGFEI XU
# Try your best
# ============
import sys


def process_line(stringList, userDic):
    userId = stringList[0]
    orderId = stringList[1]
    score = stringList[2]
    tag = stringList[3]
    comment = stringList[4]
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


def __init_user():
    outDic = {
            'badScoreTime': 0,
            'goodScoreTime': 0,
            'jingxiword': 0,
            }
    return outDic


if __name__ == '__main__':
    userCommentPath = sys.argv[1]
    outPath = sys.argv[2]
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
                    'badScoreTime',
                    'goodScoreTime',
                    'jingxiword',
                    ]
            fileWriter.write(
                    '{}\n'.format(','.join(nameList)).encode('utf8')
                    )
        infoDic = userDic[userId]
        badScoreTime = infoDic['badScoreTime']
        goodScoreTime = infoDic['goodScoreTime']
        jingxiword = infoDic['jingxiword']
        outList = [
                userId,
                str(badScoreTime),
                str(goodScoreTime),
                str(jingxiword),
                ]
        fileWriter.write(
                '{}\n'.format(','.join(outList)).encode('utf8')
                )
