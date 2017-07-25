# !/usr/bin/python
# -*- coding: utf-8 -*-
import urllib, urllib2, cookielib, threading, sys, time, base64, binascii, md5, xml.etree.ElementTree as ET
import demjson
import redis
from functools import wraps
from collections import OrderedDict

dom = "http://dev.feellike21.com/tahiti/cms/v1/hePackage"


# logfile = open("./test_interface_configure.log", "w+")

# 获取token的装饰器，如果没有登录，会要求先登录~~~
def tokenRequired(**kwargs):
    def media(f):
        @wraps(f)
        def wrapper(*args, **kw):
            PREFIX_CMS_ACCESS_TOKEN = "ACCESS_TOKEN:CMS:"
            r = redis.Redis(host='192.168.1.30', port=6379, db=2, password='feellike21')
            token = r.get(PREFIX_CMS_ACCESS_TOKEN + str(kwargs['opId']))
            # 将token设置到被装饰函数的关键字参数中，此处不能使用可变参数赋值~~
            kw['token'] = token
            if token is None:
                print "token失效，先在网页端登录~！"
                return
            return f(*args, **kw)

        return wrapper

    return media


def caseRunner(TestCase, token):
    for i in range(0, len(TestCase)):
        parlist = TestCase[i]
        requrl = dom + parlist['name']

        if parlist['method'] == 'GET':
            for key in parlist:
                if key == 'name' or key == 'method' or key == 'expect result' or key == 'comment':  # 这些字段是用于调试的，不需要设置到url中
                    continue
                else:
                    if requrl.endswith('/'):  # 如果url最后一位是/，证明是占位符的请求方式
                        requrl += str(parlist[key])
                    else:
                        if not '?' in requrl:
                            requrl += '?'
                        requrl = requrl + key + '=' + str(parlist[key]) + '&'
                requrl = requrl.rstrip('&')
        else:
            params = dict()
            if requrl.endswith('/'):  # 如果url最后一位是/，证明是占位符的请求方式
                for k in parlist:
                    if 'id' in k or 'Id' in k or 'ID' in k:
                        requrl += str(parlist[k])
                        parlist.pop(k)
                        print requrl
                        break
            for key in parlist:
                if key == 'name' or key == 'method' or key == 'expect result' or key == 'comment':  # 这些字段是用于调试的，不需要设置到url中
                    continue

                params[key] = parlist[key]

        # print 'requrl = ', requrl
        if parlist['method'] == 'POST':
            data = urllib.urlencode(params)
            print data
            req = urllib2.Request(url=requrl, data=data)
            req.add_header("token", token)
            response = urllib2.urlopen(req).read()
        else:
            req = urllib2.Request(requrl)
            req.add_header("token", token)
            response = urllib2.urlopen(req).read()
        comment = parlist['comment']

        print comment, 'response is', response
        assertequal(parlist['expect result'], response, requrl, comment)


@tokenRequired(opId=5)
def request1(token):
    TestCase = [{'name': '/getHePakageInfoByHepackIdV1_1/', 'method': 'GET', 'comment': '调用成功', 'packageId': 100101,
                 'expect result': '1000'}
                ]
    caseRunner(TestCase, token)


@tokenRequired(opId=5)
def request2(token):
    TestCase = [{'name': '/updateRemarkByByHePaId/', 'method': 'POST', 'comment': '调用成功', 'packageId': 100177,
                 'remark': 'pbxtest0006',
                 'expect result': '1000'}
                ]
    caseRunner(TestCase, token)


def assertequal(expect, responsestr, requrl, comment):
    if demjson.decode(responsestr)["code"] == int(expect):
        pass
        # logfile.write(comment + ":" + requrl + "\t" + responsestr + "\t" + expect + "\n")
    print "$$$$$$$$$$$$$$$$$$$$$$$\n\n"


if __name__ == '__main__':
    request2()
