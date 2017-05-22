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

			value = dao.getOrderHead(long(orderCode))
			if not value:
				print("[Error][%s] Not found order by orderCode" % (orderCode,))
				continue

			data += '{"index":{"_id":"%s"}}\n' % (value['order_code'],)
			data += json.dumps(es.getEsData(value)) + "\n"

		url = esConfig['ip'] + "_bulk"

		#logger.info("request data:%s" % (data,))
		print(data)
		res = requests.post(url, data=data, headers=headers)
		print(res.text)
		#base.analysisBulkLog(res.text, "index")

		break
else:
	while True:
		isContinue = raw_input("Please input is continue(y/n):")
		isContinue = isContinue.strip()
		if isContinue != 'y' and isContinue != 'y'.upper():
			break

		orderCode = raw_input("Please input orderCode:")
		orderCode = orderCode.strip()
		if orderCode is None or orderCode == "" or not orderCode.isdigit():
			print("Input parameter is not correct,please input again!")
			continue

		value = dao.getOrderHead(long(orderCode))
		if not value:
			print("Input error,not found order by orderCode,please check orderCode!")
			continue

		url = esConfig['ip'] + orderCode
		data = json.dumps(es.getEsData(value))

		print(data)
		res = requests.post(url, data=data, headers=headers)
		print(res.text)
