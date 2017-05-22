#encoding=utf-8
import sys
sys.path.append('..')

from base.dao import Dao

dao = Dao()

sql = 'select count(id) from ofc_task where status=3 and exec_count=10'
total = dao.executeOfcSelectSql(sql)

if total > 0:
	sql = 'update ofc_task set exec_count=9 where status=3 and exec_count=10'
	dao.executeOfcSql(sql)
