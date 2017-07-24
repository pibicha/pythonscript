# !/usr/bin/python
# -*- coding: utf-8 -*-
import urllib, urllib2, cookielib, threading, sys, time, base64, binascii, md5, xml.etree.ElementTree as ET
import demjson
import redis
from functools import wraps

dom = "http://dev.feellike21.com/tahiti/cms/v1/hePackage"
#logfile = open("./test_interface_configure.log", "w+")


def tokenRequired(**kwargs):
    def media(f):
        @wraps(f)
        def wrapper(*args, **kw):
            PREFIX_CMS_ACCESS_TOKEN = "ACCESS_TOKEN:CMS:"
            r = redis.Redis(host='192.168.1.30', port=6379, db=2, password='feellike21')
            token = r.get(PREFIX_CMS_ACCESS_TOKEN + str(kwargs['opId']))
            kw['token'] = token
            if token is None:
                print "token失效，先在网页端登录~！"
                return
            return f(*args, **kw)

        return wrapper

    return media


@tokenRequired(opId=5)
def request1(token):  # 更新集团账户信息
    TestCase = [{'name': 'getHePakageInfoByHepackId1_1', 'comment': '调用成功', 'packageId': 100101,
                 'expect result': '1000'}
                ]
    parlist = []
    for i in range(0, len(TestCase)):
        parlist = TestCase[i]

        requrl = dom + '/getHePakageInfoByHepackIdV1_1/'

        if 'packageId' in parlist:
            packageId = parlist['packageId']
            requrl += str(packageId)

        requrl = requrl + '?token=' + token
        print 'requrl = ', requrl
        response = urllib2.urlopen(requrl).read()
        comment = parlist['comment']

        print comment, 'response is', response
        assertequal(parlist['expect result'], response, requrl, comment)


def assertequal(expect, responsestr, requrl, comment):
    if demjson.decode(responsestr)["code"] == int(expect):
        pass
        #logfile.write(comment + ":" + requrl + "\t" + responsestr + "\t" + expect + "\n")
    print "$$$$$$$$$$$$$$$$$$$$$$$\n\n"


if __name__ == '__main__':
    request1()
