import os
import io
from datetime import date
from datetime import datetime

#functor to handle special (i.e Y/N) boolean validation 	
def isbool(value):			
	if value in ['Y','N']:
		return bool(1)
	else: 
		return bool(0)

HEADER_DATE_IDX=0
HEADER_REC_IDX=1		
MAX_HEADER_TOK_LEN = 2;
MAX_FOOTER_LEN = 1;

SYMBOL_DATE_FORMAT='%d/%m/%Y'
TICKER_SYMBOL_IDX = 1
SYM_SHORT_SELL_IDX = 2
#map of symbol column header index to a tuple of its label and data type (for validation)
symbolHeaderMap={TICKER_SYMBOL_IDX : ('TICKER SYMBOL', str), SYM_SHORT_SELL_IDX : ('SHORT SELL RESTRICTED', isbool), 3 :  ('MIN TICK SIZE', float), 4 : ('MAX PRICE DEVIATION', int), 5 : ('PREVIOUS CLOSE PRICE', float) , 6 : ('ACTIVE', bool)}

#map of client limits column header index to a tuple of its equivalent in original/source client file, label and type (for validation)
clientLimitsHeaderMap={1:(1,'SESSION ID',str), 2:(3, 'CLIENT ID', str),3:(4,'MAX ORDER SHARES',int),4:(5,'MAX ORDER VALUE',float),5:(6,'DAILY SESSION CONSIDERATION',float),6:(7,'OVERALL CLIENT CONSIDERATION',float),7:(8,'SHORT SELL CHECK',isbool),8:(28,'THRESHOLD',int),9:(29,'THRESHOLDINC',int), 10:(9,'ACTIVE',isbool)}

#map of client session config column header index to a tuple of its equivalent in original/source client file, label and type (for validation)
sessionConfigHeaderMap={1: ( 1, 'CLIENT SESSION ID', str), 2: ( 2, 'VENUE SESSION ID',str), 3: ( 10,'PROTOCOL VERSION', str), 4: (11, 'VENUE REMOTE IP ADDRESS', str), 
	5: (14, 'CARD ID',str), 6: (12, 'VENUE REMOTE PORT',str), 7: (14,'CLIENT REMOTE PORT', str), 8: ( 21,'CANCEL ON DISCONNECT', str), 9: ( 30, 'HEART-BEAT INTERVAL',str), 
	10: (15,'VENUE USERNAME', str), 11: (22, 'CLIENT USER NAME', str), 12: (16, 'VENUE PASSWORD',str), 13: (23, 'CLIENT PASSWORD',str), 14: (17,'VENUE SENDERCOMPID', str), 
	15: (14, 'CLIENT SENDERCOMID',str), 16: (18, 'VENUE TARGETCOMPID',str), 17: (25,'CLIENT TARGETCOMPID', str), 18: (19, 'VENUE SENDERSUBID',str), 19: (26, 'CLIENT SENDERSUBID', str), 
	20: (20,'VENUE TARGETSUBID',str), 21: (27, 'CLIENT TARGETSUBID',str), 22: (30, 'CLIENT GATEWAY IP','str'), 23: (31,'VENUE GATEWAY IP', str), 24: (9,'ACTIVE',  str)}

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
	
	currentLine = copyData[0].split(',')
	isSymRecComplete = len(currentLine) == len(symbolHeaderMap)
	print isSymRecComplete
	
	isTickerSymbolBlank = len(currentLine[TICKER_SYMBOL_IDX-1]) == 0
	print isTickerSymbolBlank
	isShortSellRestrictedEmpty = len(currentLine[SYM_SHORT_SELL_IDX-1]) == 0
	print isShortSellRestrictedEmpty
	
	isShortSellRestrictedValid = isbool(currentLine[SYM_SHORT_SELL_IDX-1])
	print isShortSellRestrictedValid

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


def rawClientConfigToIxEye(clientConfigData):
	pass
	
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


data='CLIENT SESSION ID,VENUE SESSION ID,PROTOCOL VERSION,VENUE REMOTE IP ADDRESS,CARD ID,VENUE REMOTE PORT,CLIENT REMOTE PORT,CANCEL ON DISCONNECT,HEART-BEAT INTERVAL,VENUE USERNAME,CLIENT USER NAME,VENUE PASSWORD,CLIENT PASSWORD,VENUE SENDERCOMPID,CLIENT SENDERCOMID,VENUE TARGETCOMPID,CLIENT TARGETCOMPID,VENUE SENDERSUBID,CLIENT SENDERSUBID,VENUE TARGETSUBID,CLIENT TARGETSUBID,CLIENT GATEWAY IP,VENUE GATEWAY IP,ACTIVE'	
lol=data.split(',')
print 'Len lol ', len(lol)
mappy=dict()

for x,l in enumerate(lol):
	mappy[x+1]=(0,l,'str')	
print mappy