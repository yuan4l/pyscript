#encoding=utf-8
import sys
sys.path.append('..')
from base.base import Base
from base.config import configs
import redis
import requests
import json
from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr

base = Base()
emailConfig = configs['email']

r = redis.Redis(host="192.168.60.152", port=6700, db=0)

newMeipiCustomerByRegions = {}
prefix = "OFC_MEIPI_CUSTOMER_CODES_"
prefixLen = len(prefix)

url = "http://192.168.60.151:9501/ofc/api/customer/meipi/addbatch"
headers = {'api-version':'1.0','random':'123','platform':'create_meipi_customer_python','Content-type':'application/json; charset=utf-8', 'Accept':'application/json'}
params = {'num':0, "region":0}
regionRelationship = {1000:'北京',1001:'天津',1002:'杭州'}

ofcMeipiCustomerByRegions = r.keys(prefix + "*")
for ofcMeipiCustomers in ofcMeipiCustomerByRegions:
	suffix = str(ofcMeipiCustomers)[prefixLen:len(ofcMeipiCustomers)]
	region = int(str(suffix))

	data = []

	number = r.llen(ofcMeipiCustomers)
	if number < 200:
		params['region'] = region
		params['num'] = 1

		paramUrl = url + '?region=' + str(params['region']) + '&num=' + str(params['num'])
		#res = requests.post(url=paramUrl, headers=headers)
		#print res.text
		#resObj = json.loads(res.text)
		#if resObj.has_key('data'):
		#	data = resObj['data']
		#else:
		#	data = ["返回数据错误"]

		data = ["小于两百，需要生成"]

		params['region'] = 0
		params['num'] = 0

	newMeipiCustomerByRegions[region] = data
	
content = ''
for region in newMeipiCustomerByRegions:
	content += str(region) + "(" + regionRelationship[region] + "):\n"
	for code in newMeipiCustomerByRegions[region]:
		content += str(code) + ","
	if len(newMeipiCustomerByRegions[region]) > 0 :
		content = content[0:len(content)-1]
	content += "\n"

msg = MIMEText(content, 'plain', 'utf-8')
msg['Subject'] = Header('物美美批用户生成信息', 'utf-8').encode()

smtpServer = emailConfig['smtp']
fromAddr = emailConfig['auth']['username']
password = emailConfig['auth']['password']
toAddr = emailConfig['to']
base.sendEmail(smtpServer, fromAddr, password, toAddr, msg)
