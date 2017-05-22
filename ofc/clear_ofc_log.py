#encoding=utf-8
import sys
sys.path.append('..')

import requests
import json
import time
import datetime
from base.base import Base

base = Base()
headers = base.getHeaders()

isPro = True

if isPro:
	host = 'http://192.168.60.151:9200'
else:
	host = 'http://192.168.60.59:9200'
ofc_log_url = host + '/ofc/ofc_log/_search?pretty'
ofc_log_delete_url = host + '/ofc/ofc_log/_bulk'

interval = 7
ago_time = (datetime.datetime.now() - datetime.timedelta(days = interval))
time_stamp = int(time.mktime(ago_time.timetuple()))

query = '{"query": {"range": {"create_time": {"lte": ' + str(time_stamp) + '}}},"_source":"id","from":0,"size":'

query_string = query + '1}'
res = requests.post(ofc_log_url, headers=headers, data=query_string)
ofc_log_obj = json.loads(res.text)
size = ofc_log_obj['hits']['total']

query_string = query + str(size) + '}'
res = requests.post(ofc_log_url, headers=headers, data=query_string)
ofc_log_obj = json.loads(res.text)
ofc_log_hits = ofc_log_obj['hits']['hits']

flag = 0
size = len(ofc_log_hits)
data = ''
for item in ofc_log_hits:
	ofc_log_id = item['_id']
	data += '{"delete":{"_id":"%s"}}\n' % (ofc_log_id,)
	if flag == size - 1 or flag % 1000 == 0:
		res = requests.post(ofc_log_delete_url, data=data, headers=headers)
		data = ''
	flag += 1
