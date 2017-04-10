import os
import socket
import math
import random
import time

hostname = 'localhost'
port = 50000

si = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
si.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

tcp_sock = socket.socket()
tcp_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
tcp_sock.bind((hostname, port))
tcp_sock.listen(5)

print 'Server listening'

conn, addr = tcp_sock.accept()

data = conn.recv(1024)

value = data.split()

filename = value[0]
w = int(value[1])
t = float(value[2])
n = int(value[3])

path = str(os.getcwd())
filesize = os.path.getsize(filename)
filename = path+'/'+filename

paclen = int(math.ceil(filesize/float(n)))
conn.send(str(paclen))

f = open(filename, 'rb')
#l = f.read(paclen)
i = 0
base = 0

while base<n:
	flag = 0 #to get and not get acknowledgement
	flag2 = 0
	t2 = time.time()
	lost_pkt = 0
	print_base = base

	print 'Restarting window with base ', base

	i = base;

	for num in range(0,w):
		l = f.read(paclen)
		if l=='':
			print 'EOF'
		i = i+1
		print 'Printing i ', i
		r = random.randrange(0,4)
		#r = i%5
		if r!=0:
			conn.send(str(i))
			si.sendto(l, (hostname,port))
			print 'Sending ', l
			ack = conn.recv(1024)
			print 'Received acknowledgement ', ack
			if ack=='####$$$$####':
				print 'nack received: out of order'
				flag = 1
			if flag==0:
				t1 = time.time()
				if t1-t2 > t and flag2 == 1:
					print 'timeout'
					break
				elif ack!='' and int(ack)==lost_pkt:
					t2 = t1

				base = base+1
			print 'base ', base
		elif r == 0:
			flag2 = 1
			t2 = time.time()
			lost_pkt = i
			print 'Not sending packet at all'
		#print r
		#l = f.read(paclen)
		#if l=='':
		#	print 'EOF'
			#si.sendto(l, (hostname,port))

                if base==n:
                    break

	print 'Base = ', base

	f.seek((base)*paclen)
	c = f.read(15)
	print 'char ',c
	f.seek((base)*paclen)

	if base == n:
		print 'We have finished sending all the packets'
		break

f.close()