import sys
sys.path.append('..')
from base.dao import Dao

dao = Dao()

receiptIdstr = raw_input("this is batch,by ',' separate receipt_order_id:")
receiptIdstr = receiptIdstr.strip()
receiptIds = receiptIdstr.split(",")
for receiptId in receiptIds:

    sql = "update  order_sign_head set status = 3, pay_status = 2, pay_type = 3 WHERE receipt_order_id = '%s'" %(receiptId)

    print dao.executeOmsSql(sql)