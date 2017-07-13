# -*- coding: utf-8 -*-
import sys
import pymysql
import datetime

reload(sys)
sys.setdefaultencoding('utf8')

dbHost = "192.168.1.20"
dbUser = "root"
dbPasswd = "Admin@123"


def getConnection():
    conn = pymysql.connect(host=dbHost, user=dbUser, passwd=dbPasswd, db="tahiti", charset="utf8", port=3306)
    return conn


def generateBillStat(cmpId):
    get_all_stat_by_cmpId = """select stat_id,start_date,end_date from tbl_cmp_fund_bill_stat
                                where cmp_id = %s 
                                order by create_time""" % cmpId

    conn = getConnection()
    cursor = conn.cursor()
    cursor.execute(get_all_stat_by_cmpId)

    row = cursor.fetchall()

    today = datetime.datetime.now()
    # print today.date()
    for col in range(len(row)):
        stat_id = row[col][0]
        start_date = today
        nextDay = today + datetime.timedelta(days=1)
        end_date = nextDay
        today = nextDay

        print start_date.date().strftime("%Y-%m-%d"), end_date.date().strftime("%Y-%m-%d")

        update = """
        update tbl_cmp_fund_bill_stat set 
        start_date = '%s',end_date = '%s'
        where stat_id = %s
        """ % (start_date.date().strftime("%Y-%m-%d"), end_date.date().strftime("%Y-%m-%d"), stat_id)
        cursor.execute(update)
        conn.commit()


if __name__ == '__main__':
    generateBillStat(30)
