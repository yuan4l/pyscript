#encoding=utf-8
import json
import sys
from base.dao import Dao
sys.path.append('..')

dao = Dao()

receipt = raw_input("Please input receipt:")
receipt = int(receipt)

orderSignHead = dao.getReceiptOrder(receipt)
orderHead = dao.getOrderHead(orderSignHead['order_id'])
orderHeadExt = dao.getOrderHeadExt(orderHead['id'])

ext = orderSignHead['ext']

data = json.loads(ext)['head_info']
data['activity_info'] = orderHeadExt['activity_info']

dictext = {}
dictext['head_info'] = data

exts = json.dumps(dictext)
print exts
sql = "update  order_sign_head set ext = '%s' WHERE receipt_order_id = '%s'" % (exts,receipt)
print dao.executeOmsSql(sql)