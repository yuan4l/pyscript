import logging

class Log(object):
	"""docstring for Log"""
	def __init__(self):
		logging.basicConfig(level=logging.INFO,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename='es.log',
                filemode='w')

		# console = logging.StreamHandler()
		# console.setLevel(logging.INFO)
		# formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
		# console.setFormatter(formatter)
		# logging.getLogger('').addHandler(console)

		self.__logger = logging

	def getLogger(self):
		return self.__logger


