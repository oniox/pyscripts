import os
import io
from datetime import date
from datetime import datetime


MAX_HEADER_TOK = 2;
SYMBOL_DATE_FORMAT='%d/%m/%Y'
symbolHeaderMap={1 : ('TICKER SYMBOL', str), 2 : ('SHORT SELL RESTRICTED', bool), 3 :  ('MIN TICK SIZE', float), 4 : ('MAX PRICE DEVIATION', int), 5 : ('PREVIOUS CLOSE PRICE', float) , 6 : ('ACTIVE', bool)}


def fetchRawInputData():
	pass

def parseRawInput(value):
	print value
	
def getRawInputHeader(inputdata):	
	header=inputdata[0]
	#print 'Header info : {0}'.format(header)
	headerToks = header.split(',')
	if len(headerToks) is MAX_HEADER_TOK:
		return headerToks
	else:
		raise Exception('Invalid header {0}, header should be of two values'.format(header))

def isDateValid(recdate):
	dt = datetime.strptime(recdate, SYMBOL_DATE_FORMAT)	
	return type(dt) is datetime

def rawSymbolDataToIxEye(symbolData):
	pass
	
def sendmail(content):
	pass

if len(os.sys.argv) < 2:
	raise Exception('Usage {0} inputfilename'.format(os.sys.argv[0]))

f=open(os.sys.argv[1])


if not f:
	raise Exception('No such file {0}'.format(os.sys.argv[1]))  
	
lines = f.readlines()


print getRawInputHeader(lines)[0]
print isDateValid(getRawInputHeader(lines)[0])



#header=lines[0]

#print 'Header info : {0}'.format(header)

#headerToks = header.split(',')
#if len(headerToks) is 2:
#	headerRecNum = headerToks[1]
#	headerDate = headerToks[0]
	
#footerRecNum = lines[-1]

#print headerRecNum
#print headerDate
#print symbolHeaderMap[1][0]
#for line in lines:
#	print line
	
	