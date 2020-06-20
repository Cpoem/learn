# -*- coding:utf-8 -*- 
# author:勤奋的大眼仔
# time:2020/6/20
import re
import requests
import json
from requests.exceptions import RequestException

'''网页为https://huaban.com/search/?q=xxxxx  '''


def get_one_page(url):
    # 获取网页源代码
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0(Macintosh;Intel Mac OS X 10_11_4) AppleWebkit/537.36(KHTNML,like Gecko)Chrome/52.0.2743.116 Safari/537.36'}  # 请求头
        data = {'username': 'user_chen', 'pwd': 'chen2314'}
        response = requests.get(url, headers=headers, data=data)
        response.encoding = 'utf-8'
        if response.status_code == 200:  # 状态码为200，请求成功
            return response.text
        return None
    except RequestException:
        return None


def parse_one_page(html):
    # 解析页面
    pattern = re.compile(
        '<li class="shop-infoo-list-item clearfix.*?h3.*?shop-infoo-list-item-title">(.*?)</h3>' + '.*?</span><span class.*?gold.*?style.*?>(.*?)</span>' + '.*?<a href.*?span class.*?target="_blank">.*?item-line-label">(.*?)</span>' + '.*?item-line-label">(.*?)</span>' + '.*?</a>.*?</li>',
        re.S)  # re.S
    items = re.findall(pattern, html)
    for item in items:
        yield {'店铺名': item[0], '评分': item[1], '人均消费（元）': item[2], '地区': item[3]

        }  # 遍历提取店铺名，人均消费，评分和地点，将它赋值为一个字典，形成结构化数据


def write_to_file(content):
    with open('百度糯米-甜品店.txt', 'a', encoding='utf-8') as f:
        f.write(json.dumps(content, ensure_ascii=False) + '\n')


def main():
    url = 'https://huaban.com/search/?q=新西林景观'
    html = get_one_page(url)
    for item in parse_one_page(html):  # 访问生成器，以json字典格式写入文件
        print(item)
        write_to_file(item)


# if __name__=='__main__':
#     for i in range(1,9,1):
#         main(page_number=i)
#         time.sleep(1)

url = 'https://huaban.com/search/?q=新西林景观'
html = get_one_page(url)
print(html)
pattern = re.compile('{"pin_id":(.*?),.*"file":{.*"key":(.*?),}', re.DOTALL)
msg = re.findall(pattern, html)
print(html)
print(msg)