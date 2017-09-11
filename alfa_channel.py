
import os, sys

# showing stat information of file "a2.py"
statinfo = os.stat('3000dollars.bmp')

print (statinfo.st_size)
f=open('3000dollars.bmp','rb')
g=open('3200dollars.bmp','wb')
g.write(f.read(0x36))
for i in range (int((statinfo.st_size-0x36)/4)):
	g.write(f.read(3))
	g.write(b'\x80')
	f.read(1)