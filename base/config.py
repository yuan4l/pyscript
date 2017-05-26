#config

configs = {
	# 'es' : {
	# 	'ip' : 'http://192.168.60.151:9200/oms/order/',
	# 	'tms_ip' : 'http://192.168.60.151:9200/tms_search/',
	# 	'create_status' : {'201', '409'},
	# 	'update_status' : {'200', '201'},
	# 	'select_status' : {'200'}
	# },
	'es' : {
		'ip' : 'http://127.0.0.1:9200/oms/order/',
		# 'tms_ip' : 'http://192.168.60.151:9200/tms_search/',
		'create_status' : {'201', '409'},
		'update_status' : {'200', '201'},
		'select_status' : {'200'}
	},
	# 'oms' : {
	# 	'host' : '192.168.60.152',
	# 	'port' : '5300',
	# 	'username' : 'order',
	# 	'password' : 'Lsh@Order2016',
	# 	'db' : 'lsh_oms'
	# },
	'oms' : {
		'host' : '192.168.60.48',
		'port' : '5201',
		'username' : 'root',
		'password' : 'root123',
		'db' : 'lsh_oms'
	},
	'ofc' : {
		'host' : '192.168.60.152',
		'port' : '5300',
		'username' : 'order',
		'password' : 'Lsh@Order2016',
		'db' : 'lsh_ofc'
	},
	'market' : {
		'host' : '192.168.60.153',
		'port' : '3317',
		'username' : 'yg01',
		'password' : 'lshygdba',
		'db' : 'lsh_market'
	},
	'email' : {
		"smtp": "smtp.qiye.163.com",
	        "auth": {
	            "username": "panxudong@lsh123.com",
	            "password": "Pxd921206."
	        },
	        #"to": ["fuhao@lsh123.com","panxudong@lsh123.com"]
		"to": ["aop@lsh123.com"]
	}
}
