#!/usr/bin/python

import httplib
import re
import sys
import string

def help():
	print "[mgoogle v1.0] - by neuro [0x0lab.org]"
	print "\nUsage: python mgoogle.py <domain_name> \n"
	sys.exit()

if len(sys.argv) < 1 or len(sys.argv) > 2:
	help()
elif len(sys.argv) == 2:
	domain_name =  sys.argv[1]
else:
	help()

googleres=[]
googleres1=[]

page_counter = 0
i=0

while page_counter < 1000:
	rg = httplib.HTTP('www.google.com')
	rg.putrequest('GET', "/search?num=100&start=" + str(page_counter) + "&hl=en&btnG=B%C3%BASearch+en+Google&meta=&q=%40" + domain_name)
	rg.putheader('Host', 'www.google.com')
	rg.putheader('User-agent', 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.5; en-US; rv:1.9.0.4) Gecko/2008102920 Firefox/3.0.4')
	rg.endheaders()
	errcode, errmsg, headers = rg.getreply()

	if errcode!=200:
		print 'Error Sending Request', errcode, errmsg
		break
	else:
		rgdata = rg.getfile().read()

	rgdata = re.sub('&lt;','',rgdata)
	rgdata = re.sub('&gt;','',rgdata)
	rgdata = re.sub(' at ','@',rgdata)
	rgdata = re.sub('<b>', '', rgdata)
	rgdata = re.sub('<em>', '', rgdata)
	rgdata = re.sub('</em>', '', rgdata)
	rgdata = re.sub('<b>', '', rgdata)
	rgdata = re.sub('</b>', '', rgdata)
		
	pattern='[\w\.\-]+@'+domain_name
	rgr = re.compile(pattern, re.I)
	rgresults = rgr.findall(rgdata)
		
	if page_counter > int(1000):
		break
	if page_counter > 1000:
		break
	else:
		page_counter = page_counter + 100
		
	for gemail in rgresults:
		if googleres.count(gemail) == 0:
			googleres.append(gemail)
			print "[*]-" + str(gemail)
			i=i+1

			l=httplib.HTTP('www.google.com')
			l.putrequest('GET', "/search?num=100&start=100&hl=en&btnG=B%C3%BASearch+en+Google&meta=&q=%22"+str(gemail)+"%22")
			l.putheader('Host', 'www.google.com')
			l.putheader('User-agent', 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.5; en-US; rv:1.9.0.4) Gecko/2008102920 Firefox/3.0.4')
			l.endheaders()
			errcode, errmsg, headers = l.getreply()
								
			if errcode!=200:
				print 'Error Sending Request', errcode, errmsg
			else:
				lgdata = l.getfile().read()
			
			ml = re.compile('"r"><a href="'+'(.*?)"'+' ')
			ml1 = re.compile(">[a-zA-Z0-9+_\-.:()| ]*</a></h3>")
														
			mlgresults = ml.findall(lgdata)
			mlgresults1 = ml1.findall(lgdata)
				
			mlgresults1 = re.sub('>','',str(mlgresults1))
			mlgresults1 = re.sub('</a','',str(mlgresults1))
			mlgresults1 = re.sub('</h3','',str(mlgresults1))
													
			print "[*][*]-Related Information about e-mail", gemail
			print "    |-", mlgresults1.encode('utf-8')
								
			print "[*][*]-Links about e-mail", gemail
			for el1 in mlgresults:
				if googleres1.count(el1) == 0:
					googleres1.append(el1)
					link=re.sub('"','',el1)
					print "    |-", str(link).encode('utf-8')
print "\n[*]-Total e-mails found:", i



