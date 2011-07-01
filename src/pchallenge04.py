#!/usr/bin/python3.1
# -*- encoding: utf-8 -*-
'''
Created on 23/02/2011

Module used to solve Python Challenge number 4, for further information visit
`Link www.pythonchallenge.com <http://www.pythonchallenge.com>`_ 

@author: rafadurancastaneda@gmail.com
'''
import urllib.request as rq
import re

def main():
   next_link = '12345'
   web = 'http://www.pythonchallenge.com/pc/def/linkedlist.php?nothing='
   
   for unused_i in range(300):
      text = rq.urlopen(web+next_link).read().decode('utf-8')

      if 'html' in text:
         print(text)
         break
      elif text == 'Yes. Divide by two and keep going.':
         next_link = str(int(next_link) / 2)
      else:
         next_link = str(re.findall(r'the next nothing is ([0-9]+)',text))[2:-2]
      print(text)

if __name__ == '__main__':
   main()