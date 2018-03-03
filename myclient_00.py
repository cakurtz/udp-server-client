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
clientSocket.settimeout(5);

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
print("SSN sending to server: " + str(userInput))
userInputHex = '%x' % int(userInput)
if len(str(userInputHex)) < 8:
	userInputHex = '0%x' % int(userInput)
userInputHex1 = '0x' + userInputHex[0:4]
userInputHex2 = '0x' + userInputHex[4:len(userInputHex)]
bitArray.append(int(userInputHex1, 16))
bitArray.append(int(userInputHex2, 16))

# Pack fields together for checksum calculation
pkt = packPkt(bitArray)

# Calculate checksum and turn into hex and byteswap for network (big endian) order
checksum = calculate_checksum(pkt)
checksumHex = hex(checksum)
if len(str(checksumHex)) < 6:
	checksumHex = checksumHex[0:2] + '0' + checksumHex[2:len(checksumHex)]

# Swap bytes of checksum to get into network (big endian) order
byteSwap = checksumHex[2:len(checksumHex)]
byteSwap = byteSwap[2:len(byteSwap)] + byteSwap[0:2]
checksumHex = '0x' + byteSwap
bitArray.append(int(checksumHex, 16))

# Add blank results to end
bitArray.append(0x0000)

# Build packet to send
pkt = packPkt(bitArray)
print("Sending Message: " + str(hexlify(pkt)))

# Send packet and resend if timeout occurs
while 1:
	try:
		clientSocket.sendto(pkt, (serverName, int(serverPort)))
		serverResult = clientSocket.recv(2048)
		break
	except timeout:
		print("Timeout, Resending Packet")

# Check results
unpackedHex = hexlify(serverResult)
print("Message Received: " + str(unpackedHex))
checkResult = check_message_type_ex0(unpackedHex)
checkResult = check_response_request_bit_ex0(unpackedHex)
checkResult = check_class_number(unpackedHex)
checkResult = check_lab_number(unpackedHex)
checkResult = check_version_number(unpackedHex)
checkResult = check_cookie(unpackedHex, '023f')
ssnSentPartA = userInputHex[0:4]
ssnSentPartB = userInputHex[4:len(userInputHex)]
checkResult = check_ssn(unpackedHex, ssnSentPartA, ssnSentPartB)
checkResult = check_checksum(unpackedHex)
if checkResult == 1:
    checkResult = check_success_bit(unpackedHex)
    if checkResult == 1:
        poBoxNumber = int(unpackedHex[28:32], 16) & 0x7FFF
        print("P.O. Box Number is " + str(poBoxNumber))
    else:
        print("Server returned error")

# Close socket
clientSocket.close()
