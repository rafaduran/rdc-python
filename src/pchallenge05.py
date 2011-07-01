#!/usr/bin/python3.1
# -*- encoding: utf-8 -*-
'''
Created on 24/02/2011

Module used to solve Python Challenge number 5, for further information visit
`Link www.pythonchallenge.com <http://www.pythonchallenge.com>`_ 

@author: rafadurancastaneda@gmail.com
'''
import urllib.request as rq
import pickle

def main():
   web = 'http://www.pythonchallenge.com/pc/def/banner.p'
   #web = 'http://www.pythonchallenge.com/pc/def/peakhell.jpg'
   data = rq.urlopen(web)
   li = pickle.load(data)
   for l in li:
      text = ''
      for x in l:
         text+= x[0] * x[1]
      print(text)
   


if __name__ == '__main__':
   main()
