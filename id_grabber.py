from urllib import request, parse 
import re
import socks, socket


socks.set_default_proxy(socks.SOCKS5,"192.168.64.167",8888)
socket.socket = socks.socksocket

a=request.urlopen("http://steamcommunity.com/market/search?q=&category_730_ItemSet%5B%5D=any&category_730_ProPlayer%5B%5D=any&category_730_StickerCapsule%5B%5D=any&category_730_TournamentTeam%5B%5D=any&category_730_Weapon%5B%5D=any&appid=730#p1_name_asc")
b=a.read().decode("utf-8")

for it in re.finditer("market_listing_row_link",b):

	start=len("market_listing_row_link\" href=\"")+it.start()
	end=b[start:].find("\"")
	q=b[start:start+end]
	z=request.urlopen(b[start:start+end])
	y=z.read().decode("utf-8")
	zstart=y.find("Market_LoadOrderSpread")+len("Market_LoadOrderSpread( ")
	zend=y[zstart:].find(" )")
	i=y[zstart:zstart+zend]
	n=parse.unquote(q[46:])
	print(i)
	f=open('items_id.txt', 'ab')
	st=bytes(n+' : '+i+'\r\n', 'utf-8')
	f.write(st)
	f.close()
