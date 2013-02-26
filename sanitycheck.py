                                                                     
                                                                     
                                                                     
                                             
import os
import io
import logging
from datetime import date
from datetime import datetime
import smtplib
from email.mime.text import MIMEText

#functor to handle special (i.e Y/N) boolean validation 	
def isbool(value):			
	if value in ['Y','N']:
		return bool(1)
	else: 
		return bool(0)
		
CONFIG_FILE='sanitycheck.config'

logger = logging.getLogger('sanitychecker')
logger.setLevel(logging.INFO)
# create file handler which logs even debug messages
fh = logging.FileHandler('sanitychecker.log')
fh.setLevel(logging.INFO)
# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.ERROR)
# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)
# add the handlers to the logger
logger.addHandler(fh)
logger.addHandler(ch)

HEADER_DATE_IDX=0
HEADER_REC_IDX=1		
MAX_HEADER_TOK_LEN = 2;
MAX_FOOTER_LEN = 1;
MAX_CLIENT_REC_LEN=32

SYMBOL_DATE_FORMAT='%d/%m/%Y'
TICKER_SYMBOL_IDX = 1
SYM_SHORT_SELL_IDX = 2
SYMBOL_COL_IDX = 0
SYMBOL_TYPE_IDX = 1
CLIENTCFG_TYPE_IDX = 2

PROP_SYMBOL_DIR='symbol.dir'
PROP_CLIENTCON_DIR='clientconfig.dir'
PROP_CLIENTCON_FILE='clientconfig.fileformat'
PROP_SYMBOL_FILE='symbol.fileformat'
PROP_IXEYE_OUT_DIR='ixeye.out.dir'

PROP_SMTP_HOST='mail.smtp.host'
PROP_SMTP_USER='mail.user'
PROP_SENDER_EMAIL='mail.from'
PROP_CLIENT_EMAIL='mail.to'

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
	20: (20,'VENUE TARGETSUBID',str), 21: (27, 'CLIENT TARGETSUBID',str), 22: (30, 'CLIENT GATEWAY IP',str), 23: (31,'VENUE GATEWAY IP', str), 24: (9,'ACTIVE',  str)}


def loadProperties(configfile=CONFIG_FILE):
	try:
		f = open(configfile, 'r')
		props = f.readlines()	
		propsmap = {}	
		for row in props:
			propsmap.update(([row.split('=')]))
		return propsmap
	except Exception as e:
		logger.error(e)
		raise Exception("File processing failed as script config file failed to load {0} ".format(str(e)))

def rawSymbolDataToIxEye(symbolData, emailContentBuf):    
	validateSourceHdrFtr(symbolData, emailContentBuf)		
	ixEyeData = [] #target data list 
	#build column header 
	ixEyeData.append(','.join(col[SYMBOL_COL_IDX] for col in symbolHeaderMap.values()))
    #take copy of client records (omit header and footer)
	clientRecords = symbolData[1:len(symbolData) - 1]
	validatedRecords = validateSymbolData(clientRecords, emailContentBuf)	
	emailBuf.append("{0} records successfully validated for loading into symbols file".format(len(validatedRecords)))
	ixEyeData.append(''.join(validatedRecords))	
	return ixEyeData	

def validateSymbolData(symbolData, emailBuffer):
	validatedRecords = []
	validRecLen = len(symbolHeaderMap)	
	for rec in symbolData:		
		recList=rec.split(',')
		recLen = len(recList)
		if recLen is not validRecLen:
			emailBuffer.append("Record {0} will not be loaded as it contains {1} records, {2} records expected".format(str(rec).strip(), recLen, validRecLen))
			continue
		elif len(recList[SYM_SHORT_SELL_IDX-1]) == 0:
			recList[SYM_SHORT_SELL_IDX-1] = 'N'
			rec = ','.join(recList)			
		if '' in recList:			
			blankColumn = getSymbolColName(recList.index('') + 1)
			emailBuffer.append("Record {0} will not be loaded because it contains a blank {1} value".format(str(rec), blankColumn))
			continue
		for colIdx,fieldval in enumerate(recList):			
			validator = symbolHeaderMap[colIdx+1][SYMBOL_TYPE_IDX]			
			try:
				validator(fieldval)
			except ValueError as ve:				
				emailBuffer.append("Record {0} will not be loaded because value {1} of field {2} is of wrong type ".format(str(rec), fieldval, getSymbolColName(colIdx+1)))
				continue		
		validatedRecords.append(rec)	
	return validatedRecords

def getSymbolColName(colIdx):
	return symbolHeaderMap[colIdx][SYMBOL_COL_IDX]

def rawClientLimitsToIxEye(clientConfigData, emailContentBuf):		
	return rawClientConfigToIxEye(clientConfigData, clientLimitsHeaderMap, emailContentBuf) 

def rawSessionConfigToIxEye(clientConfigData, emailContentBuf):		
	return rawClientConfigToIxEye(clientConfigData, sessionConfigHeaderMap, emailContentBuf) 
	
def rawClientConfigToIxEye(clientConfigData, colHeaderMap, emailContentBuf):	
	validateSourceHdrFtr(clientConfigData, emailContentBuf)
    #apply validation copy of records (omit header and footer)
	clientRecords = validateClientConfigData(clientConfigData[1:len(clientConfigData) - 1], colHeaderMap, emailContentBuf)	
	ixEyeData = [] #target data list 
	#build column header 
	ixEyeData.append(','.join(col[COL_HDR_IDX] for col in colHeaderMap.values()))        
	#using data in predefined map, map each client record to ixEye equivalent
	for clientRow in clientRecords:
		clientFields = clientRow.split(',')               
		ixEyeRow = []
		for colIdx in colHeaderMap.keys():
			colTuple = colHeaderMap[colIdx]
			fieldval = clientFields[colTuple[0] - 1] # get equivalent value from source data			
			validator = colTuple[CLIENTCFG_TYPE_IDX]			
			try:
				if len(fieldval) is not 0:
					validator(fieldval)
			except ValueError as ve:				
				emailContentBuf.append("Record {0} will not be loaded because value {1} of field {2} is of wrong type ".format(clientRow, fieldval, getSymbolColName(colIdx+1)))
				ixEyeRow = [] #value of invalid type detected in this row, reset row and abort row validation
				break		
			ixEyeRow.append(fieldval)
		if  len(ixEyeRow) is not 0:
			ixEyeData.append(','.join(ixEyeRow))
	emailBuf.append("{0} records successfully validated for loading from client configuration file".format(len(ixEyeData)-1)) #omit header info
	return ixEyeData

def validateClientConfigData(clientConfigData, colHeaderMap, emailBuffer):	
	validatedRecords = []
	validRecLen = MAX_CLIENT_REC_LEN			
	for rec in clientConfigData:		
		recList=rec.split(',')
		recLen = len(recList)
		if recLen is not validRecLen:
			emailBuffer.append("Record {0} will not be loaded as it contains {1} records, {2} records expected".format(str(rec).strip(), recLen, validRecLen))
			continue			
		validatedRecords.append(rec)
	return validatedRecords

def validateSourceHdrFtr(sourceData, emailContentBuf):
	header = getRawInputHeader(sourceData)
	dtValid = isHdrDateValid(header[HEADER_DATE_IDX])
	footer = getRawInputFooter(sourceData)
	validateHdrFtrValue(header, footer)	
	
def validateHdrFtrValue(header, footer):		
	try:
		hdrRecNum = int(header[HEADER_REC_IDX]);
		ftrRecNum = int(footer);	
		recNumMatch = hdrRecNum == ftrRecNum
		if not recNumMatch:
			raise Exception("Header and footer record count mismatch")
	except Exception as e:
		raise Exception("Error validating header / footer  value  : {0} ".format(str(e)))

def getRawInputHeader(inputdata):			
	header = inputdata[0]	
	headerToks = header.split(',')
	if len(headerToks) is MAX_HEADER_TOK_LEN:
		return headerToks
	else:					
		raise Exception('Invalid header {0}, header should be of two comma seperated values'.format(header.strip()))

def	getRawInputFooter(inputdata):	
	return inputdata[-1].strip()

def isHdrDateValid(recdate):
	try:
		dt = datetime.strptime(recdate, SYMBOL_DATE_FORMAT)	
		return type(dt) is datetime
	except Exception as e:
		raise Exception("Header date {0} is not valid, should be in format {1}. {2}".format(recdate, SYMBOL_DATE_FORMAT, str(e)))
	
def loadSymbolData(properties):		
	return loadRawData(PROP_SYMBOL_DIR,PROP_SYMBOL_FILE, properties)
	
def loadClientConfigData(properties):
	return loadRawData(PROP_CLIENTCON_DIR,PROP_CLIENTCON_FILE, properties)

def loadRawData(dirConfigKey, fileConfigKey, properties):		
	inputdir = properties[dirConfigKey].strip()
	inputfilefmt = properties[fileConfigKey]	
	inputfiletoks = inputfilefmt.split('.')	
	# generate string representation of todays date in pattern specified within input file format 
	dtToday  = date.today().strftime(inputfiletoks[1])	
	listDir = os.listdir(inputdir)	
	expnamepattern = '{0}.{1}'.format(inputfiletoks[0].strip(),dtToday[0:-4])
	expectedname = ''	
	for filename in listDir:
		try:			
			if filename.index(expnamepattern) is 0:
				expectedname = filename
		except Exception as e:
			pass	
	#replace date format pattern with value of todays date as generated from it
	#inputfiletoks[1] = dtToday
	#expectedname =  '.'.join(inputfiletoks)
	filepath  = os.path.join(inputdir.strip(), expectedname)	
	f=open(filepath.strip())
	return f.readlines()				
	
def log(message):
	if len(message) is not 0:
		logger.info(message)
	
def makeOutputFilePath(prefix, inputfilekey, properties):
	inputfilefmt = properties[inputfilekey]	
	inputfiletoks = inputfilefmt.split('.')	
	# generate string representation of todays date in pattern specified within input file format 
	dtToday  = datetime.today().strftime(inputfiletoks[1])			
	path = os.path.join(properties[PROP_IXEYE_OUT_DIR].strip(), '{0}.{1}.txt'.format(prefix, dtToday))	
	return path
	
def writeListToFile(data, filename):
	f=open(filename, 'w')        
        for item in ixEyeData:
          print>>f, item
		
def sendmail(content, properties):			
	log('Sending the following content to client :\n {0}'.format(content))
	recipient = properties[PROP_CLIENT_EMAIL].strip()	
	sender = properties[PROP_SENDER_EMAIL].strip()
	
	msg = MIMEText(content)
	msg['Subject'] = 'ixeye sanity check report for %s' %date.today().strftime('%d/%m/%y')
	msg['From'] = sender 
	msg['To'] = recipient
	
	s = smtplib.SMTP(properties[PROP_SMTP_HOST].strip())
	#s.login(properties[PROP_SMTP_USER].strip(), '')
	s.sendmail(sender, [recipient], msg.as_string())
	s.quit()
	
emailBuf = []
try:
	if len(os.sys.argv) > 1:
		properties = loadProperties(os.sys.argv[1])
	else:
		properties = loadProperties()	
except Exception as e:
	logger.error("Processing aborted, could not load properties / config file : {0}".format(e))	
	raise e #terminate as subsequent rountines depend on result of this operation 
	
#generate symbols file from input source 
try:
	symbolData =  loadSymbolData(properties)	
	ixEyeData = rawSymbolDataToIxEye(symbolData, emailBuf)	
	outputfile = makeOutputFilePath('symbols', PROP_SYMBOL_FILE, properties)
	#writeListToFile(ixEyeData, outputfile)
	emailBuf.append("Tradeable instruments data successfully loaded into symbols file {1}".format(len(ixEyeData), outputfile))
except Exception as e:	
	logger.error(e)
	emailBuf.append("Loading of tradeable instrument data to symbols file failed >> {0}".format(str(e)))
	
#client config data is input source of sessionconfig and clientlimits file
try:
	clientConfigData =  loadClientConfigData(properties)
except Exception as e:
	emailBuf.append("Further processsing aborted, client configuration data failed to load from file >> {0}".format(str(e)))
	logger.error(e)
	sendmail(''.join(emailBuf), properties)	
	raise e	#terminate as subsequent rountines depend on result of this operation 

#generate sessionconfig file from source clientconfig data 
try:
	ixEyeData = rawSessionConfigToIxEye(clientConfigData, emailBuf)
	outputfile = makeOutputFilePath('sessionconf', PROP_CLIENTCON_FILE, properties)
	writeListToFile(ixEyeData, outputfile)
	emailBuf.append("Client configuration data successfully loaded into sessionconf file {0}".format(outputfile))
except Exception as e:
	logger.error(e)
	emailBuf.append("Loading of client configuration data to sessionconfig file failed")

#generate clientlimits file from source clientconfig data 
try:	 	
	ixEyeData = rawClientLimitsToIxEye(clientConfigData, emailBuf)
	outputfile = makeOutputFilePath('clientlimits', PROP_CLIENTCON_FILE, properties)
	writeListToFile(ixEyeData, outputfile)
	emailBuf.append("Client configuration data successfully loaded into clientlimits file {0}".format(outputfile))
except Exception as e:
	logger.error(e)	
	emailBuf.append("Loading of client configuration data to clientlimits file failed")	

sendmail('\n\t'.join(emailBuf), properties)		