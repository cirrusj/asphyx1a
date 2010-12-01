#!/usr/bin/python

import sys
import string
import socket
import os


def help():
	print "[tlds v1.0] - by neuro [0x0lab.org]"
	print "\nUsage: python tlds.py domain_name\n"
	sys.exit()

if len(sys.argv) < 1 or len(sys.argv) > 2:
	help()
elif len(sys.argv) == 2:
	domain_name =  sys.argv[1]
else:
	help()

dnsplit=domain_name.split('.')
dn='www.'+'.'.join(dnsplit[:1])

tldsfilename = open("tlds",'r')

print "[*]-Top Level Domains for domain:", domain_name

i=0
for tldline in tldsfilename.read().split('\n'):
	try:
		tlds = socket.gethostbyname_ex(dn+tldline)
		print ' |--'+str(tlds)
		i=i+1
	except:
		pass
print "[*]-Total Top Level Domains found:", i
tldsfilename.close()
