#-*- coding: utf-8 -*-
'''
Handle OAuth of yuque.
'''
import time
import random
import base64
import hmac
import urllib.parse
import hashlib
import requests

OAUTH_BASE = "https://www.yuque.com/oauth2"
CODE_ALPHABET = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"

SCOPE_SHORTCUTS = {
    "all" : [
        "group",
        "repo",
        "topic",
        "doc",
        "artboard"
    ],
    "all:read": [
        "group:read",
        "repo:read",
        "topic:read",
        "doc:read",
        "artboard:read"
    ]
}


def gen_code():
    '''Generate length 40 client code for non web mode.
    '''
    code = ''.join([random.choice(CODE_ALPHABET)\
                    for i in range(40)])
    return code


def get_signature(client_id, code, response_type, scope, timestamp, client_secret):
    digest = hmac.HMAC(client_secret.encode('utf-8'),
                       msg=('&'.join(["client_id=%s" % client_id,
                                      "code=%s" % code,
                                      "response_type=%s" % response_type,
                                      "scope=%s" % urllib.parse.quote(scope),
                                      "timestamp=%s" % timestamp])).encode('utf-8'),
                       digestmod=hashlib.sha1).digest()
    return base64.b64encode(digest).decode('utf-8')


def authorize(client_id, scope="", redirect_uri="", state="", code="", client_secret='', mode=""):
    '''
    生成用户授权访问的url

    Args:
        client_id (str): OAuth client id.
        scope: 请求的权限scope
        redirect_uri (str): mode == 'web'时传递，跳转地址，需要和OAuth应用配置中的回调地址相同。
        state (str): mode =='web'时传递，OAuth state
        code (str): mode != 'web'时传递，客户端生成的code
        client_secret (str): mode != 'web'时传递，OAuth client secret.
        mode (str): 授权的模式，'web'或者其他（非web模式）

    Returns:
        str: Authorization url.
    '''
    response_type = 'code'
    if scope in SCOPE_SHORTCUTS:
        scope = ','.join(SCOPE_SHORTCUTS[scope])
    if isinstance(scope, (list, tuple)):
        scope = ','.join(scope)
    params = {
        "client_id": client_id,
        "scope": scope,
        "response_type": response_type
    }
    if mode == "web":
        params["redirect_uri"] = redirect_uri
        params["state"] = state
    else:
        timestamp = str(int(time.time() * 1000))
        sign = get_signature(client_id, code, response_type, scope, timestamp, client_secret)
        params.update({"code": code,
                       "timestamp": timestamp,
                       "sign": sign})
    return "%s/authorize?%s" % (OAUTH_BASE, urllib.parse.urlencode(params))


def get_access_token(client_id, code, client_secret='', grant_type=''):
    '''通过授权码获取access token
    '''
    params = {
        "client_id": client_id,
        "code": code,
        "grant_type": grant_type
    }
    if grant_type == 'client_code':
        pass
    elif grant_type == 'authorization_code':
        params['client_secret'] = client_secret
    else:
        raise Exception("Unknown grant_type %s." % grant_type)
    headers = {'User-Agent': 'pyuque'}
    resp = requests.post("%s/token" % OAUTH_BASE,
                         json=params, headers=headers, timeout=60)
    return resp.json()
