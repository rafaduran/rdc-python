import urllib
import zipfile
from StringIO import StringIO

zobj = StringIO()
zobj.write(urllib.urlopen("http://pythonchallenge.com/pc/def/channel.zip").read())
z = zipfile.ZipFile(zobj)

filenum = "90052"
lcomment = []

while True:
    if filenum.isdigit():
        filename = filenum + '.txt'
        lcomment.append(z.getinfo(filename).comment)
        info = z.read(filename)
        filenum = info.split(' ')[-1]
    else:
        break
z.close()
print ''.join(lcomment)
