# =======================
# -*- coding: utf-8 -*-
# author: LONGFEI XU
# Try your best
# ============
import urllib.parse

import few_base


provinceList = [
        '北京', '浙江', '甘肃', '安徽', '贵州', '吉林', '四川',
        '江苏', '福建', '新疆', '上海', '海南', '天津', '重庆',
        '云南', '青海', '内蒙古', '湖北', '河北', '西藏', '黑龙江',
        '河南', '广西', '陕西', '山东', '广东', '湖南', '山西',
        '江西', '辽宁', '宁夏',
        ]


def spider_page_list(provinceList):
    pageList = []
    pageView = 'http://data.stats.gov.cn/search.htm?'
    info = '&m=searchdata&db=&p=0'
    for province in provinceList:
        data = {'s': province}
        pageList.append(
                {
                    'url': '{}{}{}'.format(
                        pageView, urllib.parse.urlencode(data), info
                        ),
                    'province': province
                    }
                )
    return pageList


if __name__ == '__main__':
    # 获取所有需要爬的网页
    pageList = spider_page_list(provinceList)
    querier = few_base.HttpQuery(proxy=0)
    with open('provinceInfo', 'wb') as fileWriter:
        for page in pageList:
            result = querier.send_query(page['url'])['result']
            for infoDic in result:
                province = infoDic['reg']
                date = infoDic['sj']
                exp = infoDic['exp']
                data = infoDic['data']
                info = infoDic['zb']
                if page['province'] not in province:
                    continue
                infoList = [
                        page['province'],
                        info,
                        data,
                        date,
                        exp,
                        ]
                fileWriter.write(
                        '{}\n'.format(
                            '\t'.join(infoList)
                            ).encode('utf8')
                        )
