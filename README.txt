Name: Coty Kurtz
UT EID: cak2493

----------
Exercise 0
----------

Comments: My program tests each field in the received packet and outputs a message for any incorrect field in the packet. Below are 4 tests of output from my program. 2 are valid SSN's and 1 is invalid. The last test is an interaction with the lossy server on port 35607 with the timout value set to 5 seconds.

Output Test 1 (Success):
Enter a Social Security Number: 111111111
SSN sending to server: 111111111
Sending Message: 01640107023f023f069f6bc786b00000
Message Received: 41640107023f023f069f6bc741de04d2
P.O. Box Number is 1234

Output Test 2 (Error Received for Invalid SSN):
SSN sending to server: 123456789
Sending Message: 01640107023f023f075bcd1524a60000
Received Message: Ad??[?d??
Message received in hex: 41640107023f023f075bcd1564a18004
Server set error code
Server returned error

Output Test 3 (Success):
Enter a Social Security Number: 954772946
SSN sending to server: 954772946
Sending Message: 01640107023f023f38e8add2125c0000
Message Received: 41640107023f023f38e8add2c8390a22
P.O. Box Number is 2594

Output Test 4 (Lossy Server):
Enter a Social Security Number: 111111111
SSN sending to server: 111111111
Sending Message: 01640107023f023f069f6bc786b00000
Timeout, Resending Packet
Message Received: 41640107023f023f069f6bc741de04d2
P.O. Box Number is 1234

----------
Exercise 1
----------

Comments: Verification behavior is the same as Exercise 0. I set the timeout value to 60 seconds to ensure completion of interaction. Below is an interaction between my client, the cs356 server, and my sut server.