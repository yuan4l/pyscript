#encoding=utf-8
import sys
sys.path.append('..')

from base.dao import Dao
import json

soCode = raw_input("Please input soCode:")
soCode = soCode.strip()

#ofc_obd_head
sql = "select * from ofc_obd_head where so_code='" + soCode + "'"
obd = dao.executeOfcSelectSql(sql)
print("obd:" + json.dumps(obd))

sql = "delete from ofc_obd_head where id=" + obd['id']
dao.executeOfcSql(sql)

#ofc_bill
sql = "select * from ofc_bill where bill_id='" + obd['obd_code'] + "'"
ofcBill = dao.executeOfcSelectSql(sql)
print("ofc_bill:" + json.dumps(ofcBill))

sql = "delete from ofc_bill where id=" + ofcBill['id']
dao.executeOfcSql(sql)

#ofc_so_head
sql = "select * from ofc_so_head where so_code='" + soCode + "'"
ofcSoHead = dao.executeOfcSelectSql(sql)
print("ofc_so_head:" + json.dumps(ofcSoHead))

sql = "update ofc_so_head set so_status=20,total_sku_deliver_qty=0.00 where id=" + ofcSoHead['id']
dao.executeOfcSql(sql)

#ofc_task
#sql = "select * from ofc_task where ref_id='" + obd['order_code'] + "' and type=21"
#ofcTask = dao.executeOfcSelectSql(sql)
#print("ofc_task:" + json.dumps(ofcTask))

#sql = "delete from ofc_task where ref_id='" + obd['order_code'] + "' and type=21"
#dao.executeOfcSql(sql)

#ofc_order_head
sql = "select * from ofc_order_head where order_code='" + obd['order_code'] + "'"
ofcOrderHead = dao.executeOfcSelectSql(sql)
print("ofc_order_head:" + json.dumps(ofcOrderHead))

sql = "update ofc_order_head set fulfill_status=20,total_sku_deliver_qty=0.00 where id=" + ofcOrderHead['id']
dao.executeOfcSql(sql)
