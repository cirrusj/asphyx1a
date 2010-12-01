#!/usr/bin/python

import httplib
import re
import sys
import string

def help():
	print "[vHosts v1.0] - by neuro [0x0lab.org]"
	print "\nUsage: python vHosts.py <IP> <Number of Page Results>\n"
	print "Example: python vHosts.py 127.0.0.1 10\n"
	sys.exit()

if len(sys.argv) < 2 or len(sys.argv) > 3:
	help()
elif len(sys.argv) == 3:
	IP =  sys.argv[1]
	no = sys.argv[2]
else:
	help()

vHostsRes=[]

print "[*]-vHosts on Bing Search Engine [Search pattern on Bing 'IP:IP Address']"

i=0

page_counter=1
while page_counter < no:
	vhb = httplib.HTTP('www.bing.com')
	vhb.putrequest('GET', "/search?q=ip%3A" +IP+ "&FORM=MSNH11&qs=n&first="+str(page_counter))
	vhb.putheader('Host', 'www.bing.com')
	vhb.putheader('Cookie', '_FP=mkt=en-US&ui=en-US;')
	vhb.putheader('User-agent', 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.5; en-US; rv:1.9.0.4) Gecko/2008102920 Firefox/3.0.4')
	vhb.endheaders()
	errcode, errmsg, headers = vhb.getreply()
	
	if errcode!=200:
		print 'Error Sending Request', errcode, errmsg
	else:
		vhrbdata = vhb.getfile().read()
		
	#reqular expresion for store results in a list
	vhbr = re.compile('class="sb_tlst"><h3><a href="'+'(.*?)'+'" onmousedown="return')
	vhrbresult = vhbr.findall(vhrbdata)
	
	if page_counter > int(no):
		break
	else:
		page_counter = page_counter + 10
		
	#iterate through list and print results
	for x in vhrbresult:
		x=x.split('/')
		uniqurl = '/'.join(x[:3]) + '/'
		if vHostsRes.count(uniqurl) == 0:
			vHostsRes.append(uniqurl)
			print " |--" + uniqurl
			i=i+1
print "[*]-Total vHosts found:", i
