#encoding=utf-8
import sys
sys.path.append('..')

from base.dao import Dao
import redis
import requests
import json

dao = Dao()

key = 'OFC_REDIS_HASH'
field = 'OFC_WUMART_OFC_SWITCH'

r = redis.Redis(host="192.168.60.152", port=6700, db=0)

flag = False

isOpen = raw_input("off/on:")
isOpen = isOpen.strip()
if isOpen == 'on' or isOpen == 'on'.upper():
	flag = True

isExist = r.hexists(key, field)
if isExist:
	value = r.hget(key, field)
	if flag:
		r.hset(key, field, '1')
	else:
		r.hset(key, field, '0')

sql = ''
if flag:
	sql = 'update ofc_supplier set fulfill_channel=2 where id in (1,2,3,4)'
else:
	sql = 'update ofc_supplier set fulfill_channel=3 where id in (1,2,3,4)'
dao.executeOfcSql(sql)

#isJinZhan = raw_input("Is JinZhan?(y/n):")
#isJinZhan = isJinZhan.strip()
isJinZhan = 'n'

if isJinZhan == 'y' or isJinZhan == 'y'.upper():
	sql = 'insert into ofc_supplier(id,code,supplier_dc,supplier_org,warehouse_code,warehouse_name, \
			region_code,fulfill_wms,fulfill_channel,create_time,update_time,valid) values(11,"DC42","DC42",1,"DC42", \
			"WINDC常温库",1000,1,2,1473424551,1473424551,1)'
	dao.executeOfcSql(sql)

	sql = 'insert into ofc_supplier(id,code,supplier_dc,supplier_org,warehouse_code,warehouse_name, \
			region_code,fulfill_wms,fulfill_channel,create_time,update_time,valid) values(12,"DC43","DC43",2,"DC42", \
			"WINDC常温库",1000,1,2,1473424551,1473424551,1)'
	dao.executeOfcSql(sql)
