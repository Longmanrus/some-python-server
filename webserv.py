from http.server import HTTPServer, BaseHTTPRequestHandler
import sqlite3, urllib, datetime

class dohust(BaseHTTPRequestHandler):
	def do_POST(self):
		d=1
		length = int(self.headers['content-length'])
		req = self.rfile.read(length)
		postvars = urllib.parse.parse_qs(req, keep_blank_values=1)
		c = postvars[b'new_rate'][0].decode('utf-8')
		passw=postvars[b'passw'][0].decode('utf-8')
		if passw=="change7":
			try:
				d = float(c)
			except:
				d = 0.0
			if d>0:
				con = sqlite3.connect('db.sqlite3')
				cur = con.cursor()
				cur.execute("INSERT INTO rate ('date', 'rate','source') VALUES(?, ?, ?)",(datetime.datetime.now(), d,"manual"))
				con.commit()
				con.close()
		dohust.Zapis(self,not d)

	def do_GET(self):
		print (self.path)
		dohust.Zapis(self)
	def Zapis(self,error=0):
		con = sqlite3.connect('db.sqlite3')
		cur = con.cursor()
		cur.execute("SELECT * FROM rate ORDER BY date desc")
		y = cur.fetchall()

		if self.path == "/robot":
			self.wfile.write(bytes(str(y[0][1]),'UTF-8'))
		elif self.path=="/game":
			f = open("x_0.1.html", "r")
			text = f.read()
			f.close()
			self.send_response(200, 'OK')
			self.send_header('Content-type', 'html')
			self.end_headers()
			self.wfile.write(bytes(text, 'UTF-8'))
		elif self.path=="/openid":
			f = open("openid_test.html", "r")
			text = f.read()
			f.close()
			self.send_response(200, 'OK')
			self.send_header('Content-type', 'html')
			self.end_headers()
			self.wfile.write(bytes(text, 'UTF-8'))

		elif self.path=="/input":
			f = open("input.html", "r")
			text = f.read()
			f.close()
			self.send_response(200, 'OK')
			self.send_header('Content-type', 'html')
			self.end_headers()
			self.wfile.write(bytes(text, 'UTF-8'))
			for q in y:
				self.wfile.write(bytes('<tr><td>'+str(q[0])[0:19]+'</td><td><b>'+str(q[1])+'</b></td><td>'+q[2]+'</td></tr>','UTF-8'))
			self.wfile.write(bytes('</table>','utf-8'))
			if error:
				self.wfile.write(bytes('OSHIBKA EPTA!','utf-8'))
			f = open("footer.html", "r")
			text = f.read()
			f.close()
			self.wfile.write(bytes(text,'UTF-8'))
		else:
			f = open("a.html", "r")
			text = f.read()
			f.close()
			self.send_response(200, 'OK')
			self.send_header('Content-type', 'html')
			self.end_headers()
			self.wfile.write(bytes(text, 'UTF-8'))
			for q in y:
				self.wfile.write(bytes('<tr><td>'+str(q[0])[0:19]+'</td><td><b>'+str(q[1])+'</b></td><td>'+q[2]+'</td></tr>','UTF-8'))
			self.wfile.write(bytes('</table>','utf-8'))
			if error:
				self.wfile.write(bytes('OSHIBKA EPTA!','utf-8'))

			f = open("middle.html", "r")
			text = f.read()
			f.close()
			self.wfile.write(bytes(text,'UTF-8'))
			cur.execute("SELECT * FROM exchange ORDER BY date desc")
			y = cur.fetchall()
			for q in y:
				print(q[3]=="http://thbank.ru/")
				if q[3]=="http://thbank.ru/":
					self.wfile.write(bytes('<tr><td class="thb">'+str(q[0])[0:19]+'</td><td class="thb"><b>'+str(q[1])+'</b></td><td class="thb"><b>'+str(q[2])+'</b></td><td class="thb">'+q[3]+'</td></tr>','UTF-8'))
				else:
					self.wfile.write(bytes('<tr><td>'+str(q[0])[0:19]+'</td><td><b>'+str(q[1])+'</b></td><td><b>'+str(q[2])+'</b></td><td>'+q[3]+'</td></tr>','UTF-8'))
			f = open("footer.html", "r")
			text = f.read()
			f.close()
			self.wfile.write(bytes(text,'UTF-8'))
			cur.execute("SELECT * from weather ORDER by date desc")
			y = cur.fetchone()
			self.wfile.write(bytes(str(y[0])+'<br>Температура днем:'+str(y[1])+'<br>Температура ночью:'+str(y[2])+'<br>Осадки:'+str(y[3])+'<br><br>','utf-8'))
			cur.execute("SELECT * from weather2 ORDER by date desc")
			y = cur.fetchone()
			self.wfile.write(bytes(str(y[0])+'<br>Температура днем:'+str(y[1])+'<br>Температура ночью:'+str(y[2])+'<br>Осадки:'+str(y[3])+'<br><br>','utf-8'))
			cur.execute("SELECT * from weather3 ORDER by date desc")
			y = cur.fetchone()
			self.wfile.write(bytes(str(y[0])+'<br>Температура днем:'+str(y[1])+'<br>Температура ночью:'+str(y[2])+'<br>Осадки:'+str(y[3])+'<br><br>','utf-8'))
			#for q in y:
			#	self.wfile.write(bytes(str(q[0])+'<br>Температура днем:'+str(q[1])+'<br>Температура ночью:'+str(q[2])+'<br>Осадки:'+str(q[3])+'<br>','utf-8'))
			f = open("x_0.1.html", "r")
			text = f.read()
			f.close()
			self.wfile.write(bytes(text,'UTF-8'))
		con.close()
con = sqlite3.connect('db.sqlite3')
cur = con.cursor()
cur.execute("create table if not exists rate ('date' timestamp,'rate' float,'source' char(256))")
con.commit()
con.close()

server_address = ("", 8000)
httpd = HTTPServer(server_address, dohust)
httpd.serve_forever()