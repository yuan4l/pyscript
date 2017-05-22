#encoding=utf-8
import sys
sys.path.append('..')

from base.dao import Dao

dao = Dao()

updateOfcSupplier = False
dcMap = {11:1,12:2}
ofcSupplierMap = {}

if updateOfcSupplier:
	for dc in dcMap:
		sql = 'select * from ofc_supplier where id=' + str(dcMap[dc])
		ofcSuppliers = dao.executeOfcSelectSql(sql)
		ofcSupplierMap[dc] = ofcSuppliers[0]

orderCodes = set()

while True:
	isContinue = raw_input("Please input is continue(y/n):")
	isContinue = isContinue.strip()
	if isContinue != 'y' and isContinue != 'y'.upper():
		break

	soBillCodes = []
	isBatch = raw_input("Is batch?(y/n):")
	isBatch = isBatch.strip()
	if isBatch == 'y' or isBatch == 'y'.upper():
		print("Please input soBillCode by ',' separate")
		soBillCodesStr = raw_input("soBillCodes:")
		soBillCodesStr = soBillCodesStr.strip()
		if soBillCodesStr is None or soBillCodesStr == "" or len(soBillCodesStr.split(",")) <= 0:
			print("Input parameter is not correct,please input again!")
			continue
		
		soBillCodes = soBillCodesStr.split(",")
	else:
		soBillCode = raw_input("so bill code:")
		soBillCode = soBillCode.strip()

		soBillCodes.append(soBillCode)

	for soBillCode in soBillCodes:
		sql = 'select * from ofc_so_head where so_bill_code="' + soBillCode + '"'
		ofcSoHeadList = dao.executeOfcSelectSql(sql)

		for ofcSoHead in ofcSoHeadList:
			soCode = ofcSoHead['so_code']
			billType = 'ORDER'
			orderCode = ofcSoHead['order_code']

			sql = 'delete from ofc_bill where order_id=' + str(orderCode) + ' and bill_id="' + soCode + '" and bill_type="' + billType + '"'
			print sql
			#dao.executeOfcSql(sql)

			sql = 'update ofc_so_head set so_status=10 where so_bill_code="' + soBillCode + '"'
			print sql
			dao.executeOfcSql(sql)

			if updateOfcSupplier:
				supplierId = ofcSoHead['supplier_id']
				ofcSupplier = ofcSupplierMap[supplierId]
				sql = 'update ofc_so_head set warehouse_code="' + ofcSupplier['warehouse_code'] + '",warehouse_name="' + ofcSupplier['warehouse_name'] + '"\
						,supplier_id=' + str(ofcSupplier['id']) + ',supplier_dc="' + ofcSupplier['supplier_dc'] + '",supplier_org=' + str(ofcSupplier['supplier_org']) + '\
						,fulfill_wms=' + str(ofcSupplier['fulfill_wms']) + ',fulfill_channel=' + str(ofcSupplier['fulfill_channel']) + ' where so_bill_code="' + soBillCode + '"'
				print sql
				#dao.executeOfcSql(sql)

			orderCodes.add(orderCode)

for orderCode in orderCodes:
	sql = 'update ofc_task set status=3,exec_count=9 where ref_id="' + str(orderCode) + '" and type=11'
	print sql
	dao.executeOfcSql(sql)

	sql = 'update ofc_order_head set fulfill_status=10 where order_code=' + str(orderCode)
	print sql
	#dao.executeOfcSql(sql)

	sql = 'update order_head set order_status=21 where order_status=22 and order_code=' + str(orderCode)
	print sql
	#dao.executeOmsSql(sql)



