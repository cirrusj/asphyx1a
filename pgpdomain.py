#!/usr/bin/python

import httplib
import re
import sys
import string

def help():
	print "[pgpdomain v1.0] - by neuro [0x0lab.org]"
	print "\nUsage: python pgpdomain.py <domain_name> \n"
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
rpgp = httplib.HTTP('pgp.mit.edu:11371')
rpgp.putrequest('GET', "/pks/lookup?search=" + domain_name + "&op=index")
rpgp.putheader('Host', 'pgp.mit.edu')
rpgp.putheader('User-agent', 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.5; en-US; rv:1.9.0.4) Gecko/2008102920 Firefox/3.0.4')
rpgp.endheaders()
	
errcode, errmsg, headers = rpgp.getreply()

print "[*]-Start checking GPG server ==> pgp.mit.edu:11371"

if errcode!=200:
	print ' |-Error Sending Request', errcode, errmsg
	exit
else:
	rpgpdata = rpgp.getfile().read()
	
	pattern='[\w\.\-]+@'+domain_name
	rpgpreg = re.compile(pattern, re.I)
	rpgpresult = rpgpreg.findall(rpgpdata)
	
	for pgpemail in rpgpresult:
		if result.count(pgpemail) == 0:
			result.append(pgpemail)
			print " |-" + str(pgpemail)
			i=i+1

	print "[*]-Total e-mails found (gpg):", i

		