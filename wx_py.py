# -*- coding: utf-8 -*-
import os
import sys
from datetime import datetime, timedelta

import pymysql

"""
由于tbl_he_package新增support_inst_group，默认值为空；
后续逻辑需要使用该字段会报错，故通过该脚本设置该字段
"""
reload(sys)
sys.setdefaultencoding('utf8')




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
            file_name = file.decode('gbk')
            # print file_name
            if file_name in should_emit_files:
                could_emit_files.append(file_name)

    return could_emit_files


if __name__ == '__main__':

    # 导入微信模块
    from wxpy import *

    # 初始化机器人，扫码登陆
    bot = Bot(console_qr=1, cache_path=True)

    inst_files_map = tomorrow_reserve(subway_institution())
    could_emit_files = exist_files(inst_files_map.keys())
    for emit_file in could_emit_files:
        # print e.encode('utf-8')
        emit_file = emit_file.encode('utf-8')
        inst_name = inst_files_map.get(emit_file).encode('utf-8')
        # print emit_file, inst_name
        friend = bot.friends().search(inst_name.decode('utf-8'))[0]
        file_in_path = reserve_file_path + emit_file

        print file_in_path
        friend.send_file(file_in_path)
