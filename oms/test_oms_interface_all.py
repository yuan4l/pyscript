#encoding=utf-8
import sys
sys.path.append('..')
import requests
import json
from base.base import Base

base = Base()

#prefix = 'http://192.168.60.152:9300/api/oms/java'
prefix = 'http://192.168.60.151:9302/api/oms/java'
headers = {'api-version':'1.0', 'random':'000', 'platform':'test', 'Content-Type':'application/json'}

#getOrderMoney
url = prefix + '/v1/order/find/getOrderMoney'
data = '{"orderId":"6222656933975834624","details":[{"code":"000000000000277450","realQty":"6"},{"code":"000000000000544097","realQty":"6"},{"code":"000000000000607208","realQty":"10"},{"code":"000000000000607199","realQty":"10"},{"code":"000000000000277417","realQty":"6"},{"code":"000000000000607197","realQty":"10"},{"code":"000000000000607204","realQty":"10"},{"code":"000000000000277418","realQty":"6"},{"code":"000000000000607203","realQty":"6"},{"code":"000000000000277419","realQty":"6"},{"code":"000000000000607195","realQty":"10"},{"code":"000000000000607206","realQty":"5"},{"code":"000000000000607196","realQty":"10"},{"code":"000000000000607200","realQty":"10"},{"code":"000000000000607202","realQty":"6"},{"code":"000000000000277420","realQty":"6"},{"code":"000000000000277421","realQty":"6"}]}'
res = requests.post(url, data=data, headers=headers)
print('url:' + url + '\n' + 'resp:' + res.text)

#返仓单列表
print('1.返仓单列表')
url = prefix + '/v1/order/find/query/getReturnOrderList?returnIds=[3500471399329333756,3247003225026474763]'
res = requests.get(url, headers=headers)
print('url:' + url + '\n' + 'resp:' + res.text)

#返仓单详情
print('2.返仓单详情')
url = prefix + '/v1/order/find/query/getReturnOrder?return_order_id=6228542701743116288'
res = requests.get(url, headers=headers)
print('url:' + url + '\n' + 'resp:' + res.text)

#发货单列表
print('3.发货单列表')
url = prefix + '/v1/order/find/query/getDeliveryOrderList?shippingIds=[7924272772221160056]'
res = requests.get(url, headers=headers)
print('url:' + url + '\n' + 'resp:' + res.text)

#发货单详情
print('4.发货单详情')
url = prefix + '/v1/order/find/query/getDeliveryOrder?shipping_order_id=3156086736332063317'
res = requests.get(url, headers=headers)
print('url:' + url + '\n' + 'resp:' + res.text)

#签收单列表
print('5.签收单列表')
url = prefix + '/v1/order/find/query/getReceiptOrderList?receiptIds=[7040019132882814582]'
res = requests.get(url, headers=headers)
print('url:' + url + '\n' + 'resp:' + res.text)

#签收单详情
print('6.签收单详情')
url = prefix + '/v1/order/find/query/getReceiptOrder?receipt_order_id=5500210365441803043'
res = requests.get(url, headers=headers)
print('url:' + url + '\n' + 'resp:' + res.text)

#通过订单ID获取签收单信息
print('7.通过订单ID获取签收单信息')
url = prefix + '/v1/order/find/query/getReceiptInfoByOrderIds?orderIds=[6207147983176212480]'
res = requests.get(url, headers=headers)
print('url:' + url + '\n' + 'resp:' + res.text)

#通过订单ID获取发货单信息
print('8.通过订单ID获取发货单信息')
url = prefix + '/v1/order/find/query/getDeliveryInfoByOrderIds?orderIds=[6215471954430799872]'
res = requests.get(url, headers=headers)
print('url:' + url + '\n' + 'resp:' + res.text)

#通过发货单ID获取签收单信息
print('9.通过发货单ID获取签收单信息')
url = prefix + '/v1/order/find/query/getReceiptByDeliveryId?shipping_order_id=2576811162355204043'
res = requests.get(url, headers=headers)
print('url:' + url + '\n' + 'resp:' + res.text)

#通过发货单ID获取返仓单信息
print('10.通过发货单ID获取返仓单信息')
url = prefix + '/v1/order/find/query/getReturnByDeliveryId?shipping_order_id=6206647274739613696'
res = requests.get(url, headers=headers)
print('url:' + url + '\n' + 'resp:' + res.text)

#通过发货单ID获取发货单明细
print('11.通过发货单ID获取发货单明细')
url = prefix + '/v1/order/find/query/getDeliveryDetails?shippingIds=[7924272772221160056]'
res = requests.get(url, headers=headers)
print('url:' + url + '\n' + 'resp:' + res.text)

#通过发货单ID获取签收单信息
print('12.通过发货单ID获取签收单信息')
url = prefix + '/v1/order/find/query/getReceiptInfoByDeliveryIds?shippingIds=[2576811162355204043]'
res = requests.get(url, headers=headers)
print('url:' + url + '\n' + 'resp:' + res.text)

#获取订单相关单据
print('13.获取订单相关单据')
url = prefix + '/v1/order/find/query/getRelateOrders?order_id=6206647274739613696'
res = requests.get(url, headers=headers)
print('url:' + url + '\n' + 'resp:' + res.text)

#通过订单ID获取返仓单头信息
print('14.通过订单ID获取返仓单头信息')
url = prefix + '/v1/order/find/query/getReturnHeadsByOrderIds?orderIds=[6206647274739613696]'
res = requests.get(url, headers=headers)
print('url:' + url + '\n' + 'resp:' + res.text)

#通过订单ID获取返仓单明细信息
print('15.通过订单ID获取返仓单明细信息')
url = prefix + '/v1/order/find/query/getReturnDetailsByOrderIds?orderIds=[6206647274739613696]'
res = requests.get(url, headers=headers)
print('url:' + url + '\n' + 'resp:' + res.text)

#通过发货单ID获取返仓单头信息
print('16.通过发货单ID获取返仓单头信息')
url = prefix + '/v1/order/find/query/getReturnHeadsByDeliveryIds?shippingIds=[4340111156035159027]'
res = requests.get(url, headers=headers)
print('url:' + url + '\n' + 'resp:' + res.text)

#通过发货单ID获取返仓单明细信息
print('17.通过发货单ID获取返仓单明细信息')
url = prefix + '/v1/order/find/query/getReturnDetailsByDeliveryIds?shippingIds=[4340111156035159027]'
res = requests.get(url, headers=headers)
print('url:' + url + '\n' + 'resp:' + res.text)

#获取发货单配置
print('18.获取发货单配置')
url = prefix + '/bill/shipping/list'
#res = requests.get(url, headers=headers)
#print('url:' + url + '\n' + 'resp:' + res.text)

#获取签收单配置
print('19.获取签收单配置')
url = prefix + '/bill/receipt/list'
res = requests.get(url, headers=headers)
print('url:' + url + '\n' + 'resp:' + res.text)

#获取返仓单配置
print('20.获取返仓单配置')
url = prefix + '/bill/return/list'
res = requests.get(url, headers=headers)
print('url:' + url + '\n' + 'resp:' + res.text)

#app支付
print('21.app支付')
url = prefix + '/bill/shipping/dofullreceipt'
#res = requests.post(url, headers=headers)
#print('url:' + url + '\n' + 'resp:' + res.text)

