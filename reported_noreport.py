# -*-coding:utf-8-*-
import os
import platform
import sys

import pymysql

reload(sys)
sys.setdefaultencoding('utf8')
dirname = os.environ.get(__name__)

"


# 获取数据库连接
def getAndExecute(sql):
    conn = pymysql.connect(host=dbHost, user=dbUser, passwd=dbPasswd, db="tahiti", charset="utf8", port=3306)
    cursor = conn.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    conn.commit()
    conn.close()
    return result


def list_report_receive(path):
    if path is None:
        path = 'D:\\Attachment'
    s = set()
    for f in os.listdir(path):
        if platform.system() == 'Windows':
            s.add(f.decode('gbk'))
        else:
            s.add(f.decode('utf-8'))
    return s


def report_in_KJD():
    sql = "select inst_report_file from tbl_he_report"
    result = getAndExecute(sql)
    list = [outer[0] for outer in result]
    rList = []
    for identity_number in list:
        if identity_number.__contains__("_"):
            continue
        # print "report in KJD DB : ", identity_number.decode('gbk')
        rList.append(identity_number)

    return set(rList)


if __name__ == '__main__':
    received = list_report_receive(None)
    reported = report_in_KJD()

    defects = received - reported
    # 存在与康健德instReturn ， 但不存在与he_report表的报告:
    print '存在于instReturn目录、 但不存在与he_report表的报告:'
    for e in defects:
        print e.decode('utf-8')
