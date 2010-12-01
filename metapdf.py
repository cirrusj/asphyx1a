#!/usr/bin/python

import httplib
import urllib
import pyPdf
import re
import sys
import string
import os
import subprocess

def help():
	print "[metapdf v1.0] - by neuro [0x0lab.org]"
	print "\nUsage: python metapdf.py <domain_name> \n"
	sys.exit()

if len(sys.argv) < 1 or len(sys.argv) > 2:
	help()
elif len(sys.argv) == 2:
	domain_name =  sys.argv[1]
else:
	help()
	
command='/usr/bin/exiftool'

PDFRes=[]
Users=[]
PDFEmail=[]
content=""

if not os.access(domain_name, os.F_OK):
	os.mkdir(domain_name)

os.chdir(domain_name)
dirname=domain_name

pdfg = httplib.HTTP('www.google.com')
pdfg.putrequest('GET', "/search?num=100&hl=en&btnG=B%C3%BASearch+en+Google&meta=&q=site%3A"+domain_name+"+filetype%3Apdf")
pdfg.putheader('Host', 'www.google.com')
pdfg.putheader('User-agent', 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.5; en-US; rv:1.9.0.4) Gecko/2008102920 Firefox/3.5.4')
pdfg.endheaders()
errcode, errmsg, headers = pdfg.getreply()

if errcode!=200:
	print 'Error Sending Request', errcode, errmsg
else:
	pdfgdata = pdfg.getfile().read()

pdflinks = re.compile('"r"><a href="'+'(.*?)"'+' ')
pdflinksres = pdflinks.findall(pdfgdata)

i=0
y=0
em=0
print "[*]-Start downloading PDF(s) for domain:", domain_name

for p in pdflinksres:
	if PDFRes.count(p) == 0:
		PDFRes.append(p)
		dlURL=str(p)
		dlPDF=domain_name+str(i)+".pdf"
		urllib.urlretrieve(dlURL, dlPDF)
		i=i+1
		
		cmd=command + ' -author ' + dlPDF
		p=subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
		for line in p.stdout.readlines():
			if Users.count(line)==0:
				Users.append(line)
				u=line.replace("Author                          :","")
				print " |-" + dlURL + " (Author: " + u.rstrip('\n') + ")"
				y=y+1
		
		try:
			pdf = pyPdf.PdfFileReader(file(dlPDF, "rb"))
			for x in range(0, pdf.getNumPages()):
				content += pdf.getPage(x).extractText() + "\n"

			pdfemail = re.compile('[\w\.\-]+@'+domain_name)
			epdfresult = pdfemail.findall(content)	

			for epdf in epdfresult:
				if PDFEmail.count(epdf) == 0:
					PDFEmail.append(epdf)
					print "  |-e-mail:", epdf.encode('utf-8')
					em=em+1
		
		except IOError,e:
			pass
		except pyPdf.utils.PdfReadError, e:
			pass
		except Exception,e:
			pass

print "[*]-Total pdfs downloaded:", i
print "[*]-Total authors found:", y
print "[*]-Total e-mails found:", em
