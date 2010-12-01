#!/usr/bin/python

import sys
import socket
import IPy

def help():
	print "[rdns v1.0] - by neuro [0x0lab.org]"
	print "\nUsage: python rdns.py\n"
	print "Example: python rdns.py 10.0.0.0/24"
	print "Example: python rdns.py 10.0.0.0-10.0.0.254"
	print "Example: python rdns.py www.abcd.com/24\n"
	print "Note: IPy Python module is needed http://c0re.23.nu/c0de/IPy/"
	sys.exit()

if len(sys.argv) < 1 or len(sys.argv) > 2:
	help()
elif len(sys.argv) == 2:
	CIDR =  sys.argv[1]
else:
	help()

if CIDR.count('.')==3:
	ip=IPy.IP(CIDR)
elif CIDR.count('.')==6:
	try:
		ip=IPy.IP(CIDR)
	except:
		pass
else:
	parts=CIDR.split('/')
	value1=parts[0]
	value2=parts[1]
	s = socket.gethostbyname(value1)
	ipsplit=s.split('.')
	ipsplit[3]="0"
	newip=ipsplit[0]+"."+ipsplit[1]+"."+ipsplit[2]+"."+ipsplit[3]+"/"+value2
	ip=IPy.IP(newip)

i=0
print "[*]-Testing CIDR Range:", ip
for x in ip:
	try:
		s = socket.gethostbyaddr(str(x))
		print " |--",s
		i=i+1
	except:
		pass
print "[*]-Total Reverse DNS found:", i
