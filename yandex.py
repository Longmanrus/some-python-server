import socks
import socket
from urllib import request
from time import sleep
import sqlite3
import datetime


socks.set_default_proxy(socks.SOCKS5,"192.168.64.167",8888)
socket.socket = socks.socksocket
oldrate=0

con = sqlite3.connect('db.sqlite3')
cur = con.cursor()
cur.execute("create table if not exists rate ('date' timestamp, 'rate' float,'source' char(256))")
con.commit()
cur.close()

while True:
 try:
  a=request.urlopen("https://yandex.ru")
  b=a.read().decode("utf-8")
  c=b.find("inline-stocks__value_inner")
  rate=b[c+28:c+33].replace(",",".") #string
  con = sqlite3.connect('db.sqlite3')
  cur = con.cursor()
  cur.execute("select * from rate where source!='manual' order by date desc")
  y=cur.fetchone()
  print(str(y))
  cur.close()
  if y==None or (y[1]!=float(rate)):
   oldrate=rate
   con = sqlite3.connect('db.sqlite3')
   cur = con.cursor()
   cur.execute("INSERT INTO rate ('date', 'rate','source') VALUES(?, ?, ?)",(datetime.datetime.now(), float(rate),"https://yandex.ru/"))
   con.commit()
   con.close()
 except:
  print("fail")
 sleep(1800)