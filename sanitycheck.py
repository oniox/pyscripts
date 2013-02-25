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
		
CONFIG_FILE='C:/dev/projects/python/pyscripts/resources/sanitycheck.config'

HEADER_DATE_IDX=0
HEADER_REC_IDX=1		
MAX_HEADER_TOK_LEN = 2;
MAX_FOOTER_LEN = 1;

SYMBOL_DATE_FORMAT='%d/%m/%Y'
TICKER_SYMBOL_IDX = 1
SYM_SHORT_SELL_IDX = 2
SYMBOL_COL_IDX = 0

PROP_SYMBOL_DIR='symbol.dir'
PROP_CLIENTCON_DIR='clientconfig.dir'
PROP_CLIENTCON_FILE='clientconfig.fileformat'
PROP_SYMBOL_FILE='symbol.fileformat'

#map of symbol column header index to a tuple of its label and data type (for validation)
symbolHeaderMap={TICKER_SYMBOL_IDX : ('TICKER SYMBOL', str), SYM_SHORT_SELL_IDX : ('SHORT SELL RESTRICTED', isbool), 3 :  ('MIN TICK SIZE', float), 4 : ('MAX PRICE DEVIATION', int), 5 : ('PREVIOUS CLOSE PRICE', float) , 6 : ('ACTIVE', bool)}

COL_HDR_IDX = 1 #index of column header in tuple

#map of client limits column header index to a tuple of its equivalent in original/source client file, label and type (for validation)
clientLimitsHeaderMap={1:(1,'SESSION ID',str), 2:(3, 'CLIENT ID', str),3:(4,'MAX ORDER SHARES',int),4:(5,'MAX ORDER VALUE',float),5:(6,'DAILY SESSION CONSIDERATION',float),6:(7,'OVERALL CLIENT CONSIDERATION',float),7:(8,'SHORT SELL CHECK',isbool),8:(28,'THRESHOLD',int),9:(29,'THRESHOLDINC',int), 10:(9,'ACTIVE',isbool)}

#map of client session config column header index to a tuple of its equivalent in original/source client file, label and type (for validation)
sessionConfigHeaderMap={1: ( 1, 'CLIENT SESSION ID', str), 2: ( 2, 'VENUE SESSION ID',str), 3: ( 10,'PROTOCOL VERSION', str), 4: (11, 'VENUE REMOTE IP ADDRESS', str), 
	5: (14, 'CARD ID',str), 6: (12, 'VENUE REMOTE PORT',str), 7: (14,'CLIENT REMOTE PORT', str), 8: ( 21,'CANCEL ON DISCONNECT', str), 9: ( 30, 'HEART-BEAT INTERVAL',str), 
	10: (15,'VENUE USERNAME', str), 11: (22, 'CLIENT USER NAME', str), 12: (16, 'VENUE PASSWORD',str), 13: (23, 'CLIENT PASSWORD',str), 14: (17,'VENUE SENDERCOMPID', str), 
	15: (14, 'CLIENT SENDERCOMID',str), 16: (18, 'VENUE TARGETCOMPID',str), 17: (25,'CLIENT TARGETCOMPID', str), 18: (19, 'VENUE SENDERSUBID',str), 19: (26, 'CLIENT SENDERSUBID', str), 
	20: (20,'VENUE TARGETSUBID',str), 21: (27, 'CLIENT TARGETSUBID',str), 22: (30, 'CLIENT GATEWAY IP','str'), 23: (31,'VENUE GATEWAY IP', str), 24: (9,'ACTIVE',  str)}


def loadConfigFile():
	f = open(CONFIG_FILE, 'r')
	configs = f.readlines()	
	configmap = {}
	
	for row in configs:
		configmap.update(([row.split('=')]))
	return configmap
	"""
	for row in configs:
		keyval=row.split('=')
		print keyval
        configmap[keyval[0]] = keyval[1]
	return configmap
	"""
        

def loadSymbolData():
	config = loadConfigFile()
	print config
	folder = config[PROP_SYMBOL_DIR]
	file = config[PROP_SYMBOL_FILE]
	
	filetoks = file.split('.')	
	
	dtToday  = date.today().strftime(filetoks[1])	
	lst = os.listdir(folder.strip())	
	filetoks[1]=dtToday
	expectedname =  '.'.join(filetoks)	
	print expectedname in  lst
	
	#filedate=datetime.strptime(filetoks[1], '%d%m%y%H%M')
	
	#strlbl = date.today().strftime(filetoks[1])
	#filetoks[1] = strlbl
		
	#if filedate.date == date.today():
		
	
			
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
        emailContentBuf = []
	validateSourceHdrFtr(symbolData, emailContentBuf)

	ixEyeData = [] #target data list 
	#build column header 
	ixEyeData.append(','.join(col[SYMBOL_COL_IDX] for col in symbolHeaderMap.values()))
        #take copy of client records (omit header and footer)
	clientRecords = symbolData[1:len(symbolData) - 1]
	ixEyeData.append(''.join(clientRecords))

        #saveToIExEyeFile(ixEyeData, os.sys.argv[2])
	writeListToFile(ixEyeData, os.sys.argv[2])
	pass
	"""
	for x,token in enumerate(symbolData):s
		mapval = symbolHeaderMap[x+1]		
		validator = mapval[1]	
		print validator(token)	
		#print token		
        """

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
                        ixEyeRow.append(clientFields[colTuple[0] - 1]) # get equivalent value from source data  
                ixEyeData.append(','.join(ixEyeRow))
		writeListToFile(ixEyeData, os.sys.argv[2])
	pass

def writeListToFile(data, filename):
	f=open(filename, 'w')        
        for item in ixEyeData:
          print>>f, item
		
def sendmail(content):
	pass

if len(os.sys.argv) < 2:
	raise Exception('Usage {0} inputfilename'.format(os.sys.argv[0]))

f=open(os.sys.argv[1])
	
lines = f.readlines()

loadSymbolData()

#parseSymbolRawInput(lines)

#rawClientConfigToIxEye(lines)

#print loadConfigFile()

#rawSymbolDataToIxEye(lines)

"""
test.txt
13/12/2012,4
TD,N,0.01,2,70.08,Y
BMO,Y,0.01,2,50.08,Y
RY,Y,0.01,2,60.08,Y
4
"""
