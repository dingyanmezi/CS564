import sys
from json import loads
from re import sub

shu = 0
xian = 'I am wondering " if you could shut " the fuck up'
finalxian = ''
zifumen = []
indexmen = []
for babe in xian:
	zifumen.insert(shu, babe)
	if babe == '"':
		indexmen.append(shu)
	shu = shu + 1

shu2 = len(indexmen)-1
while shu2 >= 0:
	zifumen.insert(indexmen[shu2], '"')
	shu2 = shu2 - 1
for babe2 in zifumen:
	finalxian = finalxian + babe2
print finalxian

