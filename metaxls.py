#!/usr/bin/python

import httplib
import urllib
import re
import sys
import string
import os
import subprocess

def help():
	print "[metaxls v1.0] - by neuro [0x0lab.org]"
	print "\nUsage: python metaxls.py <domain_name> \n"
	sys.exit()

if len(sys.argv) < 1 or len(sys.argv) > 2:
	help()
elif len(sys.argv) == 2:
	domain_name =  sys.argv[1]
else:
	help()
	
command='/usr/bin/exiftool'
command2='/usr/bin/strings'

XlsRes=[]
Users=[]
XlsEmail=[]

if not os.access(domain_name, os.F_OK):
	os.mkdir(domain_name)

os.chdir(domain_name)
dirname=domain_name

xlsg = httplib.HTTP('www.google.com')
xlsg.putrequest('GET', "/search?num=50&hl=en&btnG=B%C3%BASearch+en+Google&meta=&q=site%3A"+domain_name+"+filetype%3Axls")
xlsg.putheader('Host', 'www.google.com')
xlsg.putheader('User-agent', 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.5; en-US; rv:1.9.0.4) Gecko/2008102920 Firefox/3.5.4')
xlsg.endheaders()
errcode, errmsg, headers = xlsg.getreply()

if errcode!=200:
	print 'Error Sending Request', errcode, errmsg
else:
	xlsgdata = xlsg.getfile().read()

xlslinks = re.compile('"r"><a href="'+'(.*?)"'+' ')
xlslinksres = xlslinks.findall(xlsgdata)

i=0
y=0
em=0
print "[*]-Start downloading XLS(s) for domain:", domain_name

for p in xlslinksres:
	if XlsRes.count(p) == 0:
		XlsRes.append(p)
		dlURL=str(p)
		dlXLS=domain_name+str(i)+".xls"
		urllib.urlretrieve(dlURL, dlXLS)
		i=i+1
		
		cmd=command + ' -author ' + dlXLS
		p=subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
		for line in p.stdout.readlines():
			if Users.count(line)==0:
				Users.append(line)
				u=line.replace("Author                          :","")
				print " |-" + dlURL + " (Author: " + u.rstrip('\n') + ")"
				y=y+1

		xlscmd2=command2 + ' ' + dlXLS + ' ' + '|egrep "\w+([._-]\w)*@"'+domain_name
		xlsp1=subprocess.Popen(xlscmd2, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
		for xlsmails in xlsp1.stdout.readlines():
			print "  |-e-mail:", xlsmails.rstrip('\n').encode('utf-8')
			em=em+1

print "[*]-Total xls(s) downloaded:", i
print "[*]-Total authors found:", y
print "[*]-Total e-mails found:", em
