from dao import Dao
from config import configs
from es import Es
from log import Log
import json
import time
import smtplib

class Base(object):

	def __init__(self):
		log = Log()
		self.__dao = Dao()
		self.__logger = log.getLogger() 
		self.__es = Es()

	def getRange(self):
		result = self.__dao.getOrderHeadIdRange()
		return (result['min'], result['max'])

	def getHeaders(self):
		headers = {'Content-type':'application/json; charset=utf-8', 'Accept':'application/json'}
		return headers

	def execute(self, method):
		esConfig = configs['es']
		headers = self.getHeaders()
		page = self.getRange()

		minId = page[0]
		#minId = 453835
		maxId = page[1]
		print("min:%d  max:%d" % (minId,maxId))
	
		total = 0

		startTime = time.clock()
		start = minId
		end = 1000
		flag = False
		while minId<=maxId:
			if not flag:
				start = minId
				end = 1000
				#end = 454835
				flag = True
			else:
				start = minId
				end += 1000
			startExecuteTime = time.clock()
			result = method(start, end, headers, esConfig, self.__es, self.__dao, self.__logger)
			endExecuteTime = time.clock()
			print("Num:%d  Execute time:%.03f sec" % (result, endExecuteTime - startExecuteTime))
			
			total += result
			minId+=1000
		endTime = time.clock()
		print("Total:%d  Execute time:%.03f sec" % (total, endTime - startTime))

	def executeMendDbData(self, db_table_configs, executeSelectSql, executeSql):
		while True:
			print("Please choose table type:")
			keys = db_table_configs.keys()
			keys.sort()
			for key in keys:
				print("  " + key + "." + db_table_configs[key]['table'])
			table = raw_input("Table type:")
			table = table.strip()
			if not db_table_configs.has_key(table):
				print("Input table type is not correct, please input again!")
				continue

			tableCols = db_table_configs[table]['col']
			tableName = db_table_configs[table]['table']
			tableKey = db_table_configs[table]['key']

			while True:
				data = {}
				isHaveValue = False	
				print("Please input value:")
				tableKeyValue = raw_input("  " + tableKey + ":")
				for col in tableCols:
					value = raw_input("  " + col + ":")
					data[col] = value.strip()
					if data[col]:
						isHaveValue = True

				if not isHaveValue:
					print("Please input need update value!")
					continue

				#print("Please check data:\n  " + "key:" + tableKeyValue + "\n  data:" + json.dumps(data))
				#isTrue = raw_input("If true, please input y, not input n:")
				#isTrue = isTrue.strip()
				#if isTrue == 'n' or isTrue == 'n'.upper():
					#print("Please input again!")
					#continue

				sql = self.__getSelectSql(tableKey, tableCols, tableName) + " from " + tableName + " where " + tableKey + "=" + tableKeyValue
				result = executeSelectSql(sql)
				while True:
					print("Database data:")
					flag = 1
					for res in result:
						print("  index:" + str(flag) + " data:" + json.dumps(res))
						flag+=1
					index = raw_input("Please choose need update data index:")
					index = int(index)
					if index < 1 or index > len(result):
						#print("Index error, please choose again!")
						continue
					break
				id = result[index - 1]['id']

				sql = 'update ' + tableName + " set "
				i = 0
				for key in data.keys():
					if not data[key]:
						i+=1
						continue
					sql += key + "=" + data[key] 
					if i != len(data) - 1:
						sql += ","
					i+=1
				sql += " where id=" + str(id)
				
				print("Please check sql : " + sql)
				isTrue = raw_input("If true, please input y, not input n:")
				isTrue = isTrue.strip()
				if isTrue == 'n' or isTrue == 'n'.upper():
					#print("Please input again!")
					continue

				result = executeSql(sql)
				print("Affect columns:" + str(result))
				
				sql = self.__getSelectSql(tableKey, tableCols, tableName) + " from " + tableName + " where id=" + str(id)
				result = executeSelectSql(sql)
				print("Data:" + json.dumps(result))
				isTrue = raw_input("Please check data, if true, please input y, not input n:")
				isTrue = isTrue.strip()
				if isTrue == 'n' or isTrue == 'n'.upper():
					#print("Please input again!")
					continue
				break
			break

	def analysisBulkLog(self, text, prefix="update"):
		logObj = json.loads(text)
		if not logObj['errors']:
			return
		if logObj['errors'] == 'false':
			return
		items = logObj['items']
		for item in items:
			detail = item[prefix]
			if not detail:
				self.__logger.error("[preifx:%s][item:%s]prefix error!" % (prefix,json.dumps(detail)))
				return
			flag = False

			if prefix == "update":
				if not self.__es.isUpdate(detail['status']):
					flag = True
			else:
				if not self.__es.isCreate(detail['status']):
					flag = True

			if not flag:
				self.__logger.error("[%s][%s]" % (detail['_id'], json.dumps(detail['error'])))

	def __getSelectSql(self, tableKey, tableCols, tableName):
		sql = "select id," + tableKey + ","
		flag = 0
		for col in tableCols:
			sql += col
			if flag != len(tableCols) - 1:
				sql += ","
			flag+=1
		return sql

	def sendEmail(self, smtpServer, fromAddr, password, toAddr, msg):
		server = smtplib.SMTP(smtpServer, 25)
		server.set_debuglevel(1)
		server.login(fromAddr, password)
		server.sendmail(fromAddr, toAddr, msg.as_string())
		server.quit()
