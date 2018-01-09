# =======================
# -*- coding: utf-8 -*-
# author: LONGFEI XU
# Try your best
# ============
import sys


def write_action(actionPath, fileWriter):
    with open(actionPath, 'rb') as fileReader:
        while True:
            stringLine = fileReader.readline()
            if stringLine:
                stringLine = stringLine.strip().decode('utf8')
                fileWriter.write(
                        '{}\n'.format(stringLine).encode('utf8')
                        )
            else:
                break


def write_his(actionPath, fileWriter):
    with open(actionPath, 'rb') as fileReader:
        count = 0
        while True:
            stringLine = fileReader.readline()
            if stringLine:
                count += 1
                if count == 1:
                    continue
                stringList = stringLine.strip().decode('utf8').split(',')
                userId = stringList[0]
                userTime = stringList[2]
                orderType = stringList[3]
                if orderType == '0':
                    actionType = '10'
                elif orderType == '1':
                    actionType = '11'
                fileWriter.write(
                        '{},{},{}\n'.format(
                            userId, actionType, userTime
                            ).encode('utf8')
                        )
            else:
                break


if __name__ == '__main__':
    actionPath = sys.argv[1]
    orderHisPath = sys.argv[2]
    outPath = sys.argv[3]
    fileWriter = open(outPath, 'wb')
    # 写入action
    write_action(actionPath, fileWriter)
    # 写入历史订单承担信息，10为0普通成单时间，11为精品承担时间
    write_his(orderHisPath, fileWriter)
