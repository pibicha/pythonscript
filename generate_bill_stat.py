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
    get_all_stat_by_cmpId = """select stat_id from tbl_cmp_fund_bill_stat
                                where cmp_id = %s 
                                order by create_time""" % cmpId

    get_all_statementId = """
                            select statement.clear_id from tbl_cmp_fund_statement as statement
                            where cmp_id = %s
                            order by statement.create_time
    """ % cmpId

    get_max_date = """
                                select start_date from tbl_cmp_fund_bill_stat
                                where cmp_id = %s 
                                order by start_date desc LIMIT 1
                    """ % cmpId

    conn = getConnection()
    cursor = conn.cursor()

    cursor.execute(get_all_stat_by_cmpId)
    all_statId = cursor.fetchall()

    cursor.execute(get_all_statementId)
    all_statementId = cursor.fetchall()

    cursor.execute(get_max_date)
    max_date = cursor.fetchone()[0]

    # print all_statementId
    # print max_date + datetime.timedelta(days=1)

    start_date = max_date

    startDays = []
    for col in range(len(all_statId)):
        stat_id = all_statId[col][0]
        startDays.append(start_date)
        next_day = start_date + datetime.timedelta(days=1)

        # print start_date.strftime("%Y-%m-%d"), next_day.strftime("%Y-%m-%d")

        updateStat = """
                        update tbl_cmp_fund_bill_stat set
                        start_date = '%s',end_date = '%s'
                        where stat_id = %s
        """ % (start_date.date().strftime("%Y-%m-%d"), next_day.date().strftime("%Y-%m-%d"), stat_id)
        cursor.execute(updateStat)

        conn.commit()

        start_date = next_day

    for col in range(len(all_statementId)):
        updateStatement = """
                               update tbl_cmp_fund_statement set
                               create_time = '%s'
                               where clear_id = %s
               """(startDays[col], cmpId)

        statementId = all_statementId[col][0]
        # print statementId
        # print startDays[col]

        cursor.execute(updateStat)
        conn.commit()


if __name__ == '__main__':
    generateBillStat(10170106)
