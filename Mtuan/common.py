# -*- coding:utf-8 -*-

import requests
from pyquery import PyQuery as pq
import hashlib
import pymysql
from sqlalchemy import create_engine
import pandas as pd
import logging
import random
import json
from config import *
import re


def get_cities():
    """城市名称-拼音简写对照字典"""
    doc = pq(requests.get('https://www.meituan.com/changecity/').text)
    a_lists = doc('.cities a').items()
    cities = {}
    [cities.update({a.text(): a.attr('href').replace('.', '/').split('/')[2]}) for a in a_lists]
    print(cities)
    with open('./utils/cities.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(cities, indent=2, ensure_ascii=False))

def get_uuid():
    """获取uuid"""
    url = 'https://bj.meituan.com/meishi/'
    # url = "http://localhost:8050/render.html?url=https://bj.meituan.com/meishi/&wait=5"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36"
    }
    res = requests.get(url, headers=headers).text
    uuid = re.findall(r'"uuid":"(.*?)"', res, re.S)[0]
    with open('./utils/uuid.log', 'w') as f:
        f.write(uuid)

def save(data):
    """存储数据"""
    # engine = create_engine('mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'.format(USER, PASS, HOST, PORT, DB))
    # connect = engine.connect()
    # try:
    #     df = pd.DataFrame(data, index=[0])
    #     df.to_sql(name=TABLE, con=connect, if_exists='append', index=False)
    # except Exception as e:
    #     logging.error("\nError: %s, Please check the error.\n" % e.args)
    #     _ = e#存在小数四舍五入
    def table_exists(conn, table_name):
        sql = "show tables;"
        conn.execute(sql)
        tables = [conn.fetchall()]
        table_list = re.findall('(\'.*?\')', str(tables))
        table_list = [re.sub("'", '', each) for each in table_list]
        if table_name in table_list:
            return 1
        else:
            return 0

    conn = pymysql.connect(host='localhost', user='root', password='****', port=3306, db='test')
    cursor = conn.cursor()
    table_name = 'meishi'
    if (table_exists(cursor, table_name) != 1):
        cursor.execute('create table meishi(id varchar(100),detail varchar(200),title varchar(100),avgprice int,avgscore double(3,2),comments int,frontimg varchar(100),address varchar(200),city varchar(30),cateId varchar(10)) ENGINE=InnoDB DEFAULT character set utf8mb4 collate utf8mb4_general_ci;')
    try:
        cursor.execute("insert into meishi (id,detail,title,avgprice,avgscore,comments,frontimg,address,city,cateId) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(data['id'],data['detail'],data['title'],data['avgprice'],data['avgscore'],data['comments'],data['frontimg'],data['address'],data['city'],data['cateId']))
    except:
        pass
    conn.commit()
    cursor.close()
    conn.close()
def get_md5(url):
    """md5处理"""
    if isinstance(url, str):
        url = url.encode('utf-8')
    m = hashlib.md5()
    m.update(url)
    return m.hexdigest()
if __name__=='__main__':
    get_uuid()
