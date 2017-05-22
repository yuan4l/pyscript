#encoding=utf-8
import sys
sys.path.append('..')

from base.base import Base
from base.es import Es
import requests
import json
import time

base = Base()
headers = base.getHeaders()

fromDc = "DC55"
toDc = "DC59"

fromIp = "http://192.168.60.151:9200/"
toIp = "http://192.168.60.151:9200/ofc/ofc_so_info/_bulk"

searchStr = fromIp + "ofc/ofc_so_info/_search?search_type=scan&scroll=30m&size=400"
res = requests.post(searchStr, headers=headers)
obj = json.loads(res.text)
scroll_id = obj['_scroll_id']
searchStr = fromIp + "_search/scroll?scroll=30m&scroll_id=" + scroll_id

total = 0
startTime = time.clock()
res=requests.post(searchStr, headers=headers)
while res:
	startExecuteTime = time.clock()

	items = json.loads(res.text)['hits']['hits']

	data = ''
	flag = 0
	for item in items:
		obj = item['_source']
		if obj['warehouse_code'] != fromDc:
			continue
		data += '{"update":{"_id":"%s"}}\n' % (item['_id'],)
		data += '{"doc":{"warehouse_code":"%s"}}\n' % (toDc,)
		flag += 1

	print(data)
	#res = requests.post(toIp, data=data, headers=headers)
	#base.analysisBulkLog(res.text, "update")

	res=requests.post(searchStr, headers=headers)

	total += flag
	endExecuteTime = time.clock()
	print("Num:%d  Execute time:%.03f sec" % (flag, endExecuteTime - startExecuteTime))
endTime = time.clock()
print("Total:%d  Execute time:%.03f sec" % (total, endTime - startTime))
