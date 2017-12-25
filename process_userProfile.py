# =======================
# -*- coding: utf-8 -*-
# author: LONGFEI XU
# Try your best
# ============
import sys

import few_model


ageDic = {
        '60后': 0,
        '70后': 1,
        '80后': 2,
        '90后': 3,
        '00后': 4,
        }

genderDic = {
        '男': 0,
        '女': 1,
        }

provinceDic = {
        '北京': 0,
        '浙江': 1,
        '甘肃': 2,
        '安徽': 3,
        '贵州': 4,
        '吉林': 5,
        '四川': 6,
        '江苏': 7,
        '福建': 8,
        '新疆': 9,
        '上海': 10,
        '海南': 11,
        '天津': 12,
        '重庆': 13,
        '云南': 14,
        '青海': 15,
        '内蒙古': 16,
        '湖北': 17,
        '河北': 18,
        '西藏': 19,
        '黑龙江': 20,
        '河南': 21,
        '广西': 22,
        '陕西': 23,
        '山东': 24,
        '广东': 25,
        '湖南': 26,
        '山西': 27,
        '江西': 28,
        '辽宁': 29,
        '宁夏': 30,
        }


def process_list(stringList):
    '''
    进行一行的处理
    '''
    userId = stringList[0]
    gender = stringList[1]
    province = stringList[2]
    age = stringList[3]
    genderList = few_model.Preprocessor.one_hot(genderDic, gender)
    provinceList = few_model.Preprocessor.one_hot(provinceDic, province)
    ageList = few_model.Preprocessor.one_hot(ageDic, age)
    outString = '{}\t{}\t{}\t{}'.format(
            userId,
            '\t'.join(list(map(lambda x: str(x), genderList))),
            '\t'.join(list(map(lambda x: str(x), provinceList))),
            '\t'.join(list(map(lambda x: str(x), ageList))),
            )
    return outString


if __name__ == '__main__':
    userProfilePath = sys.argv[1]
    outUserProfile = sys.argv[2]
    count = 0
    fileWriter = open(outUserProfile, 'wb')
    with open(userProfilePath, 'rb') as fileReader:
        while True:
            stringLine = fileReader.readline()
            if stringLine:
                count += 1
                stringList = stringLine.strip().decode('utf8').split(',')
                if count == 1:
                    outString = '{}\t{}\t{}\t{}'.format(
                            'userId',
                            '\t'.join(few_model.Preprocessor.get_one_hot_name(genderDic)),
                            '\t'.join(few_model.Preprocessor.get_one_hot_name(provinceDic)),
                            '\t'.join(few_model.Preprocessor.get_one_hot_name(ageDic)),
                            )
                else:
                    outString = process_list(stringList)
                fileWriter.write(
                        '{}\n'.format(outString).encode('utf8')
                        )
            else:
                break
