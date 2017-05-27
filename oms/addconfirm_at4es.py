#encoding=utf-8
import json
import sys
from decimal import Decimal

sys.path.append('..')

import requests
from base.config import configs
from base.dao import Dao
from base.base import Base
from base.es import Es

esConfig = configs['es']
es = Es()
dao = Dao()
base = Base()
headers = base.getHeaders()


starttime = raw_input("Please input startTime format eg 2017/01/01 00:00:00 :")
print type(starttime)
endtime = raw_input("Please input endtime :")

sql = "select * from order_sign_head where tms_id = 0 and is_valid = 1 and status = 2 and receipt_at <= UNIX_TIMESTAMP('%s') and receipt_at >= UNIX_TIMESTAMP('%s')" % (endtime,starttime)

result = dao.executeOmsSelectSql(sql)
i = 0
for receipt_order in result:
    print "*********************************************"

    receiptOrderId = receipt_order['receipt_order_id']
    print "receipt_order_id : " + str(receiptOrderId)

    data = {}
    data["confirm_at"] = receipt_order['confirm_at']

    doc = {}
    doc["doc"] = data
    jsonM = json.dumps(doc)
    print jsonM

    # 线上url
    url = esConfig['tms_ip'] + "receipt/" + str(receiptOrderId) + "/_update?pretty"
    print url

    # # 本地url
    # url = esConfig['ip'] + str(receiptOrderId) + "/_update?pretty"

    res = requests.post(url, data=jsonM, headers=headers)
    print res.text

    i += 1

print '共处理'+str(i)