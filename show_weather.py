#!/usr/bin/python3
# 爬取相应地区的天气信息
import pymysql
import pdb
import requests
from bs4 import BeautifulSoup
import re
import json
from config import user, passwd, the_db


# 构造城市天气url
def get_weather_page(name):
    db = pymysql.connect(host="localhost", port=3306, user=user,
                         passwd=passwd, db=the_db, charset="utf8")
    # pdb.set_trace()
    cursor = db.cursor()
    sql = "select Weather_id from weather where name = '%s'" % (name)
    cursor.execute(sql)
    Weather_id = cursor.fetchone()[0]
    page = 'http://www.weather.com.cn/weather/' + Weather_id + '.shtml'
    db.close()
    return page


# 得到指定城市天气情况
def get_weather(page):
    response = requests.get(page)
    soup = BeautifulSoup(response.content, "html.parser")
    # soup2 = soup.select('ul[class="t clearfix"]')
    # soup3 = soup.find_all(class_="sky skyid lv1 on")
    weather_list = soup.find_all(class_=re.compile("skyid"))
    weather_for_json = ['', '', '']
    for i in range(0, 3):
        # pdb.set_trace()
        l1 = weather_list[i]
        weather = l1.p.string
        tem = l1.i.string
        feng = l1.find_all(class_=re.compile('win'))[0].span['title']
        l2 = l1.find_all(class_=re.compile('win'))[0].i.string
        dict1 = {'temp': str(tem), 'wind': str(
            feng)+str(l2), 'weather': str(weather)}
        weather_for_json[i] = dict1
    # pdb.set_trace()
    theall = json.dumps({'today': weather_for_json[0], 'tomorrow': weather_for_json[1],
                         'afterTwoDay': weather_for_json[2]}, ensure_ascii=False)
    return theall


if __name__ == '__main__':
    page = get_weather_page("北京")
    weather = get_weather(page)
    print(weather)
