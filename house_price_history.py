# -*- coding:utf-8 -*- 
# author:勤奋的大眼仔
# time:2020/6/18
'''爬取安居客网站深圳城市每个区域过去9年每月的房价信息'''
'''网页格式为为http://www.anjuke.com/fangjia/shenzhen2020/longgang   需要根据年份和区域分页爬取，年份偏移量为1'''

import re
import requests
import json
import time
from requests.exceptions import RequestException

def get_one_page(url):
    '''获取网页源代码'''
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0(Macintosh;Intel Mac OS X 10_11_4) AppleWebkit/537.36(KHTNML,like Gecko)Chrome/52.0.2743.116 Safari/537.36'}  # 请求头
        response = requests.get(url, headers=headers)
        response.encoding = 'utf-8'
        if response.status_code == 200:  # 状态码为200，请求成功
            return response.text
        return None
    except RequestException:
        return None


def get_district(html):
    '''解析页面,获取各个区域 和对应的安居客链接'''
    url = 'https://www.anjuke.com/fangjia/shenzhen{}/'.format('2020')
    html = get_one_page(url)
    pattern = re.compile('<a href="(http://www.anjuke.com/fangjia/shenzhen2020/[a-z]{0,})/">([^0-9].*?)</a>', re.DOTALL)
    items = re.findall(pattern, html)
    dic = {}
    for tu in items:
        if '周边' not in tu[1]:  # 除去"深圳周边"的属性
            dic[tu[1]] = tu[0]
    return dic


def parse_one_page(html):
    '''解析页面，正则匹配月份和房价'''
    pattern = re.compile('<b>(.*?)年(.*?)月.*?<span>(.*?)元', re.DOTALL)
    items = re.findall(pattern, html)
    pattern1 = re.compile("<!-- 价格趋势 -->.*?年(.*?)房价走势", re.DOTALL)
    if re.findall(pattern1, html):
        district = re.findall(pattern1, html)[0]
    if items:
        for item in items:
            yield [district, item[0] + '/' + item[1], item[2]]
    return items


def write_to_file(content):
    '''写入文件'''
    with open('fangjia.txt', 'a', encoding='utf-8') as f:
        f.write(json.dumps(content, ensure_ascii=False) + '\n')

def main(url):
    html = get_one_page(url)
    items = parse_one_page(html)
    for item in items:  # 访问生成器，写入文件
        print(item)
        write_to_file(item)


if __name__ == '__main__':
    dic = get_district('http://www.anjuke.com/fangjia/shenzhen2020/')
    district = list(dic.keys())
    print(district)
    for i in district:
        url = dic[i]
        for y in range(2011, 2021, 1):
            year = re.findall('\d+', url)[0]
            new_url = url.replace(year, str(y))
            try:
                main(new_url)
                time.sleep(4)
            except Exception as e:
                print(e)