import httplib
import re
import sys
import string

def help():
	print "[rwhois v1.0] - by Neuro [0x0labs.org]"
	print "\nUsage: rwhois.py <netname or IP> \n"
	sys.exit()

if len(sys.argv) < 1 or len(sys.argv) > 2:
	help()
elif len(sys.argv) == 2:
	name =  sys.argv[1]
else:
	help()

print "[*]-Start Searching in RIPE (Free Text Search-Glimpse)"

r = httplib.HTTP('www.ripe.net')
r.putrequest('GET', "/cgi-bin/search/gdquery.cgi?index=ripedb&file-match=net[6n]&boolean=and&max-results=100&page-results=100&start-page=%2Fdb%2Fwhois-free.html&header=whois&footer=whois&record-type=paragraph&terms="+name+"&Search=Search&show-context=1&degree-of-error=0&.cgifields=search-substrings&.cgifields=case-sensitive&.cgifields=show-context")
r.putheader('Host', 'www.ripe.net')
r.putheader('User-agent', 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.5; en-US; rv:1.9.0.4) Gecko/2008102920 Firefox/3.5.4')
r.endheaders()
errcode, errmsg, headers = r.getreply()

if errcode!=200:
	print 'Error Sending Request', errcode, errmsg
else:
	rdata = r.getfile().read()

rdata = re.sub('<B>', '', rdata)
rdata = re.sub('</B>', '', rdata)
rdata = re.sub('&quot;', '', rdata)

ripe_pattern = re.compile('>inetnum: [0-9-. ]*<br>netname: [A-Za-z0-9-,./()_| ]*<br>descr: [A-Za-z0-9-,./()_| ]*<br>')
ripe_result = ripe_pattern.findall(rdata)

i=0

for riperes in ripe_result:
	ripe_clean = re.sub('>', '', riperes)
	ripe_clean = re.sub('<', '', ripe_clean)
	ripe_clean = re.sub('br', ' |', ripe_clean)
	totalriperes = ripe_clean
	print " |-", totalriperes
	i=i+1
print "[*] Total information found:", i



