#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
import MySQLdb

import sys

reload(sys)
sys.setdefaultencoding('utf8')

dbHost = ""
dbUser = ""
dbPasswd = ""


def getConnection():
    conn = MySQLdb.connect(host=dbHost, user=dbUser, passwd=dbPasswd, db="tahiti", charset="utf8", port=3306)
    return conn

with open(r'd:\yuanben.txt') as f:
    for line in f.readlines():
        utfline = line.decode('utf-8')
        if utfline == '' or utfline == None:
            continue
        pair = utfline.split(':')
        conn = getConnection()
        if len(pair) > 1:
            query = "select sort_id from tbl_he_sort where sort_name='%s'" % pair[0].strip()
            cursor = conn.cursor()
            cursor.execute(query)
            row = cursor.fetchone()
            if pair[1].strip() != '' and pair[1] is not None:
                print
                'logicsort_id:' + str(row[0]) + '\t' + 'sort_name:' + pair[0] + '\t dict_name:' + pair[1]
                try:
                    insertsql = "insert into tbl_he_sort_dict(sort_id,dict_name) values('%s','%s')" % (
                        row[0], pair[1].strip())
                    cursor.execute(insertsql)
                    cursor.close()
                except MySQLdb.Error, e:
                    print e
        conn.commit()
        conn.close()
