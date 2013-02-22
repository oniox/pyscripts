import os
import io
from datetime import date
from datetime import datetime

#functor to handle special (i.e Y/N) boolean validation 	
def isbool(value):			
	if boolMap[value] is not None:
		return value
	else: 
		raise ValueError('Value {0} not a boolean'.format(value))

HEADER_DATE_IDX=0
HEADER_REC_IDX=1		
MAX_HEADER_TOK_LEN = 2;
MAX_FOOTER_LEN = 1;
SYMBOL_DATE_FORMAT='%d/%m/%Y'
TICKER_SYMBOL_IDX = 1
SHORT_SELL_IDX = 2
symbolHeaderMap={TICKER_SYMBOL_IDX : ('TICKER SYMBOL', str), SHORT_SELL_IDX : ('SHORT SELL RESTRICTED', isbool), 3 :  ('MIN TICK SIZE', float), 4 : ('MAX PRICE DEVIATION', int), 5 : ('PREVIOUS CLOSE PRICE', float) , 6 : ('ACTIVE', bool)}

def fetchRawInputData():
	pass

def parseSymbolRawInput(symbolData):
	symbolHdr = getRawInputHeader(symbolData)
	symbolFtr = getRawInputFooter(symbolData)
	
	dtValid = isDateValid(symbolHdr[HEADER_DATE_IDX])
	recNumMatch = int(symbolHdr[HEADER_REC_IDX]) == int(symbolFtr)
	print 'Date Valid : {0}'.format(dtValid)
	print 'Rec Num match :', recNumMatch
	
	copyData = symbolData[1:]
	
	isSymRecComplete = len(copyData[0].split(',')) == len(symbolHeaderMap)
	print isSymRecComplete
	
	isTickerSymbolBlank = len(copyData[0].split(',')[TICKER_SYMBOL_IDX-1]) == 0
	print isTickerSymbolBlank
	isShortSellRestrictedEmpty = len(copyData[0].split(',')[SHORT_SELL_IDX-1]) == 0
	print isShortSellRestrictedEmpty

def parseSymbolRec(rec):
	pass
		
def getRawInputHeader(inputdata):	
	header=inputdata[0]
	#print 'Header info : {0}'.format(header)
	headerToks = header.split(',')
	if len(headerToks) is MAX_HEADER_TOK_LEN:
		return headerToks
	else:
		raise Exception('Invalid header {0}, header should be of two values'.format(header))
		

def getRawInputFooter(inputdata):	
	return inputdata[-1].strip()	
	

def isDateValid(recdate):
	try:
		dt = datetime.strptime(recdate, SYMBOL_DATE_FORMAT)	
		return type(dt) is datetime
	except Exception as e:
		print 'Invalid header date \'{0}\', date should be in format {1} eg 13/12/2012 {2}'.format(recdate, SYMBOL_DATE_FORMAT, e) 
		return False
		

def rawSymbolDataToIxEye(symbolData):
	for x,token in enumerate(symbolData):
		mapval = symbolHeaderMap[x+1]		
		validator = mapval[1]	
		print validator(token)	
		#print token		
		
def sendmail(content):
	pass

if len(os.sys.argv) < 2:
	raise Exception('Usage {0} inputfilename'.format(os.sys.argv[0]))

f=open(os.sys.argv[1])


if not f:
	raise Exception('No such file {0}'.format(os.sys.argv[1]))  
	
lines = f.readlines()

parseSymbolRawInput(lines)

#lineTokens=lines[1].split(',')
#print lineTokens

"""
for x,token in enumerate(lineTokens):
	mapval = symbolHeaderMap[x+1]
	validator = mapval[1]	
	print validator(token)	
	#print token
"""
	
#print isDateValid(getRawInputHeader(lines)[0])
#print isDateValid('12/12/2012')



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
	
	