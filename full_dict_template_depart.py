# -*- coding: utf-8 -*-
import sys

import pymysql

"""
由于tbl_he_package新增support_inst_group，默认值为空；
后续逻辑需要使用该字段会报错，故通过该脚本设置该字段
"""
reload(sys)
sys.setdefaultencoding('utf8')

dbHost = "secret"
dbUser = "secret"
dbPasswd = "secret"


# 获取数据库连接
def getConnection():
    conn = pymysql.connect(host=dbHost, user=dbUser, passwd=dbPasswd, db="tahiti", charset="utf8", port=3306)
    return conn


# 0 获取所有的机检查结果项
def get_he_log_info():
    conn = getConnection()
    cursor = conn.cursor()
    sql = """SELECT
                report.inst_id as inst_id,
                result.dict_depart as dict_depart,
                result.dict_name,
                result.unit
            FROM
                tbl_log_he_report report
            INNER JOIN tbl_log_he_result result ON report.report_code = result.report_code"""

    cursor.execute(sql)
    all_info = cursor.fetchall()
    list = []
    for outer in all_info:
        tmp_list = []
        # print outer[0],outer[1],outer[2],outer[3]
        if outer[0] is not None:
            tmp_list.append([outer[0], outer[1], outer[2], outer[3]])
            list.append(tmp_list)
    return list


# 1 获取所有连锁机构
def get_all_group():
    conn = getConnection()
    cursor = conn.cursor()
    sql = "select inst_group_id from tbl_institution_group"
    cursor.execute(sql)
    all_group = cursor.fetchall()
    # print [outer[0] for outer in all_group]
    return [outer[0] for outer in all_group]


# 2 获取所有连锁旗下的机构
def get_all_inst(group):
    conn = getConnection()
    cursor = conn.cursor()
    sql = "select inst_id from tbl_institution where inst_group_id = (%s)" % group
    cursor.execute(sql)
    all_inst = cursor.fetchall()
    # print [outer[0] for outer in all_inst]
    return [outer[0] for outer in all_inst]


# 3 将group作为key，旗下的insts作为value
def concat_group_inst():
    all_group = get_all_group()
    group_inst = {}
    for group in all_group:
        insts = get_all_inst(group)
        group_inst[group] = insts
    return group_inst


if __name__ == '__main__':

    conn = getConnection()
    cursor = conn.cursor()

    pack_inst = get_he_log_info()

    # 获取所有连锁及其旗下的机构
    group_inst = concat_group_inst()

    # 准备查询tbl_dict_template的参数
    list_param = []

    for element in pack_inst:
        for instId, dictDepart, dictName, unit in element:
            print instId, dictDepart, dictName, unit
            for group, insts in group_inst.iteritems():
                if instId in insts:
                    print "该机构属于[{}]连锁".format(group)
                    tmp_list = [group, dictDepart, dictName, unit]
                    list_param.append(tmp_list)
                    break
                else:
                    print "该[{}]机构已失效！不属于任何连锁".format(instId)
                    break
            print "\n"

    print "准备查询tbl_dict_template的参数:\n"
    for param in list_param:
        # print param[0],param[1],param[2],param[3]
        print "即将更新记录——>> institution_group_id 为 {0}," \
              "import_dic_name为{1}," \
              "import_medical_unit为{2} " \
              "的记录import_dic_depart为:{3}" \
            .format(param[0], param[1], param[2], param[3])

        update = """
                    UPDATE tbl_dict_template
                    SET import_dic_depart = '%s'
                    WHERE
                        institution_group_id = '%s'
                    AND import_dic_name = '%s'
                    AND import_medical_unit = '%s'
                """ % (param[1], param[0], param[2], param[3])
        cursor.execute(update)
        conn.commit()
