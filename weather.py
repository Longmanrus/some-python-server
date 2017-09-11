import socks
import socket
from urllib import request, parse
from time import sleep
import sqlite3
import datetime


socks.set_default_proxy(socks.SOCKS5,"192.168.64.167",8888)
socket.socket = socks.socksocket
oldrate=0

con = sqlite3.connect('db.sqlite3')
cur = con.cursor()
cur.execute("create table if not exists weather ('date' timestamp, 'day' int,'night' int, 'rain' char(256))")
cur.execute("create table if not exists weather2 ('date' timestamp, 'day' int,'night' int, 'rain' char(256))")
cur.execute("create table if not exists weather3 ('date' timestamp, 'day' int,'night' int, 'rain' char(256))")
con.commit()
cur.close()

a=request.urlopen("https://yandex.ru/pogoda/togliatti")
b=a.read().decode("utf-8")
c=b.find("forecast-brief__item-comment")+len('forecast-brief__item-comment')
print(c)
d=b[c:].find("<")
rain1=parse.unquote(b[c+2:c+d])
c=b.find("Максимальная температура днём")+len('Максимальная температура днём')
print(c)
day1=parse.unquote(b[c+2:c+5]) 
c=b.find("Минимальная температура ночью")+len('Минимальная температура ночью')
print(c)
night1=parse.unquote(b[c+2:c+5]) 
b=b[d+c:]
print (d+c)
c=b.find("forecast-brief__item-comment")+len('forecast-brief__item-comment')
d=b[c:].find("<")
rain2=parse.unquote(b[c+2:c+d])
c=b.find("Максимальная температура днём")+len('Максимальная температура днём')
day2=parse.unquote(b[c+2:c+5]) 
c=b.find("Минимальная температура ночью")+len('Минимальная температура ночью')
night2=parse.unquote(b[c+2:c+5]) 
b=b[d+c:]
print (d+c)
c=b.find("forecast-brief__item-comment")+len('forecast-brief__item-comment')
d=b[c:].find("<")
rain3=parse.unquote(b[c+2:c+d])
c=b.find("Максимальная температура днём")+len('Максимальная температура днём')
day3=parse.unquote(b[c+2:c+5]) 
c=b.find("Минимальная температура ночью")+len('Минимальная температура ночью')
night3=parse.unquote(b[c+2:c+5]) 


con = sqlite3.connect('db.sqlite3')
cur = con.cursor()
cur.execute("INSERT INTO weather ('date', 'day', 'night', 'rain') VALUES(?, ?, ?, ?)",(datetime.datetime.now(), day1, night1, rain1))
cur.execute("INSERT INTO weather2 ('date', 'day', 'night', 'rain') VALUES(?, ?, ?, ?)",(datetime.datetime.now(), day2, night2, rain2))
cur.execute("INSERT INTO weather3 ('date', 'day', 'night', 'rain') VALUES(?, ?, ?, ?)",(datetime.datetime.now(), day3, night3, rain3))
con.commit()
con.close()



