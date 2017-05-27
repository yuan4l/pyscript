#encoding:utf8
from config import configs
from dao import Dao
import json

null = None

class Es(object):

    def __init__(self):
        self.__dao = Dao()
        self.__level_default_value = '0'
        self.__create_status = configs['es']['create_status']
        self.__update_status = configs['es']['update_status']
        self.__select_status = configs['es']['select_status']

    def getEsData(self, order):
        es = {}
        es['order_id'] = order['order_code'] and str(order['order_code']) or null
        es['zone_id'] = order['region_code'] and str(order['region_code']) or null
        es['order_status'] = order['order_status'] and str(order['order_status']) or null
        es['storage_type_id'] = order['storage_type'] and str(order['storage_type']) or null
        es['ordered_at'] = order['order_time'] and str(order['order_time']) or null
        es['dc_status'] = order['lack_delivery_type'] and str(order['lack_delivery_type']) or null
        es['uid'] = order['user_code'] and str(order['user_code']) or null
        es['so_codes'] = order['so_codes'] and str(order['so_codes']) or null
        es['address_id'] = order['address_code'] and str(order['address_code']) or null
        es['money'] = order['expect_pay_amount'] and float(order['expect_pay_amount']) or null

        marketName = self.__dao.getMarketName(order['address_code'])
        es['market_name'] = marketName.has_key("market_name") and str(marketName['market_name']) or null
        userName = self.__dao.getUserName(order['user_code'])
        es['username'] = userName.has_key("username") and str(userName['username']) or null
        adminName = self.__dao.getAdminName(order['address_code'])
        es['admin_name'] = adminName.has_key("admin_name") and str(adminName['admin_name']) or null

        es['exception_status'] = null

        aftersales = self.__dao.getAftersales(order['order_code'])
        if not aftersales:
            es['aftersales_status'] = "0"
        else:
            es['aftersales_status'] = aftersales['aftersales_status'] and str(aftersales['aftersales_status']) or "0"

        orderHeadExt = self.__dao.getOrderHeadExt(order['id'])
        if not orderHeadExt:
            es['is_comment'] = null
        else:
            es['is_comment'] = orderHeadExt['is_comment'] and str(orderHeadExt['is_comment']) or null

        levels = {}
        if orderHeadExt['ext']:
            levels = self.__getLevel(orderHeadExt['ext'])
        es['level3'] = levels.has_key("3") and str(levels["3"]) or self.__level_default_value
        es['level4'] = levels.has_key("4") and str(levels["4"]) or self.__level_default_value
        es['level5'] = levels.has_key("5") and str(levels["5"]) or self.__level_default_value
        es['level6'] = levels.has_key("6") and str(levels["6"]) or self.__level_default_value
        es['level7'] = levels.has_key("7") and str(levels["7"]) or self.__level_default_value

        return es

    def getDocData(self, order):
        es = {}
        es['doc'] = self.__getDocDict(order)
        return es

    def getShippingEsData(self, order):
        es = {}
        es['address_id'] = order['address_id'] and long(order['address_id']) or null
        es['delay_type'] = order['delay_type'] and int(order['delay_type']) or null
        es['level3'] = self.__level_default_value
        es['level4'] = self.__level_default_value
        es['level5'] = self.__level_default_value
        es['level6'] = self.__level_default_value
        es['level7'] = self.__level_default_value
        marketName = self.__dao.getMarketName(order['address_id'])
        es['market_name'] = marketName.has_key("market_name") and str(marketName['market_name']) or null
        es['money'] = order['money'] and float(order['money']) or null
        es['order_id'] = order['order_id'] and str(order['order_id']) or null
        es['shipping_actived_at'] = order['actived_at'] and long(order['actived_at']) or null
        es['shipping_arrived_at'] = order['arrived_at'] and long(order['arrived_at']) or null
        es['shipping_created_at'] = order['created_at'] and long(order['created_at']) or null
        es['shipping_order_id'] = order['shipping_order_id'] and str(order['shipping_order_id']) or null
        es['shipping_receipt_status'] = order['receipt_status'] and int(order['receipt_status']) or null
        es['shipping_shipped_at'] = order['shipped_at'] and long(order['shipped_at']) or null
        es['shipping_status'] = order['status'] and int(order['status']) or null
        es['storage_type_id'] = order['storage_type_id'] and int(order['storage_type_id']) or null
        es['zone_id'] = order['zone_id'] and long(order['zone_id']) or null
        return es

    def getReceiptEsData(self, order):
        es = {}
        es['address_id'] = order['address_id'] and long(order['address_id']) or null
        es['is_valid'] = order['is_valid'] and int(order['is_valid']) or null
        es['level3'] = self.__level_default_value
        es['level4'] = self.__level_default_value
        es['level5'] = self.__level_default_value
        es['level6'] = self.__level_default_value
        es['level7'] = self.__level_default_value
        # marketName = self.__dao.getMarketName(order['address_id'])
        # es['market_name'] = marketName.has_key("market_name") and str(marketName['market_name']) or null
        es['money'] = order['money'] and float(order['money']) or null
        es['order_id'] = order['order_id'] and str(order['order_id']) or null
        es['pay_type'] = order['pay_type'] and long(order['pay_type']) or null
        es['receipt_at'] = order['receipt_at'] and long(order['receipt_at']) or null
        es['receipt_created_at'] = order['created_at'] and long(order['created_at']) or null
        es['receipt_order_id'] = order['receipt_order_id'] and str(order['receipt_order_id']) or null
        es['receipt_status'] = order['status'] and int(order['status']) or null
        es['shipping_order_id'] = order['shipping_order_id'] and str(order['shipping_order_id']) or null
        es['storage_type_id'] = order['storage_type_id'] and int(order['storage_type_id']) or null
        es['zone_id'] = order['zone_id'] and long(order['zone_id']) or null
        return es

    def getReturnEsData(self, order):
        es = {}
        es['address_id'] = order['address_id'] and long(order['address_id']) or null
        es['cost_money'] = order['cost_money'] and float(order['cost_money']) or null
        es['f_order_id'] = order['f_order_id'] and str(order['f_order_id']) or null
        es['is_mp'] = order['is_mp'] and int(order['is_mp']) or null
        es['is_valid'] = order['is_valid'] and int(order['is_valid']) or null
        es['item_type'] = order['item_type'] and int(order['item_type']) or null
        es['level3'] = self.__level_default_value
        es['level4'] = self.__level_default_value
        es['level5'] = self.__level_default_value
        es['level6'] = self.__level_default_value
        es['level7'] = self.__level_default_value
        es['money'] = order['money'] and float(order['money']) or null
        es['order_id'] = order['order_id'] and str(order['order_id']) or null
        es['pass_at'] = order['pass_at'] and long(order['pass_at']) or null
        es['return_at'] = order['return_at'] and long(order['return_at']) or null
        es['return_order_id'] = order['return_order_id'] and str(order['return_order_id']) or null
        es['return_order_type'] = order['return_order_type'] and int(order['return_order_type']) or null
        es['return_status'] = order['status'] and int(order['status']) or null
        es['return_type'] = order['return_type'] and int(order['return_type']) or null
        es['shipping_order_id'] = order['shipping_order_id'] and str(order['shipping_order_id']) or null
        es['storage_type_id'] = order['storage_type_id'] and int(order['storage_type_id']) or null
        es['type'] = order['type'] and long(order['type']) or null
        es['zone_id'] = order['zone_id'] and long(order['zone_id']) or null
        return es  

    def isUpdate(self, key):
        if key in self.__update_status:
            return True
        else:
            return False

    def isCreate(self, key):
        if key in self.__create_status:
            return True
        else:
            return False

    def isSelect(self, key):
        if key in self.__select_status:
            return True
        else:
            return False
    
    def transform(self, obj):
        es = {}

        es['order_id'] = obj['order_id'] and str(obj['order_id']) or null
        es['zone_id'] = obj['zone_id'] and str(obj['zone_id']) or null
        es['order_status'] = obj['order_status'] and str(obj['order_status']) or null
        es['storage_type_id'] = obj['storage_type_id'] and str(obj['storage_type_id']) or null
        es['ordered_at'] = obj['ordered_at'] and str(obj['ordered_at']) or null
        es['dc_status'] = obj['dc_status'] and str(obj['dc_status']) or null
        es['uid'] = obj['uid'] and str(obj['uid']) or null
        es['so_codes'] = obj['so_codes'] and str(obj['so_codes']) or null
        es['address_id'] = obj['address_id'] and str(obj['address_id']) or null
        es['money'] = obj['money'] and float(obj['money']) or null

        es['market_name'] = obj['market_name'] and str(obj['market_name']) or null
        es['username'] = obj['username'] and str(obj["username"] ) or null
        es['admin_name'] = obj['admin_name'] and str(obj['admin_name']) or null

        es['exception_status'] = null
        es['aftersales_status'] = obj['aftersales_status'] and str(obj['aftersales_status']) or '0'
        
        es['is_comment'] = obj['is_comment'] and str(obj['is_comment']) or null
        
        es['level3'] = obj['level3'] and str(obj['level3']) or '0'
        es['level4'] = obj['level4'] and str(obj['level4']) or '0'
        es['level5'] = obj['level5'] and str(obj['level5']) or '0'
        es['level6'] = obj['level6'] and str(obj['level6']) or '0'
        es['level7'] = obj['level7'] and str(obj['level7']) or '0'
        
        return es

    def __getDocDict(self, order):
        doc = {}

        #aftersales = self.__dao.getAftersales(order['order_code'])
        #if not aftersales:
            #doc['aftersales_status'] = ""
        #else:
            #doc['aftersales_status'] = aftersales['aftersales_status'] and str(aftersales['aftersales_status']) or ""

        #doc['aftersales_status'] = "0"
        doc['so_codes'] = order['so_codes'] and str(order['so_codes']) or null
        #doc['address_id'] = order['address_code'] and str(order['address_code']) or null
        #doc['money'] = order['expect_pay_amount'] and float(order['expect_pay_amount']) or null
        doc['order_status'] = order['order_status'] and str(order['order_status']) or null
        if order['lack_delivery_type']:
            doc['dc_status'] = str(order['lack_delivery_type'])
        else:
            if order['lack_delivery_type'] == None:
                doc['dc_status'] = null
            else:
                doc['dc_status'] = "0"
        return doc

    def __getLevel(self, extObj):
        levels = {};
        '''
        if not extObj:
            return levels
        
        try:
            extObj = json.loads(extObj)
            if not extObj.has_key('saleInfo'):
                return levels

            levelStr = extObj['saleInfo']

            if not levelStr:
                return levels

            for obj in levelStr:
                if obj['level']:
                    levels[str(obj['level'])] = obj['uid']
        except Exception, e:
            raise e
        '''
        return levels

#print(type(configs['es']['create_status']))
#es = Es()
#levelStr = {"saleInfo":[{"id":"8","uid":"3640222739837423437","sales_name":"\u8303\u7ef4\u9f99","f_uid":"0","level":"3","picture":"","status":"1",
#    "created_at":"0","updated_at":"1470215479","main_uid":"3640222739837423437","useraccount":"fanweilong@lsh123.com","zone_id":"1000",
#    "contact_phone":"13771971388"},{"id":"6","uid":"8557309060442556331","sales_name":"\u674e\u7199","f_uid":"3640222739837423437",
#    "level":"4","picture":"","status":"1","created_at":"0","updated_at":"1470215493","main_uid":"8557309060442556331","useraccount":"lixi@lsh123.com",
#    "zone_id":"1000","contact_phone":"18611219500"},{"id":"180","uid":"3684837096098028829","sales_name":"\u674e\u7199\uff08\u7ecf\u7406\uff09",
#    "f_uid":"8557309060442556331","level":"5","picture":"","status":"1","created_at":"1470214197","updated_at":"1470215436",
#    "main_uid":"920049137357605073","useraccount":"lixi01@lsh123.com","zone_id":"1000","contact_phone":null},{"id":"3","uid":"219175825042905776",
#    "sales_name":"\u89e3\u76fc","f_uid":"3684837096098028829","level":"6","picture":"","status":"1","created_at":"0","updated_at":"1472046159",
#    "main_uid":"219175825042905776","useraccount":"xiepan@lsh123.com","zone_id":"1000","contact_phone":"18612387674"},
#    {"id":"199","uid":"7703173891402372818","sales_name":"\u827e\u8fdb","f_uid":"219175825042905776","level":"7","picture":"","status":"1",
#    "created_at":"1471062068","updated_at":"1472994956","main_uid":"7703173891402372818","useraccount":"aijin@lsh123.com","zone_id":"1000",
#    "contact_phone":"18611974843"}],"payCouponMoney":"0"}
#print(es.getLevel(levelStr))