from array import *
from struct import *
from binascii import *
from socket import *
from random import *
from string import *
from utility import *

# Server connection setup to paris.cs.utexas.edu
serverName = '128.83.144.56'
serverPort = 35605
clientSocket = socket(AF_INET, SOCK_DGRAM)
clientSocket.settimeout(60);

# Turn IP address and port number to hex for packet construction
sutport = 24390
tempSocket = socket(AF_INET, SOCK_DGRAM)
tempSocket.connect((serverName, serverPort))
sutIP = tempSocket.getsockname()[0]
tempSocket.close()
print("Local IP Address: " + str(sutIP))
print("SUT Port Number: " + str(sutport))
sutIPHexContainer = split(sutIP, '.')

# Convert IP address to number then to hex
sutIPNum = int(sutIPHexContainer[0]) * 256**3 + int(sutIPHexContainer[1]) * 256**2 + int(sutIPHexContainer[2]) * 256 + int(sutIPHexContainer[3])
sutIPHex = '0x{0:08X}'.format(sutIPNum)
print(sutIPHex)
sutPortHex = '0x{0:04X}'.format(sutport)
print("Sending IP Address in hex: " + str(sutIPHex) + " and port in hex: " + str(sutPortHex))

# Construct Packet
bitArray = array('l')
first16Bits = 0x8164
bitArray.append(first16Bits)
second16Bits = 0x0107
bitArray.append(second16Bits)

# Add cookie to packet
clientCookie = 0x023F
bitArray.append(clientCookie)
bitArray.append(clientCookie)

# Add IP to packet
sutIPHex1 = '0x' + sutIPHex[2:6]
sutIPHex2 = '0x' + sutIPHex[6:len(sutIPHex)]
bitArray.append(int(sutIPHex1, 16))
bitArray.append(int(sutIPHex2, 16))

# Add checksum to packet
bitArray.append(0x0000)

# Add port to packet
bitArray.append(int(sutPortHex, 16))

# Pack fields together for checksum calculation
pkt = packPkt(bitArray)
checksum = calculate_checksum(pkt)
checksumHex = hex(checksum)
if len(str(checksumHex)) < 6:
	checksumHex = checksumHex[0:2] + '0' + checksumHex[2:len(checksumHex)]

# Get checksum into network order
byteSwap = checksumHex[2:len(checksumHex)]
byteSwap = byteSwap[2:len(byteSwap)] + byteSwap[0:2]
checksumHex = '0x' + byteSwap
bitArray[6] = (int(checksumHex, 16))

# Build whole packet
pkt = packPkt(bitArray)
print("Sending Message: " + str(hexlify(pkt)))

# Send packet and resend if timeout occurs
while 1:
	try:
		clientSocket.sendto(pkt, (serverName, int(serverPort)))
		print("Packet sent to server, waiting for test results")
		serverResult = clientSocket.recv(2048)
		break
	except timeout:
		print("Timeout, Resending Packet")

# Check contents of packet
unpackedHex = hexlify(serverResult)
print("Message Received: " + str(unpackedHex))
checkResult = check_message_type_ex1(unpackedHex)
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
        print("Server reports successful SUT interaction")
    else:
    	errorCode = int(unpackedHex[28:32], 16) & 0x7FFF
        print("Server reports error in SUT interaction: " + str(errorCode))
