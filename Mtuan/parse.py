# -*- coding:utf-8 -*-

from config import HOST
from common import get_md5
import re

def parse_json(info):
    """解析JSON"""
    data = dict()
    detail_url = 'http://meituan.com/meishi/{id}/'.format(host=HOST[-1], id=info['poiId'])
    data['id'] = get_md5(detail_url)
    data['detail'] = detail_url
    data['title'] = info['title']

    data['avgprice'] = info['avgPrice']
    data['avgscore'] = info['avgScore']
    data['comments'] = info['allCommentNum']
    data['frontimg'] = info['frontImg']
    data['address'] = info['address']
    return data