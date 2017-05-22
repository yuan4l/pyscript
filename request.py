#encoding=utf-8
from base.base import Base
import requests

#url = 'http://api.wms.lsh123.com/API/V1/openApi/saveObd'
url = 'http://192.168.60.151:9501/ofc/api/customer/refresh/5105581738303293879'

#base = Base()
#headers = base.getHeaders()

headers = {'api-version':'1.0', 'random':1, 'platform':'test'}

while True:
	requestBody = raw_input("Please input:")
	requestBody = requestBody.strip()

	#res = requests.post(url, data=requestBody, headers=headers)
	res = requests.post(url, headers=headers)
	print res.text
