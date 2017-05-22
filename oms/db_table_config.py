#config

db_table_configs = {
	'1' : {
		'table' : 'order_head',
		'key' : 'order_code',
		'col' : ['order_status']
	},
	'2' : {
		'table' : 'order_shipping_head',
		'key' : 'shipping_order_id',
		'col' : ['status']
	},
	'3' : {
		'table' : 'order_sign_head',
		'key' : 'receipt_order_id',
		'col' : ['status']
	},
	'4' : {
		'table' : 'order_ro_head',
		'key' : 'return_order_id',
		'col' : ['status']
	}
}