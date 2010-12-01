#!/usr/bin/python

import httplib
import urllib
import re
import sys
import string
import os
import subprocess

def help():
	print "[metadoc v1.0] - by neuro [0x0lab.org]"
	print "\nUsage: python metadoc.py <domain_name> \n"
	sys.exit()

if len(sys.argv) < 1 or len(sys.argv) > 2:
	help()
elif len(sys.argv) == 2:
	domain_name =  sys.argv[1]
else:
	help()
	
command='/usr/bin/exiftool'
command2='/usr/bin/strings'

DocRes=[]
Users=[]
DocEmail=[]

if not os.access(domain_name, os.F_OK):
	os.mkdir(domain_name)

os.chdir(domain_name)
dirname=domain_name

docg = httplib.HTTP('www.google.com')
docg.putrequest('GET', "/search?num=50&hl=en&btnG=B%C3%BASearch+en+Google&meta=&q=site%3A"+domain_name+"+filetype%3Adoc")
docg.putheader('Host', 'www.google.com')
docg.putheader('User-agent', 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.5; en-US; rv:1.9.0.4) Gecko/2008102920 Firefox/3.5.4')
docg.endheaders()
errcode, errmsg, headers = docg.getreply()

if errcode!=200:
	print 'Error Sending Request', errcode, errmsg
else:
	docgdata = docg.getfile().read()

doclinks = re.compile('"r"><a href="'+'(.*?)"'+' ')
doclinksres = doclinks.findall(docgdata)

i=0
y=0
em=0
print "[*]-Start downloading DOC(s) for domain:", domain_name

for p in doclinksres:
	if DocRes.count(p) == 0:
		DocRes.append(p)
		dlURL=str(p)
		dlDOC=domain_name+str(i)+".doc"
		urllib.urlretrieve(dlURL, dlDOC)
		i=i+1
		
		cmd=command + ' -author ' + dlDOC
		p=subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
		for line in p.stdout.readlines():
			if Users.count(line)==0:
				Users.append(line)
				u=line.replace("Author                          :","")
				print " |-" + dlURL + " (Author: " + u.rstrip('\n') + ")"
				y=y+1

		doccmd2=command2 + ' ' + dlDOC + ' ' + '|egrep "\w+([._-]\w)*@"'+domain_name
		docp1=subprocess.Popen(doccmd2, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
		for docmails in docp1.stdout.readlines():
			print "  |-e-mail:", docmails.rstrip('\n').encode('utf-8')
			em=em+1

print "[*]-Total docs downloaded:", i
print "[*]-Total authors found:", y
print "[*]-Total e-mails found:", em
