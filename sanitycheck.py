import os
import io

symbolHeaderMap={1 : ('TICKER SYMBOL', str), 2 : ('SHORT SELL RESTRICTED', bool), 3 :  ('MIN TICK SIZE', float), 4 : ('MAX PRICE DEVIATION', int), 5 : ('PREVIOUS CLOSE PRICE', float) , 6 : ('ACTIVE', bool)}


def fetchRawInputData():
	pass

def parseRawInput(value):
	print value;
	
def getRawInputHeader(inputdata):
	linelen=len(lines)
	header=lines[0]
	print 'Header info : {0}'.format(header)
	headerToks = header.split(',')
	return headerToks

if len(os.sys.argv) < 2:
	raise Exception('Usage {0} inputfilename'.format(os.sys.argv[0]))

f=open(os.sys.argv[1])


if not f:
	raise Exception('No such file {0}'.format(os.sys.argv[1]))  
	
lines = f.readlines()
linelen=len(lines)

header=lines[0]

#print 'Header info : {0}'.format(header)

#headerToks = header.split(',')
#if len(headerToks) is 2:
	headerRecNum = headerToks[1]
	headerDate = headerToks[0]
	
footerRecNum = lines[-1]

print headerRecNum
print headerDate
print symbolHeaderMap[1][0]
#for line in lines:
#	print line
	
	