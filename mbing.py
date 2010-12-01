#!/usr/bin/python

import httplib
import re
import sys
import string

def help():
	print "[mbing v1.0] - by neuro [0x0lab.org]"
	print "\nUsage: python mbing.py <domain_name> \n"
	sys.exit()

if len(sys.argv) < 1 or len(sys.argv) > 2:
	help()
elif len(sys.argv) == 2:
	domain_name =  sys.argv[1]
else:
	help()

result=[]
page_counter = 1

i=0
while page_counter < 1000:
	rb = httplib.HTTP('www.bing.com')
	rb.putrequest('GET', "/search?q=%2B%40" + domain_name+ "&FORM=MSNH11&qs=n&first="+str(page_counter))
	rb.putheader('Host', 'www.bing.com')
	rb.putheader('Cookie', '_FP=mkt=en-US&ui=en-US;')
	rb.putheader('User-agent', 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.5; en-US; rv:1.9.0.4) Gecko/2008102920 Firefox/3.0.4')
	rb.endheaders()
	
	errcode, errmsg, headers = rb.getreply()
	
	if errcode!=200:
		print 'Error Sending Request', errcode, errmsg
	else:
		rbdata = rb.getfile().read()

	rbdata = re.sub('<strong>', '', rbdata)
	rbdata = re.sub('</strong>', '', rbdata)

	pattern='[\w\.\-]+@'+domain_name
	rbr1 = re.compile(pattern, re.I)
	rbresult = rbr1.findall(rbdata)
		
	page_counter = page_counter + 10
	
	for bemail in rbresult:
		if result.count(bemail) == 0:
			result.append(bemail)
			print "[*]-" + str(bemail)
			i=i+1
			l=httplib.HTTP('www.bing.com')
			l.putrequest('GET',"/search?q=%22"+str(bemail)+"%22&go=&form=QBRE&filt=all")
			l.putheader('Host', 'www.bing.com')
			l.putheader('Cookie', '_FP=mkt=en-US&ui=en-US;')
			l.putheader('User-agent', 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.5; en-US; rv:1.9.0.4) Gecko/2008102920 Firefox/3.0.4')
			l.endheaders()
			errcode, errmsg, headers = l.getreply()
	
			if errcode!=200:
				print 'Error Sending Request', errcode, errmsg
			else:
				lgdata = l.getfile().read()
			
			ml = re.compile('class="sb_tlst"><h3><a href="'+'(.*?)'+'onmousedown="return')
			ml1 = re.compile(">[a-zA-Z0-9@[\]?+_\-.:()| ]*</a></h3>")
			
			mlgresults = ml.findall(lgdata)
			mlgresults1 = ml1.findall(lgdata)

			mlgresults1 = re.sub('>','',str(mlgresults1))
			mlgresults1 = re.sub('</a','',str(mlgresults1))
			mlgresults1 = re.sub('</h3','',str(mlgresults1))
													
			print "[*][*]-Related Information about e-mail", bemail
			print "    |-", mlgresults1
			print "[*][*]-Related Links about e-mail", bemail

			for l in mlgresults:
				if result.count(l) == 0:
					result.append(l)
					l=re.sub('"','',l)
					print "    |--" + str(l)
print "\n[*]-Total e-mails found:", i

