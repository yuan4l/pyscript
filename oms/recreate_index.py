#encoding=utf-8
import sys
sys.path.append('..')

from base.base import Base
import requests
import json

base = Base()

def method(start, end, headers, esConfig, es, dao, logger):
	print("start:%d  end:%d" % (start,end))

	values = dao.getOrderHeadList(start, end)

	url = esConfig['ip'] + "_bulk"
	data = ''
	for value in values:
		data += '{"index":{"_id":"%s"}}\n' % (value['order_code'],)
		data += json.dumps(es.getEsData(value)) + "\n"

	#logger.info("request data:%s" % (data,))
	#print(data)
	res = requests.post(url, data=data, headers=headers)
	#print(res.text)
	base.analysisBulkLog(res.text, "index")

	return len(values)

base.execute(method)
