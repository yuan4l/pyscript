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
es = Es()

fromIp = "http://192.168.60.59:9200/"
toIp = "http://192.168.60.59:9200/oms_v1/order/_bulk"

searchStr = fromIp + "oms_v2/order/_search?search_type=scan&scroll=30m&size=400"
res = requests.post(searchStr, headers=headers)
obj = json.loads(res.text)
scroll_id = obj['_scroll_id']
searchStr = fromIp + "_search/scroll?scroll=30m&scroll_id=" + scroll_id

total = 0
flag = 0
startTime = time.clock()
res=requests.post(searchStr, headers=headers)
while res:
	#print(res.text)

	startExecuteTime = time.clock()
	print("Start:%d" % (flag,))

	items = json.loads(res.text)['hits']['hits']
	#print(len(items))

	data = ''
	for item in items:
		obj = es.transform(item["_source"])
		data += '{"index":{"_id":"%s"}}\n' % (item['_id'],)
		data += json.dumps(obj) + "\n"

	res = requests.post(toIp, data=data, headers=headers)
	base.analysisBulkLog(res.text, "index")

	res=requests.post(searchStr, headers=headers)

	flag += 2000
	result = len(items)
	total += result
	endExecuteTime = time.clock()
	print("Num:%d  Execute time:%.03f sec" % (result, endExecuteTime - startExecuteTime))
endTime = time.clock()
print("Total:%d  Execute time:%.03f sec" % (total, endTime - startTime))