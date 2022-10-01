import socket               # Import socket module
import random   # for random number generating
import time  # for sleep
socket.setdefaulttimeout(120)


#STUDENT has to connect to the ROBOT TCP Port 3310 and send your BlazerID via the connection established.

s = socket.socket()         # Create a socket object
local_host = socket.gethostname() # Get local machine name
port = 3310                # Reserve a port for your service.
BlazerID='4445'.encode()
s.connect((local_host, port))
s.send(BlazerID)
new_port = s.recv(100)  # receive 100 character from sive 
new_port = int(new_port.decode())
s.close()


print("")

#to create a TCP socket s_2 at port ddddd to accept a new connection. The ROBOT will initiate the new connection 1 second later after sending ddddd. Upon accepting the
#connection, a new socket s2 will be returned.

# Create a TCP socket to listen connection
print("Creating TCP socket...")
s_2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s_2.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s_2.bind((local_host, new_port))
s_2.listen(5)
print("\nTCP socket created, ready for listening and accepting connection...")
print("Waiting for connection on port", new_port)

ser1, address = s_2.accept()
ser1_address = address[0]
print("\nClient from %s at port %d connected" %(ser1_address,address[1]))

#STUDENT needs to decode the message and create a UDP socket s3 to send a
 
data_12_char = ser1.recv(100)
spilt_data = data_12_char.decode().split(",")
new_port = int(spilt_data[0]) 
print("12 chararacter data received: " + str(data_12_char.decode()))
s_2.close()
# send variable num ( 5 < num < 10) to ROBOT on port fffff.
byte_to_send = str.encode(str(random.randint(5,10))) # random number between 5 and 10 to send to server 
time.sleep(1)

UDPclinetSocket = socket.socket(family = socket.AF_INET, type = socket.SOCK_DGRAM) 
time.sleep(1)
# sending random number to server
UDPclinetSocket.sendto(byte_to_send, (local_host,new_port))
bufferSize = 90
#STUDENT only needs to receive any one of them.
addr = (local_host, int(spilt_data[1]))
s_3 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s_3.bind(addr)

#STUDENT only needs to receive any one of them.
ser_mesg = s_3.recvfrom(bufferSize) 
print("UDP packet received", ser_mesg[0])
time.sleep(1)


#When the STUDENT received the char string xxx, it will send back the string to the
# ROBOT at UDP port fffff. Similar to the ROBOT, the string will be sent 5 times, once
# every 1 second. The ROBOT will check if the two strings are the same.
for i in range(0,5):
    s_3.sendto(ser_mesg[0],(local_host,new_port))
    time.sleep(1)
    print("UDP packet %d sent" %(i+1))
