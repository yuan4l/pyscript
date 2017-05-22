#encoding=utf-8
import sys
sys.path.append('..')

from base.dao import Dao

dao = Dao()

while True:
	soBillCode = raw_input("so bill code:")
	soBillCode = soBillCode.strip()

	sql = 'select * from ofc_so_head where so_bill_code="' + soBillCode + '"'
	ofcSoHeadList = dao.executeOfcSelectSql(sql)

	for ofcSoHead in ofcSoHeadList:
		soCode = ofcSoHead['so_code']
		billType = 'ORDER'
		orderCode = ofcSoHead['order_code']

		sql = 'delete from ofc_bill where order_id=' + str(orderCode) + ' and bill_id="' + soCode + '" and bill_type="' + billType + '"'
		print sql
		#dao.executeOfcSql(sql)

		sql = 'update ofc_so_head set so_status=15 where so_bill_code="' + soBillCode + '"'
		print sql
		#dao.executeOfcSql(sql)
