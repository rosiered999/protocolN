import os
import socket
import math
import time

w = int(raw_input('enter window size: '))
t = float(raw_input('enter timeout time: '))
n = int(raw_input('enter number of packets: '))

packet_loss_prob = 0.5

filename = str(raw_input('filename: ').strip())


hostname = 'localhost'
port = 50000

tcp_sock = socket.socket()
tcp_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
tcp_sock.connect((hostname, port))

siceket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
siceket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
siceket.bind((hostname,port))

send_string = str(filename) + " " + str(w) + " " + str(t) + " " + str(n)
print send_string
tcp_sock.send(send_string)

pacsize = tcp_sock.recv(1024)
pacsize = int(pacsize)
print pacsize

tcp_sock.settimeout(t)

filename = 'server' + filename

f = open(filename,'w+')

base = 0
recv_seq = tcp_sock.recv(1024)
print 'Received seq = ', recv_seq
data_arr = ['a' for i in range(0,n)]
expected_seq = 1

while recv_seq != '':

	# expected_seq = 1
	# loop_var = base
	# print 'Restarting window with base ', base
	# for num in range(1,w+1):
	data_flag = 0
	data = siceket.recvfrom(pacsize)
	print 'Expecting ', expected_seq
	if int(recv_seq) == expected_seq:
		print 'And received ', recv_seq
		expected_seq = expected_seq + 1
		tcp_sock.send(recv_seq)
		base = base+1
		data_flag = 1
		f.write(data[0])
	else:
		print 'But received ', recv_seq
		num = recv_seq
		tcp_sock.send('####$$$$####')


	if data[0]!='':
		print 'The data we received is', data
	else:
		print 'client EOF'

	recv_seq = tcp_sock.recv(1024)
	print 'Received seq = ', recv_seq

	if base == n:
		print 'We have finished receiving all packets'
		break