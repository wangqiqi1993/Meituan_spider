#  -*- coding:utf-8 -*-
import os
import pandas as pd
from token_ import encrypt_token
from urllib.parse import urlencode
from common import save,get_uuid
from parse import parse_json
import logging
import math
import json
import requests
import time
import random
import multiprocessing
from config import GET_PARAM, HEADERS, TIMEOUT, MAX_PAGES, BASE_URL
from get_cateId import *
def main(base_url, page,cateId,originUrl):
    """主函数"""
    # 添加_token参数
    GET_PARAM['cateId'] = str(cateId)
    GET_PARAM["originUrl"]=originUrl
    SIGN_PARAM = "areaId={}&cateId={}&cityName={}&dinnerCountAttrId={}&optimusCode={}&originUrl={}&page={}&partner={}&platform={}&riskLevel={}&sort={}&userId={}&uuid={}".format(
        GET_PARAM["areaId"],
        GET_PARAM["cateId"],
        GET_PARAM["cityName"],
        GET_PARAM["dinnerCountAttrId"],
        GET_PARAM["optimusCode"],
        GET_PARAM["originUrl"],
        GET_PARAM["page"],
        GET_PARAM["partner"],
        GET_PARAM["platform"],
        GET_PARAM["riskLevel"],
        GET_PARAM["sort"],
        GET_PARAM["userId"],
        GET_PARAM["uuid"]
    )
    GET_PARAM["_token"] = encrypt_token(SIGN_PARAM)
    GET_PARAM['page'] = str(page)
    url = base_url + urlencode(GET_PARAM)
    # proxies = xdaili_proxy()
    # session = requests.Session()
    # response = json.loads(session.get(url, headers=HEADERS, proxies=proxies, timeout=TIMEOUT).text)
    response = json.loads(requests.get(url, headers=HEADERS, timeout=TIMEOUT).text)
    try:
        infos = response['data']['poiInfos']
        for info in infos:
            data = parse_json(info)
            data['city'] = base_url.split('//')[-1].split('.')[0]
            data['cateId'] = GET_PARAM['cateId']
            print(data, sep='\n')
            save(data)
    except Exception as e:
        logging.warning(" Response status code: {}, Requests was found, no target data was obtained!".format(response['code']))
        _ = e

if __name__ == '__main__':
    # 多进程
    # pool = multiprocessing.Pool(multiprocessing.cpu_count())
    # for page in range(1, MAX_PAGES + 1):
    #     pool.apply_async(main, (BASE_URL, page))
    # pool.close()
    # pool.join()

    # 获取数据
    log_path = os.path.dirname(os.path.realpath(__file__)) + '\\utils\\labels.log'
    f = open(log_path)
    for file in f.readlines():
        cateId=file.split('\t')[0]
        originUrl=file.split('\t')[-1]
        GET_PARAM['cateId'] = str(cateId)
        GET_PARAM["originUrl"] = originUrl
        SIGN_PARAM = "areaId={}&cateId={}&cityName={}&dinnerCountAttrId={}&optimusCode={}&originUrl={}&page={}&partner={}&platform={}&riskLevel={}&sort={}&userId={}&uuid={}".format(
        GET_PARAM["areaId"],
        GET_PARAM["cateId"],
        GET_PARAM["cityName"],
        GET_PARAM["dinnerCountAttrId"],
        GET_PARAM["optimusCode"],
        GET_PARAM["originUrl"],
        GET_PARAM["page"],
        GET_PARAM["partner"],
        GET_PARAM["platform"],
        GET_PARAM["riskLevel"],
        GET_PARAM["sort"],
        GET_PARAM["userId"],
        GET_PARAM["uuid"]
    )
        GET_PARAM["_token"] = encrypt_token(SIGN_PARAM)
        url = BASE_URL + urlencode(GET_PARAM)
        response = json.loads(requests.get(url, headers=HEADERS, timeout=TIMEOUT).text)
        try:
            totalCounts = response['data']['totalCounts']
            MAX_PAGES=math.ceil( totalCounts/15)
        except Exception as e:
            logging.warning(" Response status code: {}, Requests was found, no target data was obtained!".format(response['code']))
            _ = e
        for page in range(1, MAX_PAGES + 1):
            main(BASE_URL, page,cateId,originUrl)
            time.sleep(random.randint(1,3))