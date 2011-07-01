#!/usr/bin/python3.1
# -*- encoding: utf-8 -*-
"""
Created on 24/02/2011

Module used to solve Python Challenge number 6, for further information visit
http://www.pythonchallenge.com

@author: rafadurancastaneda@gmail.com
"""

import urllib.request as rq
import zipfile
import re
import os

def main():
   """Everything is done here"""
   if not os.path.exists('/home/rdc/channel.zip'):
      web = 'http://www.pythonchallenge.com/pc/def/channel.zip'
      fi = rq.URLopener()
      fi.retrieve(web,'/home/rdc/channel.zip')
   
   zip = zipfile.ZipFile('/home/rdc/channel.zip')
   
   text = ''
   next_nothing = ''
   search = re.compile(r'Next nothing is (\d+)')
   start_search = re.compile(r'\d\d+')
   comment = ''
   
   while True:
      if text == '':
         text = zip.read("readme.txt").decode('utf-8')
         next_nothing = start_search.findall(text)[0]
         print(next_nothing)
         print(text)
      else:
         text = zip.read(str(next_nothing)+'.txt').decode('utf-8')
         new_comment = zip.getinfo(str(next_nothing)+'.txt').\
            comment.decode('utf-8')
         if new_comment.isalpha() and new_comment not in comment:
            comment = comment + new_comment

         if text[:15] != 'Next nothing is':
            print(text)
            print(comment)
            break
         else:
            next_nothing = search.findall(text)[0]
            print(text)
            print(next_nothing)
            
   zip.close()


if __name__ == '__main__':
   main()
