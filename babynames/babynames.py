#!/usr/bin/python3.1
# Copyright 2010 Google Inc.
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

# Google's Python Class
# http://code.google.com/edu/languages/google-python-class/

import sys
import re
import os

from urllib import request
from html.parser import HTMLParser

"""Baby Names exercise

Define the extract_names() function below and change main()
to call it.

For writing regex, it's nice to include a copy of the target
text for inspiration.

Here's what the html looks like in the baby.html files:
...
<h3 align="center">Popularity in 1990</h3>
....
<tr align="right"><td>1</td><td>Michael</td><td>Jessica</td>
<tr align="right"><td>2</td><td>Christopher</td><td>Ashley</td>
<tr align="right"><td>3</td><td>Matthew</td><td>Brittany</td>
...

Suggested milestones for incremental development:
 -Extract the year and print it
 -Extract the names and rank numbers and just print them
 -Get the names data into a dict and print it
 -Build the [year, 'name rank', ... ] list and print it
 -Fix main() to use the extract_names list
"""

class MyHTMLParser(HTMLParser):
   """ HTML parser, it cactchs and save in a list year and
   baby names
   """
   def __init__(self):
      """__init__ method, overrides super"""
      super(MyHTMLParser, self).__init__()
      self.h3_flag = False
      self.td_flag = False
      self.year = ""
      self.names = []
      self.name1 = ""
      self.order = ""
   def handle_starttag(self, tag, attrs):
      """ Searches start tags, overrides super"""
      if tag == "h3":
         self.h3_flag = True
      elif self.year!= "" and tag == "td" and attrs == []:
         self.td_flag = True
   def handle_endtag(self, tag):
      """ Searches ends tags, overrides super"""
      if tag=="h3":
         self.h3_flag = False
      elif tag == "td":
         self.td_flag = False
   def handle_data(self, data):
      """ Save data when tags are found, overrides super"""
      if self.h3_flag:
         li = data.split()
         self.year = li[len(li)-1]
      elif self.td_flag and data.isnumeric():
         self.order = data
      elif self.td_flag and self.name1 == "":
         self.name1 = data
      elif self.td_flag and self.name1 != "":
         self.names += [self.name1+" "+self.order,]
         self.names += [data+" "+self.order,]
         self.name1 = ""

def extract_names(filename):
   """
   Given a file name for baby.html, returns a list starting with the year string
   followed by the name-rank strings in alphabetical order.
   ['2006', 'Aaliyah 91', Aaron 57', 'Abagail 895', ' ...]
   """
   text = request.urlopen(filename).read().decode("utf8")
   myparser = MyHTMLParser()
   myparser.feed(text)
   myparser.names.sort()
   return [myparser.year,] + myparser.names

def main():
   # This command-line parsing code is provided.
   # Make a list of command line arguments, omitting the [0] element
   # which is the script itself.
   args = sys.argv[1:]

   if not args:
      print('usage: [--summaryfile] file [file ...]')
      sys.exit(1)
   
  
    # Notice the summary flag and remove it from args if it is present.
   summary = False
   if args[0] == '--summaryfile':
      summary = True
      del args[0]

   di = {}
   for i in range(len(args)):
      li = extract_names("file:///"+os.getcwd()+"/"+args[i])
      di[li[0]] = li      
   
   if summary:
      with open("summary.txt","at") as f:
         for d in di:
            f.write(str(di[d]) + '\n')
      f.close()
   else:
      for d in di:
         print(di[d])
    

    # +++your code here+++
    # For each filename, get the names, then either print the text output
    # or write it to a summary file
  
if __name__ == '__main__':
  main()
