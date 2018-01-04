# =======================
# -*- coding: utf-8 -*-
# author: LONGFEI XU
# Try your best
# ============
import pickle


provinceList = [
        '北京', '浙江', '甘肃', '安徽', '贵州', '吉林', '四川',
        '江苏', '福建', '新疆', '上海', '海南', '天津', '重庆',
        '云南', '青海', '内蒙古', '湖北', '河北', '西藏', '黑龙江',
        '河南', '广西', '陕西', '山东', '广东', '湖南', '山西',
        '江西', '辽宁', '宁夏',
        ]


transDic = {
        '地区生产总值(亿元)': '国内生产总值(亿元)',
        '年末常住人口(万人)': '年末总人口(万人)',
        '社会消费品零售总额(亿元)': '社会商品零售总额(亿元)',
        }


def return_info():
    countInfo = {
            '国内生产总值(亿元)': {'2015年': '', '2014年': ''},
            '社会商品零售总额(亿元)': {'2015年': '', '2014年': ''},
            '年末总人口(万人)': {'2015年': '', '2014年': ''},
            '居民消费价格指数(上年同月=100)': {'2017年11月': ''},
            '商品零售价格指数(上年同月=100)': {'2017年11月': ''},
            '工业生产者出厂价格指数(上年同月=100)': {'2017年11月': ''},
            }
    return countInfo


if __name__ == '__main__':
    inputPath = './provinceInfo'
    with open(inputPath, 'rb') as fileReader:
        provinceDic = {}
        while True:
            stringLine = fileReader.readline()
            if stringLine:
                stringList = stringLine.strip().decode('utf8').split('\t')
                province = stringList[0]
                info = stringList[1]
                date = stringList[3]
                value = stringList[2]
                if province not in provinceDic:
                    provinceDic[province] = return_info()
                if info in transDic:
                    info = transDic[info]
                if info in provinceDic[province]:
                    if date in provinceDic[province][info]:
                        if value.strip() != '':
                            provinceDic[province][info][date] = value
            else:
                break
    with open('province.pkl', 'wb') as fileWriter:
        pickle.dump(provinceDic, fileWriter)
