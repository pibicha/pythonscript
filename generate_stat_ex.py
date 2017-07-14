# -*- coding: utf-8 -*-
import sys
import pymysql
import datetime

import urllib2

reload(sys)
sys.setdefaultencoding('utf8')

dbHost = "192.168.1.20"
dbUser = "root"
dbPasswd = "Admin@123"


def getConnection():
    conn = pymysql.connect(host=dbHost, user=dbUser, passwd=dbPasswd, db="tahiti", charset="utf8", port=3306)
    return conn


def generateBillStat(cmpId):
    get_all_statementId = """
                            select statement.clear_id from tbl_cmp_fund_statement as statement
                            where cmp_id = %s
                            order by statement.create_time
    """ % cmpId

    select_max_createtime = """
                            select statement.create_time from tbl_cmp_fund_statement as statement
                            where cmp_id = %s
                            order by statement.create_time desc limit 1
    """ % cmpId

    conn = getConnection()
    cursor = conn.cursor()

    cursor.execute(get_all_statementId)
    all_statementId = cursor.fetchall()
    # print all_statementId

    cursor.execute(select_max_createtime)
    max_createTime = cursor.fetchone()
    # print max_createTime[0].strftime("%Y-%m-%d %H:%M:%S")
    # print (max_createTime[0] + datetime.timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S")
    # print max_createTime[0].strftime("%Y-%m-%d %H:%M:%S")

    createTime = max_createTime[0]
    for statementId in all_statementId:
        updateStatement = """
                update tbl_cmp_fund_statement set create_time = '%s' WHERE clear_id = %s
            """ % (createTime.strftime("%Y-%m-%d %H:%M:%S"), statementId[0])

        startDate = createTime
        endDate = createTime + datetime.timedelta(days=1)

        # print createTime
        # print startDate.strftime("%Y-%m-%d %H:%M:%S"), endDate.strftime("%Y-%m-%d %H:%M:%S")

        cursor.execute(updateStatement)
        conn.commit()

        # print "http://192.168.1.30:9001/v1_2/cmp/fund/stat?start=" + startDate.strftime(
        #     "%Y-%m-%d%H:%M:%S") + "&end=" + endDate.strftime("%Y-%m-%d%H:%M:%S")

        # 发送请求生成账单
        urllib2.urlopen("http://192.168.1.30:9001/v1_2/cmp/fund/stat?start=" + startDate.strftime(
            "%Y-%m-%d%H:%M:%S") + "&end=" + endDate.strftime("%Y-%m-%d%H:%M:%S"))

        createTime = endDate


if __name__ == '__main__':
    generateBillStat(30)
