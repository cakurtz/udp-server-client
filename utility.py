from array import *
from struct import *

# Calculates the checksum by adding up everything in pkt
# and manipulating the bits to get into 16 bits
def calculate_checksum(pkt):
	if len(pkt) % 2 == 1:
		pkt = pkt + "\0"
	checksum = sum(array("H", pkt))
	checksum = (checksum >> 16) + (checksum & 0xffff)
	checksum += checksum >> 16
	checksum = ~checksum
	checksum = checksum & 0xffff
	return checksum

# Packs the array into pkt for a sendable form
def packPkt(bitArray):
	pkt = ''
	for i in range(0,len(bitArray)):
		pkt = pkt + pack('!H',bitArray[i])
	return pkt

# Checks the received checksum for correctness
# Result should be all 1's or 0xFFFF
def verify_checksum(pktHex):
    bitArray = array('l')
    bitArray.append(int(pktHex[0:4], 16)) #Type/ClassNum
    bitArray.append(int(pktHex[4:8], 16)) #Lab/VersionNum
    bitArray.append(int(pktHex[8:12], 16)) #Cookie1
    bitArray.append(int(pktHex[12:16], 16)) #Cookie2
    bitArray.append(int(pktHex[16:20], 16)) #SSN1
    bitArray.append(int(pktHex[20:24], 16)) #SSN2
    bitArray.append(int(pktHex[24:28], 16)) #Checksum
    bitArray.append(int(pktHex[28:32], 16)) #Result
    
    checksum = sum(array("H", bitArray))
    checksum = (checksum >> 16) + (checksum & 0xffff)

    return checksum



## Check Packet Contents Helper Methods ##

# Checks the message type of received packet for type 0
def check_message_type_ex0(unpackedHex):
	correct = 1
	if int(unpackedHex[0:1]) & 0x8 <> 0:
		print("Message Type Incorrect: 1")
		correct = 0
	return correct

# Checks the message type of received packet for type 1
def check_message_type_ex1(unpackedHex):
	correct = 1
	if int(unpackedHex[0:1]) & 0x8 == 0:
		print("Message Type Incorrect: 0")
		correct = 0
	return correct

# Checks the response/request bit of received packet for response
def check_response_request_bit_ex0(unpackedHex):
	correct = 1
	if int(unpackedHex[0:1]) & 0x4 == 0:
	    print("Response or Request Bit Incorrect: 0")
	    correct = 0
	return correct

# Checks the response/request bit of received packet for resquest
def check_response_request_bit_ex1(unpackedHex):
	correct = 1
	if int(unpackedHex[0:1]) & 0x4 <> 0:
	    print("Response or Request Bit Incorrect: 1")
            correct = 0
	return correct

# Checks the class number bytes of received packet for value 356
def check_class_number(unpackedHex):
	correct = 1
	classNumber = int(unpackedHex[1:4])
	if classNumber <> 164:
	    print("Class Number is not 356")
	    correct = 0
	return correct

# Checks the lab number bytes of received packet for value 1
def check_lab_number(unpackedHex):
	correct = 1
	labNumber = int(unpackedHex[4:6])
	if labNumber <> 01:
	    print("Lab Number Incorrect: " + str(labNumber))
	    correct = 0
	return correct

# Checks the version number of received packet for value 7
def check_version_number(unpackedHex):
	correct = 1
	versionNumber = int(unpackedHex[6:8])
	if versionNumber <> 07:
	    print("Version Number Incorrect: " + str(versionNumber))
	    correct = 0
	return correct

# Checks the cookie of received packet against original cookie value sent
def check_cookie(unpackedHex, cookieSent):
	correct = 1
	cookieReceivedPartA = unpackedHex[8:12]
	cookieReceivedPartB = unpackedHex[12:16]
	if cookieReceivedPartA <> cookieSent or cookieReceivedPartB <> cookieSent:
	    print("Cookies do not match, received: " + str(cookieReceivedPartA) + str(cookieReceivedPartB))
	    correct = 0
	return correct

# Checks the SSN of received packet against original SSN value sent
def check_ssn(unpackedHex, ssnSentPartA, ssnSentPartB):
	correct = 1
	ssnReceivedPartA = unpackedHex[16:20]
	ssnReceivedPartB = unpackedHex[20:24]
	if ssnReceivedPartA <> ssnSentPartA or ssnReceivedPartB <> ssnSentPartB:
	    print("SSN does not match: " + str(ssnReceivedPartA) + str(ssnReceivedPartB))
	    correct = 0
	return correct

# Checks the checksum of received packet for equivalence to 0xFFFF
def check_checksum(unpackedHex):
	correct = 1
	verifiedChecksum = verify_checksum(unpackedHex)
	verifyChecksumHex = '%x' % int(verifiedChecksum)
	if verifyChecksumHex <> 'ffff':
	    print("Checksum Incorrect!")
	    correct = 0
	return correct

# Checks the success bit for a value of 0 or 1
# If 0, server returned success, print out P.O. Box Number returned
# If 1, server found an error
def check_success_bit(unpackedHex):
	correct = 1
	verifySuccessBit = int(unpackedHex[28:29], 16) & 0x8
	if verifySuccessBit <> 0:
		print("Server set error code")
		correct = 0
	return correct
