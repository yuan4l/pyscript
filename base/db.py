#encoding:utf8

import sys
reload(sys)
sys.setdefaultencoding('utf8')

import MySQLdb
import MySQLdb.cursors

class MysqlHelper(object):
	def __init__(self, config):
		self.__config = config

	def __get_connection(self):
		self.__conn = MySQLdb.connect(host=self.__config['host'],port=int(self.__config['port']),user=self.__config['username'],passwd=self.__config['password'],db=self.__config['db'],charset = 'utf8',)
		self.__cursor = self.__conn.cursor(MySQLdb.cursors.DictCursor)
		self.__cursor.execute("set names 'utf8'")
		return self.__cursor

	def __find(self, sql, is_one=False):
		try:
			cursor = self.__get_connection()
    			cursor.execute(sql)
	    		if is_one :
	    			result = cursor.fetchone()
	    		else :
	    			result = cursor.fetchall()
			return result
		except MySQLdb.Error,e:
			print "Mysql Error %d: %s" % (e.args[0], e.args[1])
			raise Exception()
		finally:
			self.__cursor.close()
			self.__conn.close()

	def findOne(self, sql):
		return self.__find(sql, True)

	def findList(self, sql):
		return self.__find(sql)

	def executeSql(self, sql):
		try:
			cursor = self.__get_connection()
    			result = cursor.execute(sql)
    			self.__conn.commit()
    			return result
		except MySQLdb.Error,e:
			print "Mysql Error %d: %s" % (e.args[0], e.args[1])
			self.__conn.rollback()
			raise Exception()
		finally:
			self.__cursor.close()
			self.__conn.close()
		return 