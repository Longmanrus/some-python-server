import socket
import sys
import threading 

def recieving():
	while True:
		data = s.recv(1500).decode()
		if data == b'':
			e1.set()
			print ('recieve dead')
			return
		print (data)

def sending():
	while True:

		e1.wait(0)
		if e1.is_set(): 
			print ('send dead')
			return
		i = bytes(input(), 'UTF-8')
		s.send(i)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 6)
s.bind(('192.168.64.80', 0))
h = "192.168.64.80"
p = 8007
s.connect((h, p))

e1 = threading.Event()

t1 = threading.Thread(target=recieving, args=())
t2 = threading.Thread(target=sending, args=())	

t1.start()
t2.start()

t1.join()
t2.join()