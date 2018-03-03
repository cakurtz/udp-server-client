from array import *
from struct import *
from binascii import *
from socket import *
from random import *
from utility import *

# Setup database as list
db = []
with open('db.txt') as dbfile:
	for ln in dbfile:
		db.append(ln.strip().split())

# Create socket for server to connect to
psock = socket(AF_INET, SOCK_DGRAM) # server connects to this port

# Creating connection to gather IP address to send server, then close
serverName = '128.83.144.56'
serverPort = 35605
clientSocket = socket(AF_INET, SOCK_DGRAM)
try:
	clientSocket.connect((serverName,serverPort))
except Exception as err:
	print("EXCEPTION: " + str(err))
	raise SystemExit

# Bind psock to valid IP and port for SUT
sockName = clientSocket.getsockname()
clientSocket.close()
sockName = (sockName[0], 24390)
print("SUT Address: " + str(sockName))
psock.bind(sockName)

# Wait for response from cs356 server
print("Wait for Response")
while 1:
	serverResult = psock.recvfrom(2048)
	print("Receive Success")
	unpackedHex = hexlify(serverResult[0])
	print("Message in hex: " + str(unpackedHex))

	# Check for errors in packet
	error = 0
	if check_message_type_ex0(unpackedHex) == 0:
		error = 2
	if check_response_request_bit_ex1(unpackedHex) == 0:
		error = 2
	if check_class_number(unpackedHex) == 0:
		error = 2
	if check_lab_number(unpackedHex) == 0:
		error = 2
	if check_version_number(unpackedHex) == 0:
		error = 2
	if check_checksum(unpackedHex) == 0:
		error = 1

	# Check SSN and get P.O. Box Number if valid
	ssnHex = unpackedHex[16:24]
	ssnNum = int(ssnHex, 16)
	print("Social Security Number Received: " + str(ssnNum))
    poBoxNum = 0
    for social in db:
        if int(social[0]) == int(ssnNum):
            poBoxNum = social[1]
    print("P.O. Box Number Sending to cs356 Server: " + str(poBoxNum))
    if poBoxNum == 0:
        error = 4

    # Construct Response Packet
    bitArray = array('l')
    first16Bits = 0xC164
    bitArray.append(first16Bits)
    second16Bits = 0x0107
    bitArray.append(second16Bits)
    cookiePartA = unpackedHex[8:12]
    cookiePartB = unpackedHex[12:16]
    bitArray.append(int(cookiePartA, 16))
    bitArray.append(int(cookiePartB, 16))
    ssnPartA = unpackedHex[16:20]
    ssnPartB = unpackedHex[20:24]
    bitArray.append(int(ssnPartA, 16))
    bitArray.append(int(ssnPartB, 16))
    bitArray.append(0x0000)
    if error == 0:
        last16Bits = "0x0%0.3X" % int(poBoxNum)
    else:
        last16Bits = "0x8%0.3X" % error
    bitArray.append(int(last16Bits, 16))

    # Caclulate checksum and place into bit array
    pkt = packPkt(bitArray)
    calculatedChecksum = calculate_checksum(pkt)
    calcHex = hex(calculatedChecksum)
    byteSwap = calcHex[2:len(calcHex)]
    byteSwap = byteSwap[2:len(calcHex)] + byteSwap[0:2]
    calcHex = '0x' + byteSwap
    bitArray[6] = int(calcHex, 16)

    # Build final packet and send
    pkt = packPkt(bitArray)
    psock.sendto(pkt, serverResult[1])
