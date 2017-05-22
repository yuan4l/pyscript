#encoding=utf-8
import sys
sys.path.append('..')

from base.dao import Dao
from base.base import Base
from db_table_config import db_table_configs
import json

base = Base()
dao = Dao()

base.executeMendDbData(db_table_configs, dao.executeOmsSelectSql, dao.executeOmsSql)