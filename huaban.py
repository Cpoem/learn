# -*- coding:utf-8 -*- 
# author:勤奋的大眼仔
# time:2020/6/20
import re
import requests
import time
from requests.exceptions import RequestException


def get_one_page(url):
    # 获取网页源代码
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0(Macintosh;Intel Mac OS X 10_11_4) AppleWebkit/537.36(KHTNML,like Gecko)Chrome/52.0.2743.116 Safari/537.36'}  # 请求头
        data = {'username': 'xxx', 'pwd': 'xxx'}
        response = requests.get(url, headers=headers, data=data)
        response.encoding = 'utf-8'
        if response.status_code == 200:  # 状态码为200，请求成功
            return response.text
        return None
    except RequestException:
        return None


def load_image(html):
    # 获取pin_id,key,图片类型type
    msg = re.findall('{"pin_id":(\d+),.*?"file":{.*?key":"(.*?)".*?"type":"image/(.*?)".*?}', html)
    images = []
    for i in msg:
        info = {}
        info['id'] = re.findall('(\d+).*?', i[0])[0]
        info['key'] = i[1]
        info['type'] = i[2]
        image_url = 'https://hbimg.huabanimg.com/{}_fw658/format/webp'.format(info['key'])
        info['url'] = image_url
        images.append(info)
    # 打开图片地址，保存图片到本地
    for image in images:
        req = requests.get(image['url'])
        imageName = image["id"] + "." + image["type"]
        path = r"C:\HUABAN\早餐\\"
        with open(path + imageName, 'wb') as fp:
            fp.write(req.content)

def main(page_number):
    html = get_one_page('https://huaban.com/search/?q=新西林景观')
    q = re.findall('app.page.*?= "/search/\?q=(.*?)"', html)[0]
    url = f'https://huaban.com/search/?q={q}'
    p_url = f'{url}&page={page_number}&per_page=20&wfl=1'
    print(p_url)
    p_html = get_one_page(p_url)
    load_image(p_html)


if __name__ == '__main__':
    for i in range(1, 20, 1):
        main(page_number=i)
        time.sleep(15)

