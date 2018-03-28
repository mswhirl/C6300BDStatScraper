# (c) Mark Smith (Whirlpool).  License: GPLv3
# Only tested on Windows
import http.client, re, html2text, os
from urllib.parse import urlencode
from urllib.request import Request, urlopen

#setup
modem = '192.168.100.1'
username = 'admin'
password = 'password'

#get the login url which is dynamic
conn = http.client.HTTPConnection(modem)
conn.request("GET", "/")
r1 = conn.getresponse()
print(r1.status, r1.reason)
data1 = r1.read()
loginurl = re.compile("""(?:<form name="HngLoginForm" action=")([^"]+)""")
out = loginurl.search(data1.decode())

#authenticate
url = 'http://' + modem + out.group(1)  # Set destination URL here
post_fields = {'HngLoginUserName': username, 'HngLoginPassword' : password}     # Set POST fields here
request = Request(url, urlencode(post_fields).encode())
json = urlopen(request).read().decode()
#no cookie etc is used - it seems to be IP based?

#at this point we can query away - make sure html2text is installed 'pip install html2text'
output = ""
conn.request("GET", "/HngConnectionSettings.asp")
r1 = conn.getresponse()
print(r1.status, r1.reason)
data1 = r1.read()
h = html2text.HTML2Text()
h.body_width = 999
body = h.handle(data1.decode())
body = body[body.find('Connection Settings'):body.find('# MENU')]
print(body)
output += body

# get system information
conn.request("GET", "/HngIndex.asp")
r1 = conn.getresponse()
print(r1.status, r1.reason)
data1 = r1.read()
h = html2text.HTML2Text()
h.body_width = 999
body = h.handle(data1.decode())
body = body[body.find('Information'):body.find('# MENU')]
print(body)
output += body

# get system log
conn.request("GET", "/HngEventLog.asp")
r1 = conn.getresponse()
print(r1.status, r1.reason)
data1 = r1.read()
h = html2text.HTML2Text()
h.body_width = 999
body = h.handle(data1.decode())
body = body[body.find('System Event Log'):body.find('# MENU')]
print(body)
output += body

# save and open in default text editor 
outfile = os.path.join(os.environ['TEMP'], 'cablestats.txt')
out = open(outfile, 'w+')
out.write(output)
out.close()
os.startfile(outfile)
