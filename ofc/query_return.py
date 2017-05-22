import requests
import json

codes=[6588533252659876949,
8320167308871638104,
7304183369872260465,
7985915729983105039,
9044824578056977200,
57047093244749472,
6822579632949272496,
8595871955627175595,
3212522269172115045]
prefix='http://192.168.60.151:9501/ofc/api/return/ro/status/query?returnCode='
headers = {'api-version':'1.0','random':'123','platform':'tms'}
notExist2101 = []
notExist2103 = []
other = []
for code in codes:
	url=prefix + str(code)	
	res=requests.get(url, headers=headers)
	print(res.text)
	obj = json.loads(res.text)
	if obj['code'] == 'E2101':
		notExist2101.append(code)
	elif obj['code'] == 'E2103':
		notExist2103.append(code) 
	else:
		other.append(code)

print(len(notExist2101))
print('2101:' + json.dumps(notExist2101))
print('\n' + str(len(notExist2103)))
print('2103:' + json.dumps(notExist2103))
print('\n' + str(len(other)))
print('other:' + json.dumps(other))
