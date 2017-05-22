#encoding=utf-8
import sys
sys.path.append('..')

from base.config import configs
from base.base import Base
from base.es import Es
from base.dao import Dao
import requests
import json

es = Es()
dao = Dao()
base = Base()
headers = base.getHeaders()
esConfig = configs['es']

isBatch = raw_input("Is batch?(y/n):")
isBatch = isBatch.strip()
if isBatch == 'y' or isBatch == 'y'.upper():
	while True:
		print("Please choose order type:\n1.order_head\n2.shipping_order\n3.receipt_order\n4.return_order")
		orderType = raw_input("orderType:")
		orderType = orderType.strip()
		if orderType != '1' and orderType != '2' and orderType != '3' and orderType != '4':
			print("Input order type is not correct, please input again!")
			continue

		print("Please input orderCode by ',' separate")
		orderCodesStr = raw_input("orderCodes:")
		orderCodesStr = orderCodesStr.strip()
		if orderCodesStr is None or orderCodesStr == "" or len(orderCodesStr.split(",")) <= 0:
			print("Input parameter is not correct,please input again!")
			continue
		
		orderCodes = orderCodesStr.split(",")
		data = ''
		for orderCode in orderCodes:
			orderCode = orderCode.strip()
			if orderCode is None or orderCode == "" or not orderCode.isdigit():
				print("[Error][%s] Input parameter is not correct" % (orderCode,))
				continue

			value = None
			if orderType == '1':
				value = dao.getOrderHead(long(orderCode))
			elif orderType == '2':
				value = dao.getShippingOrder(long(orderCode))
			elif orderType == '3':
				value = dao.getReceiptOrder(long(orderCode))
			else:
				value = dao.getReturnOrder(long(orderCode))
			
			if not value:
				print("[Error][%s] Not found order by orderCode" % (orderCode,))
				continue

			esData = None
			if orderType == '1':
				esData = es.getEsData(value)
				data += '{"index":{"_id":"%s"}}\n' % (value['order_code'],)
			elif orderType == '2':
				esData = es.getShippingEsData(value)
				data += '{"index":{"_id":"%s"}}\n' % (value['shipping_order_id'],)
			elif orderType == '3':
				esData = es.getReceiptEsData(value)
				data += '{"index":{"_id":"%s"}}\n' % (value['receipt_order_id'],)
			else:
				esData = es.getReturnEsData(value)
				data += '{"index":{"_id":"%s"}}\n' % (value['return_order_id'],)
			data += json.dumps(esData) + "\n"

		url = ''
		if orderType == '1':
			url = esConfig['ip'] + "_bulk"
		elif orderType == '2':
			url = esConfig['tms_ip'] + "shipping/_bulk"
		elif orderType == '3':
			url = esConfig['tms_ip'] + "receipt/_bulk"
		else:
			url = esConfig['tms_ip'] + "return/_bulk"

		#logger.info("request data:%s" % (data,))
		print(url)
		print(data)
		res = requests.post(url, data=data, headers=headers)
		print(res.text)
		base.analysisBulkLog(res.text, "index")

		break
else:
	while True:
		isContinue = raw_input("Please input is continue(y/n):")
		isContinue = isContinue.strip()
		if isContinue != 'y' and isContinue != 'y'.upper():
			break

		print("Please choose order type:\n1.order_head\n2.shipping_order\n3.receipt_order\n4.return_order")
		orderType = raw_input("orderType:")
		orderType = orderType.strip()
		if orderType != '1' and orderType != '2' and orderType != '3' and orderType != '4':
			print("Input order type is not correct, please input again!")
			continue

		orderCode = raw_input("Please input orderCode:")
		orderCode = orderCode.strip()
		if orderCode is None or orderCode == "" or not orderCode.isdigit():
			print("Input parameter is not correct,please input again!")
			continue

		value = None
		if orderType == '1':
			value = dao.getOrderHead(long(orderCode))
		elif orderType == '2':
			value = dao.getShippingOrder(long(orderCode))
		elif orderType == '3':
			value = dao.getReceiptOrder(long(orderCode))
		else:
			value = dao.getReturnOrder(long(orderCode))
		if not value:
			print("Input error,not found order by orderCode,please check orderCode!")
			continue

		url = ''
		data = ''
		if orderType == '1':
			url = esConfig['ip'] + orderCode
			data = json.dumps(es.getEsData(value))
		elif orderType == '2':
			url = esConfig['tms_ip'] + "shipping/" + orderCode
			data = json.dumps(es.getShippingEsData(value))
		elif orderType == '3':
			url = esConfig['tms_ip'] + "receipt/" + orderCode
			data = json.dumps(es.getReceiptEsData(value))
		else:
			url = esConfig['tms_ip'] + "return/" + orderCode
			data = json.dumps(es.getReturnEsData(value))
		
		print(url)
		print(data)
		res = requests.post(url, data=data, headers=headers)
		print(res.text)
