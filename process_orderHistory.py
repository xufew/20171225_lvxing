# =======================
# -*- coding: utf-8 -*-
# author: LONGFEI XU
# Try your best
# ============
import sys
import pickle

import few_model


def process_line(stringList, userDic, cityPer, countryPer, continentPer):
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
    # 所去城市，州，大陆的概率
    if city in cityPer:
        userDic[userId]['cityPer'] = cityPer[city]
    if country in countryPer:
        userDic[userId]['countryPer'] = countryPer[country]
    if continent in continentPer:
        userDic[userId]['continentPer'] = continentPer[continent]
    # 不同时间去的不同城市
    userDic[userId]['timeGoDic'][orderTime] = {
            'city': city, 'country': country, 'continent': continent
            }


def __init_user():
    outDic = {
            'orderNum': 0,          # 所下总订单数量
            'superNum': 0,          # 精品订单数量
            'continentDic': {},     # 旅游去过的大陆
            'nearestTime': 0,       # 最近下单时间
            'nearSuper': 0,         # 最近一次下单是否为精品订单
            'simpleNum': 0,         # 普通单数量
            'cityPer': '',
            'countryPer': '',
            'continentPer': '',
            'timeGoDic': {},        # 不同时间去的不同地方
            }
    return outDic


def read_go_dic():
    '''
    获取去city,country,continent的不同概率
    '''
    with open('./continent.pkl', 'rb') as fileReader:
        continent = pickle.load(fileReader)
    with open('./country.pkl', 'rb') as fileReader:
        country = pickle.load(fileReader)
    with open('./city.pkl', 'rb') as fileReader:
        city = pickle.load(fileReader)
    return city, country, continent


def read_go_key():
    '''
    读取每个城市对应的值key
    '''
    with open('./continent_key.pkl', 'rb') as fileReader:
        continent = pickle.load(fileReader)
    with open('./country_key.pkl', 'rb') as fileReader:
        country = pickle.load(fileReader)
    with open('./city_key.pkl', 'rb') as fileReader:
        city = pickle.load(fileReader)
    return city, country, continent


if __name__ == '__main__':
    orderHistoryPath = sys.argv[1]
    outPath = sys.argv[2]
    cityPer, countryPer, continentPer = read_go_dic()
    cityKey, countryKey, continentKey = read_go_key()
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
                process_line(
                        stringList,
                        userDic,
                        cityPer,
                        countryPer,
                        continentPer,
                        )
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
                    'cityPer',
                    'countryPer',
                    'continentPer',
                    few_model.Preprocessor.get_one_hot_name(
                        cityKey, 'finalGoCity_'
                        ),
                    few_model.Preprocessor.get_one_hot_name(
                        countryKey, 'finalGoCity_'
                        ),
                    few_model.Preprocessor.get_one_hot_name(
                        continentKey, 'finalGoCity_'
                        ),
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
        # 去的不同城市的编码
        timeSort = sorted(infoDic['timeGoDic'].keys())
        finalGoCity = infoDic['timeGoDic'][timeSort[-1]]['city']
        finalGoCountry = infoDic['timeGoDic'][timeSort[-1]]['country']
        finalGoContinent = infoDic['timeGoDic'][timeSort[-1]]['continent']
        finalGoCity = few_model.Preprocessor.one_hot(cityKey, finalGoCity)
        finalGoCountry = few_model.Preprocessor.one_hot(
                countryKey, finalGoCountry
                )
        finalGoContinent = few_model.Preprocessor.one_hot(
                continentKey, finalGoContinent
                )
        outList = [
                userId,
                str(orderNum),
                str(superNum),
                str(superPer),
                str(nearSuper),
                str(simpleNum),
                str(simpleNum/float(orderNum)),
                str(infoDic['cityPer']),
                str(infoDic['countryPer']),
                str(infoDic['continentPer']),
                str(finalGoCity),
                str(finalGoCountry),
                str(finalGoContinent),
                ]
        fileWriter.write(
                '{}\n'.format(','.join(outList)).encode('utf8')
                )
