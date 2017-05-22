#encoding=utf-8
import sys
sys.path.append('..')

from base.dao import Dao

dao = Dao()

sql = 'select * from ofc_so_head where region_code=1000 and total_sku_supply_qty>total_sku_deliver_qty and create_time>unix_timestamp("2017-04-17") and so_status=30';
ofcSoHeads = dao.executeOfcSelectSql(sql)
print len(ofcSoHeads)

lacks = []
for ofcSoHead in ofcSoHeads:
	soBillCode = ofcSoHead['so_bill_code']

	sql = 'select * from ofc_so_detail where so_bill_code="' + soBillCode + '"'
	ofcSoDetails = dao.executeOfcSelectSql(sql)

	sql = 'select * from ofc_obd_detail where so_bill_code="' + soBillCode + '"'
	ofcObdDetails = dao.executeOfcSelectSql(sql)

	for ofcSoDetail in ofcSoDetails:
		flag = False
		for ofcObdDetail in ofcObdDetails:
			if ofcSoDetail['sku_supply_code'] == ofcObdDetail['sku_supply_code']:
				flag = True

				if ofcSoDetail['sku_supply_qty'] > ofcObdDetail['sku_deliver_qty']:
					lack = {}
					lack['so_code'] = ofcSoHead['so_code']
					lack['so_bill_code'] = ofcSoHead['so_bill_code']
					lack['sku_supply_code'] = ofcSoDetail['sku_supply_code']
					lack['sku_supply_qty'] = ofcSoDetail['sku_supply_qty']
					lack['sku_deliver_qty'] = ofcObdDetail['sku_deliver_qty']
					lack['goods_name'] = ofcSoDetail['goods_name']

					lacks.append(lack)
					break

		if not flag:
			lack = {}
			lack['so_code'] = ofcSoHead['so_code']
			lack['so_bill_code'] = ofcSoHead['so_bill_code']
			lack['sku_supply_code'] = ofcSoDetail['sku_supply_code']
			lack['sku_supply_qty'] = ofcSoDetail['sku_supply_qty']
			lack['sku_deliver_qty'] = 0.00
			lack['goods_name'] = ofcSoDetail['goods_name']

			lacks.append(lack)

for lack in lacks:
	print lack['so_code'] + ' ' + lack['so_bill_code'] + ' ' + lack['sku_supply_code'] + ' ' + str(lack['sku_supply_qty']) + ' ' + str(lack['sku_deliver_qty']) + ' ' + lack['goods_name']