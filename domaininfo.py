#!/usr/bin/python

import sys
import string
import dns.resolver
import dns.zone
import socket

def help():
	print "[domaininfo.py v 1.0] - by neuro [0x0lab.org]"
	print "\nUsage: python domaininfo.py <domain_name>\n"
	sys.exit()

if len(sys.argv) < 1 or len(sys.argv) > 2:
	help()
elif len(sys.argv) == 2:
	domain_name =  sys.argv[1]
else:
	help()

print "[*]-Trying retrieve Domain Information for domain", domain_name
	
def A(domain_name):
	global arec
	print "[*][*]-Trying retrieve A record(s)"
	try:
		A = dns.resolver.query(domain_name, 'A')
		for arec in A:
			print '    |--', arec
	except:
		print '    |-- Failed to retrieve A record(s)'

#Display MX Record for a given domain
def MX(domain_name):
	global mxrec
	global a
	print "[*][*]-Trying retrieve MX record(s)"
	try:
		mx = dns.resolver.query(domain_name, 'MX')
		for mxrec in mx:
			for ip in dns.resolver.query(mxrec.exchange):
				print '    |--', mxrec.exchange, 'has preference', mxrec.preference, ip
	except:
		print '    |-- Failed to retrieve MX record(s)'

#Display NS Record for a given domain
def NS(domain_name):
	print "[*][*]-Trying retrieve NS record(s)"
	try:
		NS = dns.resolver.query(domain_name, 'NS')
		for nsrec in NS:
			print '    |--', nsrec
	except:
		print '    |-- Failed to retrieve Name Server(s)'

#Display SOA Record for a given domain
def SOA(domain_name):
	print "[*][*]-Trying retrieve SOA record(s)"
	try:
		SOA = dns.resolver.query(domain_name, 'SOA')
		for soarec in SOA:
			print '    |--', soarec
	except:
		print '    |-- Failed to retrieve SOA record(s)'

def Zone_Transfer(domain_name):
	NS = dns.resolver.query(domain_name, 'NS')
	ns = []

	for rdata in NS:
		n = str(rdata)
   		ns.append(n)
	
	for n in ns:
		print "[*][*]-Trying a zone transfer for %s from name server %s" % (domain_name, n)
		try:
			zone = dns.zone.from_xfr(dns.query.xfr(n, domain_name))
			for name, node in zone.nodes.items():
				rdataset = node.rdatasets
				for record in rdataset:
					print '    |--', name, record
		except:
			print '    |-- Zone Transfer failed'

A(domain_name)
MX(domain_name)
NS(domain_name)
SOA(domain_name)
Zone_Transfer(domain_name)
