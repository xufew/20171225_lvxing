# =======================
# -*- coding: utf-8 -*-
# author: LONGFEI XU
# Try your best
# ============
import sys
import pickle

import few_model


ageDic = {
        '60后': 0,
        '70后': 1,
        '80后': 2,
        '90后': 3,
        '00后': 4,
        }

ageNum = {
        '': '',
        '60后': 60,
        '70后': 70,
        '80后': 80,
        '90后': 90,
        '00后': 100,
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


def process_list(stringList, provinceValue):
    '''
    进行一行的处理
    '''
    userId = stringList[0]
    gender = stringList[1]
    province = stringList[2]
    age = stringList[3]
    if len(stringList) > 4:
        useridUse = userId
        userId = stringList[4]
    else:
        useridUse = userId
    genderList = few_model.Preprocessor.one_hot(genderDic, gender)
    provinceList = few_model.Preprocessor.one_hot(provinceDic, province)
    ageList = few_model.Preprocessor.one_hot(ageDic, age)
    outString = '{},{},{},{},{},{},{}'.format(
            userId,
            useridUse,
            genderList,
            provinceList,
            ageList,
            ','.join(provinceValue[province]),
            ageNum[age],
            )
    return outString


def get_hot_name(inputDic):
    return few_model.Preprocessor.get_one_hot_name(inputDic)


def get_province():
    nameList = []
    valueDic = {}
    with open('./province.pkl', 'rb') as fileReader:
        provinceDic = pickle.load(fileReader)
    count = 0
    for province in provinceDic:
        count += 1
        if count == 1:
            valueDic[province] = []
        else:
            valueDic[province] = ['']*len(nameList)
        for info in provinceDic[province]:
            for date in provinceDic[province][info]:
                thisName = '{}_{}'.format(info, date)
                thisValue = provinceDic[province][info][date]
                if count == 1:
                    nameList.append(thisName)
                    valueDic[province].append(thisValue)
                else:
                    valueDic[province][nameList.index(thisName)] = thisValue
    valueDic[''] = ['']*len(nameList)
    return nameList, valueDic


if __name__ == '__main__':
    userProfilePath = sys.argv[1]
    outUserProfile = sys.argv[2]
    provinceName, provinceValue = get_province()
    #
    count = 0
    fileWriter = open(outUserProfile, 'wb')
    with open(userProfilePath, 'rb') as fileReader:
        while True:
            stringLine = fileReader.readline()
            if stringLine:
                count += 1
                stringList = stringLine.strip().decode('utf8').split(',')
                if count == 1:
                    outString = '{},{},{},{},{},{},{}'.format(
                            'userid',
                            'useridUse',
                            get_hot_name(genderDic),
                            get_hot_name(provinceDic),
                            get_hot_name(ageDic),
                            provinceName,
                            'ageNum',
                            )
                else:
                    outString = process_list(stringList, provinceValue)
                fileWriter.write(
                        '{}\n'.format(outString).encode('utf8')
                        )
            else:
                break
