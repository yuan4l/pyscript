#encoding=utf-8
import sys
sys.path.append('..')

import requests
import json
from base.base import Base

base = Base()
headers = base.getHeaders()

term = {}
term['storage_type_id'] = '2'
query = {}
query['term'] = term
query_string = {}
query_string['query'] = query

shipping_url = 'http://192.168.60.59:9200/tms_search/shipping/_search?pretty'
shipping_delete_url = 'http://192.168.60.59:9200/tms_search/shipping/'
receipt_url = 'http://192.168.60.59:9200/tms_search/receipt/_search?pretty'
receipt_delete_url = 'http://192.168.60.59:9200/tms_search/receipt/?pretty'
return_url = 'http://192.168.60.59:9200/tms_search/return/_search?pretty'
return_delete_url = 'http://192.168.60.59:9200/tms_search/return/'

query_string['_source'] = 'shipping_order_id'
res = requests.post(shipping_url, headers=headers, data=json.dumps(query_string))
shipping_obj = json.loads(res.text)
shipping_hits = shipping_obj['hits']['hits']
for item in shipping_hits:
	shipping_order_id = item['_source']['shipping_order_id']
	url = shipping_delete_url + shipping_order_id
	print(url)
	#res = requests.delete(url, headers=headers)
	#print(res.text)

query_string['_source'] = 'receipt_order_id'
res = requests.post(receipt_url, headers=headers, data=json.dumps(query_string))
receipt_obj = json.loads(res.text)
receipt_hits = receipt_obj['hits']['hits']
for item in receipt_hits:
	receipt_order_id = item['_source']['receipt_order_id']
	url = receipt_delete_url + receipt_order_id
	print(url)
	#res = requests.delete(url, headers=headers)
	#print(res.text)

query_string['_source'] = 'return_order_id'
res = requests.post(return_url, headers=headers, data=json.dumps(query_string))
return_obj = json.loads(res.text)
return_hits = return_obj['hits']['hits']
for item in return_hits:
	return_order_id = item['_source']['return_order_id']
	url = return_delete_url + return_order_id
	print(url)
	#res = requests.delete(url, headers=headers)
	#print(res.text)
