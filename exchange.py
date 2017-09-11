#exchange rates
import socks
import socket
from urllib import request
from time import sleep
import sqlite3
import datetime


socks.set_default_proxy(socks.SOCKS5,"192.168.64.167",8888)
socket.socket = socks.socksocket

con = sqlite3.connect('db.sqlite3')
cur = con.cursor()
cur.execute("create table if not exists exchange ('date' timestamp, 'rate1' float,'rate2' float,'source' char(256))")
con.commit()
cur.close()

while True:
 try:
  a=request.urlopen("http://novikom.ru/ru/phisycal_persons/")
  b=a.read().decode("windows-1251")
  c=b.find("id=3>")
  rate1=b[c+5:c+10] #string
  c=b.find("id=4>")
  rate2=b[c+5:c+10] #string
  con = sqlite3.connect('db.sqlite3')
  cur = con.cursor()
  cur.execute("select * from exchange where source!='manual' order by date desc")
  y=cur.fetchone()
  print(y)
  cur.close()
  if y==None or (y[1]!=float(rate1)) or (y[2]!=float(rate2)):
   con = sqlite3.connect('db.sqlite3')
   cur = con.cursor()
   cur.execute("INSERT INTO exchange ('date', 'rate1','rate2','source') VALUES(?, ?, ?,?)",(datetime.datetime.now(), float(rate1),float(rate2),"http://novikom.ru/"))
   con.commit()
   con.close()
 except:
  print("fail")
 sleep(1800)
 try:
  a=request.urlopen("http://www.thbank.ru")
  b=a.read().decode("windows-1251")
  c=b.find("USD")
  rate1=b[c+12:c+17] #string
  rate2=b[c+26:c+31] #string
  con = sqlite3.connect('db.sqlite3')
  cur = con.cursor()
  cur.execute("select * from exchange where source='http://thbank.ru/' order by date desc")
  y=cur.fetchone()
  print(y)
  cur.close()
  if y==None or (y[1]!=float(rate1)) or (y[2]!=float(rate2)):
   con = sqlite3.connect('db.sqlite3')
   cur = con.cursor()
   cur.execute("INSERT INTO exchange ('date', 'rate1','rate2','source') VALUES(?, ?, ?,?)",(datetime.datetime.now(), float(rate1),float(rate2),"http://thbank.ru/"))
   con.commit()
   con.close()
 except:
  print("fail")
 sleep(1800)