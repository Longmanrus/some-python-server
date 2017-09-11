import socket
import sys
import threading 

def recieving():
	while True:
		data = conn.recv(1500).decode()
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
		conn.send(i)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 8007))
s.listen(2)
while True:
	conn, addr = s.accept()
	print (addr)
	e1 = threading.Event()



	t1 = threading.Thread(target=recieving, args=())
	t2 = threading.Thread(target=sending, args=())	

	t1.start()
	t2.start()