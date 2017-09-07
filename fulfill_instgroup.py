# -*- coding: utf-8 -*-
import sys

import pymysql

"""
由于tbl_he_package新增support_inst_group，默认值为空；
后续逻辑需要使用该字段会报错，故通过该脚本设置该字段
"""
reload(sys)
sys.setdefaultencoding('utf8')

dbHost = "192.168.1.20"
dbUser = "z"
dbPasswd = "z"


# 获取数据库连接
def getConnection():
    conn = pymysql.connect(host=dbHost, user=dbUser, passwd=dbPasswd, db="tahiti", charset="utf8", port=3306)
    return conn


# 获取所有连锁机构
def get_all_group():
    conn = getConnection()
    cursor = conn.cursor()
    sql = "select inst_group_id from tbl_institution_group"
    cursor.execute(sql)
    all_group = cursor.fetchall()
    # print [outer[0] for outer in all_group]
    return [outer[0] for outer in all_group]


# 获取所有连锁下的机构
def get_all_inst(group):
    conn = getConnection()
    cursor = conn.cursor()
    sql = "select inst_id from tbl_institution where inst_group_id = (%s)" % group
    cursor.execute(sql)
    all_inst = cursor.fetchall()
    # print [outer[0] for outer in all_inst]
    return [outer[0] for outer in all_inst]


# 将group作为key，旗下的insts作为value
def concat_group_inst():
    all_group = get_all_group()
    group_inst = {}
    for group in all_group:
        insts = get_all_inst(group)
        group_inst[group] = insts
    return group_inst

# 获取所有套餐，将support_inst_group字段回填上去
def fulfill_inst_group():
    conn = getConnection()
    cursor = conn.cursor()

    # 获取所有套餐及其inst
    sql = "select pack_id,support_inst from tbl_he_package"
    cursor.execute(sql)
    all_pack = cursor.fetchall()
    pack_inst={}
    for pack in all_pack:
        packs = pack[1].split(",")
        packs = map(int,packs)
        pack_inst[pack[0]] = packs

    # 获取所有套餐及旗下机构
    group_inst = concat_group_inst()

    # 将每个套餐中各自支持的inst，与所有连锁的机构对比，获取groupId
    for packId,insts in pack_inst.iteritems():
        print "套餐Id:",packId
        groups = find_group_by_inst(insts)
        print groups
        fulfill_group = "update tbl_he_package set support_inst_group='%s' where pack_id='%s'" % (groups,packId)
        cursor.execute(fulfill_group)
        conn.commit()


    return pack_inst

# 找出套餐支持的机构都属于哪些连锁
def find_group_by_inst(insts):
    insert_group=""
    group_inst = concat_group_inst()
    for group,instInGroup in group_inst.iteritems():
        if len(set(insts) & set(instInGroup)) > 0:
            insert_group = insert_group + str(group) + ","
        if set(insts) - set(instInGroup) <= 0:
            break
    return insert_group



if __name__ == '__main__':
    pack_inst = fulfill_inst_group()
