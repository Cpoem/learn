# -*- coding:utf-8 -*-
# author:勤奋的大眼仔
# time:2020/6/18
'''爬取安居客网站深圳城市福田区20个小区过去3年每月的房价信息，https://shenzhen.anjuke.com/community/futian/，
偏移量为1，这个脚本只爬取第一页前20个小区下钻'''
import re
import requests
import json
import time
import pandas as pd
from requests.exceptions import RequestException


def get_one_page(url):
    # 获取网页源代码
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0(Macintosh;Intel Mac OS X 10_11_4) AppleWebkit/537.36(KHTNML,like Gecko)Chrome/52.0.2743.116 Safari/537.36'}  # 请求头
        data = {'username': 'your_name', 'pwd': 'your_password'}
        response = requests.get(url, headers=headers, data=data)
        response.encoding = 'utf-8'
        if response.status_code == 200:  # 状态码为200，请求成功
            return response.text
        return None
    except RequestException:
        return None


def get_district_comm(html):
    pattern = re.compile(
        '<a hidefocus="true" target="_blank" alt="(.*?)"' + '.*?title.*?href="https://shenzhen.anjuke.com/community/view/(.*?)"',
        re.DOTALL)
    msg = re.findall(pattern, html)
    return dict(msg)


def get_data(html):
    pattern = re.compile('data : \{"status":"ok","community":\[(.*?)\]', re.DOTALL)
    items = re.findall(pattern, html)  # string类型
    list1 = items[0].split(',')
    if re.findall('commName   : "(.*?)"', html):
        community_name = re.findall('commName   : "(.*?)"', html)[0]
    for i in list1:
        dt, price = re.findall('"(\d+)":"(\d+)"', i)[0]
        #         print(dt,price)
        #             yield [item[0]+'/'+item[1],item[2]]
        yield {'community': community_name, 'date': dt, 'price': price

        }  # 遍将它赋值为一个字典，形成结构化数据


def write_to_file(content):
    with open('20_community.json', 'a', encoding='utf-8') as f:
        f.write(json.dumps(content, ensure_ascii=False) + '\n')


def main(comm_id):
    url = f'https://shenzhen.anjuke.com/community/trends/{comm_id}'
    html = get_one_page(url)
    for content in get_data(html):  # 访问生成器，写入文件
        with open('nanshan_communities', 'a', encoding='utf-8') as f:
            f.write(json.dumps(content, ensure_ascii=False) + '\n')


if __name__ == '__main__':
    html1 = get_one_page('https://shenzhen.anjuke.com/community/nanshan/')
    dic = get_district_comm(html1)
    #     print(html1)
    #     print(dic)
    comm_list = list(dic.keys())
    print('comm_list', comm_list)
    for comm_name in comm_list[0:10]:
        comm_id = dic[comm_name]
        main(comm_id=comm_id)
        time.sleep(5)
