from array import *
from struct import *
from binascii import *
from socket import *
from random import *
from utility import *

# Server connection setup to paris.cs.utexas.edu
serverName = '128.83.144.56'
serverPort = 35605
clientSocket = socket(AF_INET, SOCK_DGRAM)
try:
	clientSocket.connect((serverName,serverPort))
except Exception as err:
	print("EXCEPTION: " + str(err))
	raise SystemExit

# Build message packet
bitArray = array('l')
first16Bits = 0x0164
bitArray.append(first16Bits)
second16Bits = 0x0107
bitArray.append(second16Bits)
clientCookie = 0x023F
bitArray.append(clientCookie)
bitArray.append(clientCookie)

# Prompt user for social security number and turn into hex
userInput = raw_input("Enter a Social Security Number: ")
print("Entered: " + str(userInput))
userInputHex = '%x' % int(userInput)
print("Length of userInput: " + str(len(str(userInputHex))))
if len(str(userInputHex)) < 8:
	userInputHex = '0%x' % int(userInput)
print(userInputHex)
userInputHex1 = '0x' + userInputHex[0:4]
print(userInputHex1)
userInputHex2 = '0x' + userInputHex[4:len(userInputHex)]
print(userInputHex2)
bitArray.append(int(userInputHex1, 16))
bitArray.append(int(userInputHex2, 16))

# Pack fields together for checksum calculation
pkt = packPkt(bitArray)

# Calculate checksum and turn into hex and byteswap for network (big endian) order
checksum = calculate_checksum(pkt)
print(checksum)
checksumHex = hex(checksum)
print(checksumHex)
print("Length of checksum: " + str(len(str(checksumHex))))
if len(str(checksumHex)) < 6:
	checksumHex = checksumHex[0:2] + '0' + checksumHex[2:len(checksumHex)]
print(checksumHex)
byteSwap = checksumHex[2:len(checksumHex)]
print(byteSwap)
byteSwap = byteSwap[2:len(byteSwap)] + byteSwap[0:2]
checksumHex = '0x' + byteSwap
print(byteSwap)
print(checksumHex)
bitArray.append(int(checksumHex, 16))

# Add blank results to end
bitArray.append(0x0000)

# Build packet to send
pkt = packPkt(bitArray)

clientSocket.send(pkt)
serverResult = clientSocket.recv(1024)
print("Received: " + serverResult)

# Check results
unpackedHex = hexlify(serverResult)
print(unpackedHex)
if int(unpackedHex[0:1]) & 0x8 == 0:
    print("Message Type Correct: 0")
else:
    print("Message Type Incorrect: 1")
if int(unpackedHex[0:1]) & 0x4 == 0:
    print("Response or Request Bit Incorrect: 0")
else:
    print("Response or Request Bit Correct: 1")
classNumber = int(unpackedHex[1:4])
if classNumber == 164:
    print("Class Number Correct: 356")
else:
    print("Class Number is not 356")
labNumber = int(unpackedHex[4:6])
if labNumber == 01:
    print("Lab Number Correct: " + str(labNumber))
else:
    print("Lab Number Incorrect: " + str(labNumber))
versionNumber = int(unpackedHex[6:8])
if versionNumber == 07:
    print("Version Number Correct: " + str(versionNumber))
else:
    print("Version Number Incorrect: " + str(versionNumber))
cookieReceivedPartA = unpackedHex[8:12]
cookieReceivedPartB = unpackedHex[12:16]
cookieSent = '023f'
if cookieReceivedPartA == cookieSent and cookieReceivedPartB == cookieSent:
    print("Cookie Correct: " + str(cookieReceivedPartA) + str(cookieReceivedPartB))
else:
    print("Cookies do not match, received: " + str(cookieReceivedPartA) + str(cookieReceivedPartB))
ssnReceivedPartA = unpackedHex[16:20]
ssnReceivedPartB = unpackedHex[20:24]
ssnSentPartA = userInputHex[0:4]
ssnSentPartB = userInputHex[4:len(userInputHex)]
if ssnReceivedPartA == ssnSentPartA and ssnReceivedPartB == ssnSentPartB:
    print("SSN matches: " + str(ssnReceivedPartA) + str(ssnReceivedPartB))
else:
    print("SSN does not match: " + str(ssnReceivedPartA) + str(ssnReceivedPartB))
verifiedChecksum = verify_checksum(unpackedHex)
print(str(verifiedChecksum))
verifyChecksumHex = '%x' % int(verifiedChecksum)
print(verifyChecksumHex)
if verifyChecksumHex == 'ffff':
    print("Checksum Correct!")
    print("P.O. Box Number is " + str(int(unpackedHex[28:32], 16)))
else:
    print("Checksum Incorrect!")

# Close socket
clientSocket.close()


# Notes: Need to add checks of result, clean up code
