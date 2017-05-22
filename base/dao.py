from config import configs
from db import MysqlHelper

class Dao(object):

	def __init__(self):
		self.__oms = MysqlHelper(configs['oms'])
		self.__ofc = MysqlHelper(configs['ofc'])
		self.__market = MysqlHelper(configs['market'])

	def executeOmsSql(self, sql):
		return self.__oms.executeSql(sql)

	def executeOmsSelectSql(self, sql):
		return self.__oms.findList(sql)

	def executeOfcSql(self, sql):
		return self.__ofc.executeSql(sql)

	def executeOfcSelectSql(self, sql):
		return self.__ofc.findList(sql)

	def getOrderHeadIdRange(self):
		sql = "select min(id) as min,max(id) as max from order_head"
		result = self.__oms.findOne(sql)
		return result

	def getOrderHead(self, orderCode):
		sql = "select * from order_head where order_code=%d" % (orderCode,)
		result = self.__oms.findOne(sql)
		return result

	def getOrderHeadList(self, start, end):
		sql = "select * from order_head where id>=%d and id<=%d" % (start, end)
		result = self.__oms.findList(sql)
		return result

	def getOrderHeadExt(self, id):
		sql = "select * from order_head_ext where id=%d" % (id,)
		result = self.__oms.findOne(sql)
		return result

	def getAftersales(self, orderCode):
		sql = "select * from order_aftersales where order_code=%d" % (orderCode,)
		result = self.__oms.findOne(sql)
		return result
	
	def getMarketName(self, addressCode):
		sql = "select market_name as market_name from user_address where address_id=%d" % (addressCode,)
		result = self.__market.findOne(sql)
		if not result:
			result = {}
		return result

	def getUserName(self, userCode):
		sql = "select username as username from user_info where uid=%d" % (userCode,)
		result = self.__market.findOne(sql)
		if not result:
			result = {}
		return result

	def getAdminName(self, addressCode):
		uid = self.getUid(addressCode)
		if not uid or not uid['uid']:
			return {}
		sql = "select admin_name as admin_name from admin_user where uid=%d" % (int(uid['uid']),)
		result = self.__market.findOne(sql)
		if not result:
			return {}
		return result

	def getUid(self, addressCode):
		sql = "select uid as uid from salesman_market where address_id=%d" % (addressCode,)
		result = self.__market.findOne(sql)
		return result

	def getShippingOrder(self, shipping_order_id):
		sql = "select * from order_shipping_head where shipping_order_id=%d" % (shipping_order_id,)
		result = self.__oms.findOne(sql)
		if not result:
			return {}
		return result

	def getReceiptOrder(self, receipt_order_id):
		sql = "select * from order_sign_head where receipt_order_id=%d" % (receipt_order_id,)
		result = self.__oms.findOne(sql)
		if not result:
			return {}
		return result

	def getReturnOrder(self, return_order_id):
		sql = "select * from order_ro_head where return_order_id=%d" % (return_order_id,)
		result = self.__oms.findOne(sql)
		if not result:
			return {}
		return result

#dao = Dao()	
#result = dao.getMarketName(123)
#print(result)
#result = dao.getOrderHeadList(1, 5)
#print(result)
#result = dao.getOrderHeadCount()
#print(result)
