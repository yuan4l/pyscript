#encoding=utf-8
import sys
sys.path.append('..')

from base.dao import Dao
dao = Dao()


returnOrderIds = {}
returnOrderIds[6229122891925970944] = 6223301991620173825
returnOrderIds[6228542701743116288] = 6223301992584843265

createTime = {}
createTime[6229122891925970944] = 1485138628
createTime[6228542701743116288] = 1485000300

updateTime = {}
updateTime[6229122891925970944] = 1485138628
updateTime[6228542701743116288] = 1485000300

for returnOrderId in returnOrderIds:
	sql = "select * from order_shipping_detail where shipping_order_id=" + str(returnOrderIds[returnOrderId])
	details = dao.executeOmsSelectSql(sql);

	sql = "insert into order_ro_detail (return_order_id, sku_id, sku_name, sale_unit, qty, real_qty, status, ext, \
	 created_at, updated_at, zone_id, price, money, return_note, make_up_note, item_id,tms_id) values "

	totalMoney = 0.00

	for detail in details:
		insertSql = sql + "(" + str(returnOrderId) + "," + str(detail['sku_id']) + ",'" + str(detail['sku_name']) + "'," + str(detail['sale_unit']) + "," \
		+ str(detail['qty']) + "," + str(detail['real_qty']) + "," + str(detail['status']) + ",'" + detail['ext'].encode("unicode-escape") + "'," + str(createTime[returnOrderId]) \
		+ "," + str(updateTime[returnOrderId]) + "," + str(detail['zone_id']) + "," + str(detail['price']) + "," + str(detail['money']) + "," \
		+ str(0) + "," + "''" + "," + str(detail['item_id']) + "," + str(0L) + ")"

		totalMoney += float(detail['qty']) * float(detail['price'])

		#print(insertSql)
		dao.executeOmsSql(insertSql)
	
	print(totalMoney)
