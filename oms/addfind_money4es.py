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

sql = "select * from order_sign_head where tms_id = 0 and pay_type = 3 and created_at <= UNIX_TIMESTAMP('%s') and created_at >= UNIX_TIMESTAMP('%s')" % (endtime,starttime)

result = dao.executeOmsSelectSql(sql)
i = 0
for receipt_order in result:
    print "*********************************************"

    receiptOrderId =  receipt_order['receipt_order_id']
    print "receipt_order_id : "+str(receiptOrderId)

    # money = str(receipt_order['money'])
    # # 取小数点后两位
    # two_decimal_place = Decimal(money[-2:])

    # if two_decimal_place != 0:
    #     inte = Decimal(money[:-3])
    #     dec = two_decimal_place/100
    #     print "^^^^^^^^^^未抹零，执行update^^^^^^^^^^^"
    #     upsql = "update  order_sign_head set money = '%f',floor_money = '%f' WHERE receipt_order_id = '%s'" % (inte,dec,receiptOrderId)
    #     print upsql
    #     dao.executeOmsSql(upsql)
    #     receipt_order['money'] = inte
    # 造数据
    # data = json.dumps(es.getReceiptEsData(receipt_order))
    # print data


    data = {}
    data["final_money"] = float(receipt_order['money'])

    doc ={}
    doc ["doc"] = data
    jsonM = json.dumps(doc)
    print jsonM
    # 线上用url
    # url = esConfig['ip'] + "receipt/" + str(receiptOdocrderId)

    # 本地url
    url = esConfig['ip'] + str(receiptOrderId)  + "/_update?pretty"

    res = requests.post(url, data=jsonM, headers=headers)
    print res.text

    i += 1
    print "*********************************************"

print '共处理'+str(i)