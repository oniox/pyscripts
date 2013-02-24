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

COL_HDR_IDX = 1 #index of column header in tuple

#map of client limits column header index to a tuple of its equivalent in original/source client file, label and type (for validation)
clientLimitsHeaderMap={1:(1,'SESSION ID',str), 3:(2, 'CLIENT ID', str),4:(3,'MAX ORDER SHARES',int),5:(4,'MAX ORDER VALUE',float),6:(5,'DAILY SESSION CONSIDERATION',float),7:(6,'OVERALL CLIENT CONSIDERATION',float),8:(7,'SHORT SELL CHECK',isbool),28:(8,'THRESHOLD',int),29:(9,'THRESHOLDINC',int), 9:(10,'ACTIVE',isbool)}

#map of client session config column header index to a tuple of its equivalent in original/source client file, label and type (for validation)
sessionConfigHeaderMap={1: ( 1, 'CLIENT SESSION ID', str), 2: ( 2, 'VENUE SESSION ID',str), 3: ( 10,'PROTOCOL VERSION', str), 4: (11, 'VENUE REMOTE IP ADDRESS', str), 
	5: (14, 'CARD ID',str), 6: (12, 'VENUE REMOTE PORT',str), 7: (14,'CLIENT REMOTE PORT', str), 8: ( 21,'CANCEL ON DISCONNECT', str), 9: ( 30, 'HEART-BEAT INTERVAL',str), 
	10: (15,'VENUE USERNAME', str), 11: (22, 'CLIENT USER NAME', str), 12: (16, 'VENUE PASSWORD',str), 13: (23, 'CLIENT PASSWORD',str), 14: (17,'VENUE SENDERCOMPID', str), 
	15: (14, 'CLIENT SENDERCOMID',str), 16: (18, 'VENUE TARGETCOMPID',str), 17: (25,'CLIENT TARGETCOMPID', str), 18: (19, 'VENUE SENDERSUBID',str), 19: (26, 'CLIENT SENDERSUBID', str), 
	20: (20,'VENUE TARGETSUBID',str), 21: (27, 'CLIENT TARGETSUBID',str), 22: (30, 'CLIENT GATEWAY IP','str'), 23: (31,'VENUE GATEWAY IP', str), 24: (9,'ACTIVE',  str)}

def fetchRawInputData():
	pass

def parseSymbolRawInput(symbolData):
	emailContentBuf = []
	validateSourceHdrFtr(symbolData, emailContentBuf)
	
	print emailContentBuf
	
	copyData = symbolData[1:]
                
	currentLine = copyData[0].split(',')
	isSymRecComplete = len(currentLine) == len(symbolHeaderMap)
	#print isSymRecComplete
	
	isTickerSymbolBlank = len(currentLine[TICKER_SYMBOL_IDX-1]) == 0
	#print isTickerSymbolBlank
	isShortSellRestrictedEmpty = len(currentLine[SYM_SHORT_SELL_IDX-1]) == 0
	#print isShortSellRestrictedEmpty
	
	isShortSellRestrictedValid = isbool(currentLine[SYM_SHORT_SELL_IDX-1])
	#print isShortSellRestrictedValid

def parseSymbolRec(rec):
	pass
		

def validateSourceHdrFtr(sourceData, emailContentBuf):
	header = getRawInputHeader(sourceData)
	footer = getRawInputFooter(sourceData)
	
	dtValid = isDateValid(header[HEADER_DATE_IDX])
	hdrRecNum = int(header[HEADER_REC_IDX]);
	ftrRecNum = int(footer);
	
	recNumMatch = hdrRecNum == ftrRecNum
	emailContentBuf.append('Header date {0} is valid '.format(header[HEADER_DATE_IDX]))
	
	if recNumMatch:	
		emailContentBuf.append('Header ({0}) and footer  ({1}) record numbers match'.format(hdrRecNum, ftrRecNum))

def getRawInputHeader(inputdata):	
	header = inputdata[0]	
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
	emailContentBuf = []
	validateSourceHdrFtr(clientConfigData, emailContentBuf)
        #take copy of records (omit header and footer)
	clientRecords = clientConfigData[1:len(clientConfigData) - 1]
	ixEyeData = [] #target data list 
	#build column header 
	ixEyeData.append(','.join(col[COL_HDR_IDX] for col in clientLimitsHeaderMap.values()))

        #using data in predefined map, map each client record to ixEye equivalent
        for clientRow in clientRecords:
                clientFields = clientRow.split(',')
                ixEyeRow = []
                for colIdx in clientLimitsHeaderMap.keys():
                        colTuple = clientLimitsHeaderMap[colIdx]
                        ixEyeRecord.append(clientFields[colTuple[0]])
                ixEyeData.append(','.join(ixEyeRecord))
                
	for colIdx in clientLimitsHeaderMap.keys():
                rec = records[colIdx]
                if len(rec) == len(clientLimitsHeaderMap):
                        tokens = rec.split(',');
                        for i,tok in enumerate(tokens):
                                client
                        
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

rawClientConfigToIxEye(lines)

"""
test.txt
13/12/2012,4
TD,N,0.01,2,70.08,Y
BMO,Y,0.01,2,50.08,Y
RY,Y,0.01,2,60.08,Y
4
"""
