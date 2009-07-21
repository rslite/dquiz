from BeautifulSoup import BeautifulSoup
import re, sys

f = open(sys.argv[1])
data = f.read()
f.close()

rgComments = re.compile(r'<!--.*?-->', re.S)
rgSpan = re.compile(r'</?(span|div).*?>', re.S)
rgLetters = re.compile(r'([a-z])<strong>:</strong>', re.S)
rgStrong = re.compile(r'\s*<strong>:</strong>', re.S)
rgSynonim = re.compile(r'<div class="synonym".*$', re.S)
rgSpaces = re.compile(r'\s+', re.S)

data = rgComments.sub('', data)

bs = BeautifulSoup(data)
main = bs.findAll('div', attrs={'class':'defs'})[0]
print main
print

txt = rgSpaces.sub(' ', str(main).replace('\x0A', ' '))
print txt
print

entries = txt.split('<span class=" sense_label start">')[1:]

for entry in entries:
	# Remove synonyms (in last entry)
	entry = rgSynonim.sub('', entry)
	# Get rid of spans, divs
	entry = rgSpan.sub('', entry)
	# Bold the subdef letters (a, b, ...)
	entry = rgLetters.sub(r'*\1*', entry)
	# Remove the digits of the definitions
	entry = re.sub(r'^\d\s*', '', entry)
	# Remove the strong colons
	entry = rgStrong.sub(':', entry)
	# Remove the colons at the beginning
	entry = re.sub(r'^:\s*', '', entry)
	# Change obsolete marker
	entry = re.sub(r'<em>(obsolete|also|especially)</em>', r'(\1)', entry)
	# Change word in examples
	entry = re.sub(r'</?em>', '_', entry)
	# Remove links
	entry = re.sub(r'</?a.*?>', '', entry)
	# Replace < and >
	entry = entry.replace('&lt;', '<').replace('&gt;', '>')

	print entry
	print

