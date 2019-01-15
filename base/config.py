#config

configs = {
	# 'es' : {
	# 	'ip' : 'http://127.0.0.1:9200/oms/order/',
	# 	'tms_ip' : 'http://127.0.0.1:9200/tms_search/',
	# 	'create_status' : {'201', '409'},
	# 	'update_status' : {'200', '201'},
	# 	'select_status' : {'200'}
	# },
	'es' : {
		'ip' : 'http://127.0.0.1:9200/oms/order/',
		# 'tms_ip' : 'http://127.0.0.1:9200/tms_search/',
		'create_status' : {'201', '409'},
		'update_status' : {'200', '201'},
		'select_status' : {'200'}
	},
	# 'oms' : {
	# 	'host' : '127.0.0.1',
	# 	'port' : '5300',
	# 	'username' : 'user',
	# 	'password' : 'Order2016',
	# 	'db' : 'lsh_oms'
	# },
	'oms' : {
		'host' : '127.0.0.1',
		'port' : '5201',
		'username' : 'user',
		'password' : 'root123',
		'db' : 'lsh_oms'
	},
	'ofc' : {
		'host' : '127.0.0.1',
		'port' : '5300',
		'username' : 'order',
		'password' : 'Order2016',
		'db' : 'lsh_ofc'
	},
	'market' : {
		'host' : '127.0.0.1',
		'port' : '3317',
		'username' : 'yg01',
		'password' : 'lshygdba',
		'db' : 'lsh_market'
	},
	'email' : {
		"smtp": "smtp.qiye.163.com",
	        "auth": {
	            "username": "123@123.com",
	            "password": "921206."
	        },
	        #"to": ["123@123.com","123@123.com"]
		"to": ["123@123.com"]
	}
}
