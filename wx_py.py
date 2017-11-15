# -*- coding: utf-8 -*-
import os
import sys
from datetime import datetime, timedelta
from random import randint

import pymysql

reload(sys)
sys.setdefaultencoding('utf8')

dbHost = "XXX"
dbUser = "XXX"
dbPasswd = "XXX"
reserve_file_path = r'XXX'


# 获取数据库连接
def getAndExecute(sql):
    conn = pymysql.connect(host=dbHost, user=dbUser, passwd=dbPasswd, db="tahiti", charset="utf8", port=3306)
    cursor = conn.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    conn.commit()
    conn.close()
    return result


# 获取线下机构，排除爱康和慈名
def subway_institution():
    sql = """select name from tbl_institution
            where 
            inst_group_id not in (4,3,2,1)"""
    result = getAndExecute(sql)
    result_list = [outer[0].encode("utf-8") for outer in result]
    return result_list


# 获取明天应该发送的预约文件
def tomorrow_reserve(insts):
    tomorrow = datetime.now() + timedelta(days=1)
    # 理论上需要发送的邮件，不一定真的在instReserve目录上存在！
    idea_files = []
    # 文件名例子： (体检日期：2017年10月25日)北京大学首钢医院.xls
    for inst in insts:
        file_name = "(体检日期：{0}){1}.xls".format(tomorrow.strftime("%Y年%m月%d日"), inst)
        # print file_name
        idea_files.append(file_name)

    return dict(zip(idea_files, insts))


# 从存放预约文件的目录获取已有的文件
def exist_files(should_emit_files):
    could_emit_files = []
    files = os.listdir(reserve_file_path)
    if files:
        for file in files:
            file_name = file.decode('utf-8')  # 针对window而言！！
            # print file_name
            if file_name in should_emit_files:
                could_emit_files.append(file_name)

    return could_emit_files


if __name__ == '__main__':

    from itchat import *
    import time

    auto_login(hotReload=True, enableCmdQR=2)

    now_time = time.time()
    now_time = time.localtime(now_time)

    # time.struct_time(tm_year=2017, tm_mon=10, tm_mday=27, tm_hour=18, tm_min=21, tm_sec=25, tm_wday=4, tm_yday=300, tm_isdst=0)


    if now_time.tm_hour == 14 and now_time.tm_min == 1:
        from multiprocessing.dummy import Pool

        pool = Pool()
        args = []

        inst_files_map = tomorrow_reserve(subway_institution())
        could_emit_files = exist_files(inst_files_map.keys())
        for emit_file in could_emit_files:
            # print e.encode('utf-8')
            emit_file = emit_file.encode('utf-8')
            inst_name = inst_files_map.get(emit_file).encode('utf-8')
            # print emit_file, inst_name
            print inst_name
            friends = search_friends(name=inst_name)
            if len(friends) == 0:
                print 'no user named %s in your friendList' % inst_name
                continue
            else:
                friend = friends[0]
            file_in_path = reserve_file_path + emit_file

            print file_in_path
            # IO密集，使用多线程发送消息send_file(file_in_path.decode('utf-8'), toUserName=friend.get('UserName'))
            arg = pool.apply_async(send_file, (file_in_path.encode('utf-8'),),
                                   kwds={'toUserName': friend.get('UserName')})
            args.append(arg)
        pool.close()
        pool.join()
        time.sleep(60)
        exit(0)
    if now_time.tm_min % 1 == 0:
        send_msg(randint(1, 100000))
        time.sleep(60)
        exit(0)
