#encoding=utf-8

import requests
import json

prefix = 'http://service.wumart.com'
so_query_url = '/lians/orderStatus'
ro_query_url = '/lians/orderStatus'

base_headers = {'Content-type':'application/json;accountName=lsh123;password=lsh321;'}
headers = base_headers

while True:
	isContinue = raw_input("Please input is continue(y/n):")
	isContinue = isContinue.strip()
	if isContinue != 'y' and isContinue != 'y'.upper():
		break

	url = ''

	is_query = raw_input("Is query so?(y/n):")
	is_query = is_query.strip()
	if is_query == 'y' or is_query == 'y'.upper():
		print("Query So!")
		url = prefix + so_query_url
	else:
		print("Query Ro!")
		url = prefix + ro_query_url

	businessId = raw_input("Please input businessid:")
	batchNumber = raw_input("Please input batchNumber:")
	so_query_obj = {}
	so_query_obj['businessId']=businessId
	so_query_obj['batchNumber']=batchNumber
	query_data = json.dumps(so_query_obj)

	i = 0
	while i<2:
		print("query_url:" + url)
		print("query_data:" + query_data)
		res = requests.post(url, data=query_data, headers=headers)
		print("return content:" + json.dumps(res.text,ensure_ascii=False))
		res_obj = json.loads(res.text)
		if not res_obj.has_key('code'):
			break
		code = res_obj['code']
		if code == 200:
			break;
		elif code == 1:
			token = res_obj['gatewayToken']
			if not token:
				print("token is null," + token)
				break
			headers['Content-type'] = base_headers['Content-type'] + "gatewayToken=" + token + ";"

