# -*- coding:utf-8 -*-
import urllib
from urllib.request import urlopen, Request
from urllib.parse import urlencode
import sys
import ssl
import json
from pprint import pprint


def get_token_key():
    token_key = ''
    client_id = 'your id'  # API key
    client_secret = 'your secret'  # Secret key

    host = f'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials' \
        f'&client_id={client_id}&client_secret={client_secret}'

    request = Request(host)
    request.add_header('Content-Type', 'application/json; charset=UTF-8')
    response = urlopen(request)
    token_content = response.read()
    if token_content:
        token_info = json.loads(token_content)
        token_key = token_info['access_token']
    return token_key


def nlp_result(text, token_key, index=0, way='poem'):
    assert way in ['poem', 'couplets'], 'type should be poem or couplet'
    request_url = f'https://aip.baidubce.com/rpc/2.0/nlp/v1/{way}'

    params_d = dict()
    params_d['text'] = text
    params_d['index'] = index
    params = json.dumps(params_d).encode('utf-8')
    access_token = token_key
    request_url = request_url + "?access_token=" + access_token
    request = Request(url=request_url, data=params)
    request.add_header('Content-Type', 'application/json')
    response = urlopen(request)
    content = response.read()
    if content:
        data = json.loads(content)
        if way == 'couplets':
            center = data['couplets']['center']
            first = data['couplets']['first']
            second = data['couplets']['second']
            return center, first, second
        else:
            title = data['poem'][0]['title']
            poem = data['poem'][0]['content'].replace('\t', '\n')
            return title, poem


# token_key = 'put your token_key here'  # get_token_key()
# print(token_key)
# center, first, second = nlp_result('春节', token_key, way='couplets')
# title, poem = nlp_result('春节', token_key, way='poem')
