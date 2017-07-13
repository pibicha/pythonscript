# -*- coding: utf-8 -*-
import sys
import pymysql

reload(sys)
sys.setdefaultencoding('utf8')

import sys




def getConnection():
    conn = pymysql.connect(host=dbHost, user=dbUser, passwd=dbPasswd, db="tahiti", charset="utf8", port=3306)
    return conn


def updateReserveByMobile(mobile, status):
    sql = """select 
            reserve.he_id as reserveid
            from tbl_cmp_he_invitation invite
            left join tbl_he_reserve reserve
            on reserve.he_id = invite.reserve_id
            left JOIN tbl_user_payment payment
            on payment.item_id = invite.id
            left join tbl_user_refund refund
            on refund.pay_id = payment.pay_id
            where invite.mobile = '%s'
            and invite.`status`=1 and payment.`status`=1
            order by invite.create_time desc
            LIMIT 1""" % mobile
    conn = getConnection()
    cursor = conn.cursor()
    cursor.execute(sql)
    row = cursor.fetchone()
    if row is None:
        print "you have no reserve with mobile： ", mobile
        return
    reserveId = row[0]

    update = "update tbl_he_reserve set status=%s where he_id = %s" % (status, reserveId)
    cursor.execute(update)
    conn.commit()
    cursor.close()

    print "更新成功！"


if __name__ == '__main__':
    mobile = input("输入预约的手机号(只能更新该手机号最新的一条预约状态)：".encode("utf-8"))
    print "\n\n\n"
    status = input("0-预约 1-到检未出报告 2-已出报告,3已出PDF 4-过期 5-取消：")
    updateReserveByMobile(mobile, status)