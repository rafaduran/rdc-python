#!/usr/bin/python2.6
# -*- encoding: utf-8 -*-
'''
Created on 25/02/2011

Module used to solve Python Challenge number 7, for further information visit
http://www.pythonchallenge.com

@author: rafadurancastaneda@gmail.com
'''
#import urllib.request as rq
import urllib
import os

from PIL import Image


def main():
   if not os.path.exists('/home/rdc/oxygen.png'):
      web = 'http://www.pythonchallenge.com/pc/def/oxygen.png'
      fi = urllib.URLopener()
      fi.retrieve(web,'/home/rdc/oxygen.png')
   im = Image.open('/home/rdc/oxygen.png')
   
   n_img = im.crop((0,43,604,52)) 
   
   li = [x[0] for x in list(n_img.getdata())]
   
   print(''.join([chr(l) for l in li]))
   
   print(''.join(chr(n) for n in [105, 110 ,116, 101, 103, 114, 105, 116, 121]))
      
   
if __name__ == '__main__':
   main()
