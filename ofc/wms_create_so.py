#encoding=utf-8

import requests
import json
import time

order = {}
order['warehouseCode']='A001'
order['orderOtherId']='SO6195201487052779520'
order['orderOtherRefId']=''
order['orderUserCode']=''
order['orderUser']=''
order['deliveryName']='上地超市'
order['deliveryCode']='18612520632'
order['ownerUid']=1
order['orderType']=1
order['transTime']=1478685600
order['shipperProvince']='北京市'
order['shipperCity']='市辖区'
order['shipperDistrict']='海淀区'
order['deliveryAddrs']='上地三街信息大厦'

detail = {}
detail['detailOtherId']=10
detail['skuCode']='000000000000180887'
detail['barCode']=''
detail['packUnit']=1
detail['orderQty']=5.000
detail['packName']=''
detail['lotNum']=''
detail['price']='1.000'
detail['unitName']='件'
detail['unitQty']=5.000

details= [detail]

order['detailList']=details

url = ""
data = json.dumps(order)
print(data + "\n")

res=requests.post(url, data=data)
print(res.text)
