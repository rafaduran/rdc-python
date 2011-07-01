'''
Created on 23/02/2011

@author: rdc
'''
#!/usr/bin/env python3.1

import re
import urllib.request as r

def main():
   url="http://www.pythonchallenge.com/pc/def/linkedlist.php?nothing="
   nothing = "12345"
   search = re.compile(" (\d*)$")
   search_html = re.compile("\.html$")

   for unused_i in range(300): 
      print("%s: " % nothing)

      line = r.urlopen( "%s%s" % (url,nothing) ).read()
      print(line)

      # handle the solution (last) line
      if search_html.findall (line):
         break
        
      match = search.findall (line)
      if match:
         # next nothing
         nothing = match[0]
      else:
         # handle the divide by two line
         nothing = str (int (nothing) / 2)
                           
if __name__ == '__main__':
   main()
 