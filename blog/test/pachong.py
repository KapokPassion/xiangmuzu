import requests
from lxml import etree
header={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36"
    }
def get_html(url):
    html = requests.get(url, headers={'User-Agent':'headers'})
    html.encoding = html.apparent_encoding
    return html.text
def parse_html(html,wea):
    html_element = etree.HTML(html)
    provinces = html_element.xpath('//div[@class="conMidtab"][1]//div[@class="conMidtab2"]')
    for province in provinces:
        trs = province.xpath('.//tr')[2:3]
        for tr in trs:
            weather = {}
            city = tr.xpath('.//td[@width="83"]/a/text()')
            hightest = tr.xpath('.//td[@width="92"]/text()')
#             lowest = tr.xpath('.//td[@width="86"]/text()')
            weather['name'] = city
            weather['value'] = hightest
#             weather['lowest'] = lowest
            wea.append(weather)

def parse_html2(html,wea):
    html_element = etree.HTML(html)
    provinces = html_element.xpath('//div[@class="conMidtab"][1]//div[@class="conMidtab2"]')
    for province in provinces:
        trs = province.xpath('.//tr')[2:3]
        for tr in trs:
            weather = {}
            city = tr.xpath('.//td[@width="83"]/a/text()')
            lowest = tr.xpath('.//td[@width="86"]/text()')
            weather['name'] = city
            weather['value'] = lowest
            wea.append(weather)



def crawler():
    wea=[]
    urls = ['http://www.weather.com.cn/textFC/hb.shtml',
             'http://www.weather.com.cn/textFC/db.shtml',
             'http://www.weather.com.cn/textFC/hd.shtml',
             'http://www.weather.com.cn/textFC/hz.shtml',
             'http://www.weather.com.cn/textFC/hn.shtml',
             'http://www.weather.com.cn/textFC/xb.shtml',
             'http://www.weather.com.cn/textFC/xn.shtml',]
    for url in urls:
        html = get_html(url)
        if html == 0:
            html = get_html(url)
        parse_html(html, wea)
    return wea

def crawler2():
    wea=[]
    urls = ['http://www.weather.com.cn/textFC/hb.shtml',
             'http://www.weather.com.cn/textFC/db.shtml',
             'http://www.weather.com.cn/textFC/hd.shtml',
             'http://www.weather.com.cn/textFC/hz.shtml',
             'http://www.weather.com.cn/textFC/hn.shtml',
             'http://www.weather.com.cn/textFC/xb.shtml',
             'http://www.weather.com.cn/textFC/xn.shtml',]
    for url in urls:
        html = get_html(url)
        if html == 0:
            html = get_html(url)
        parse_html2(html, wea)
    return wea