#!/usr/bin/python

import sys
import string
import socket

def help():
	print "[bfdomain v1.0] - by neuro [0x0lab.org]"
	print "\nUsage: python mgoogle.py domain_name dictionary\n"
	sys.exit()

if len(sys.argv) < 1 or len(sys.argv) > 3:
	help()
elif len(sys.argv) == 3:
	domain_name =  sys.argv[1]
	filename =  sys.argv[2]
else:
	help()

file = open(filename,'r')
fc = open(filename, 'r')
cnames = fc.readlines()

print "[*]-Using dictionairy: " + filename + " (Loaded " + str(len(cnames)) + " words)"

l=0
i=0
for line in file.read().split('\n'):
	l=l+1
	ESC = chr(27)
	sys.stdout.write(ESC + '[2K'+ ESC + '[G')
	sys.stdout.write(' |-' + line+ ' (line: ' + str(l) + ')' + ' ==> ')
	sys.stdout.flush()
	try:
		s = socket.gethostbyname_ex(line+"."+domain_name)
		print s
		i=i+1
	except:
		pass
sys.stdout.write(ESC + '[2K'+ESC + '[G')
print "[*]-Total assets found:", i
file.close()
fc.close()