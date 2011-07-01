#!/usr/bin/python3.1
# Copyright 2010 Google Inc.
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

# Google's Python Class
# http://code.google.com/edu/languages/google-python-class/

import os
import re
import sys
import urllib2
import urllib
from PIL import Image

"""Logpuzzle exercise
Given an apache logfile, find the puzzle urls and download the images.

Here's what a puzzle url looks like:
10.254.254.28 - - [06/Aug/2007:00:13:48 -0700] "GET /~foo/puzzle-bar-aaab.jpg HTTP/1.0" 302 528 "-" "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.6) Gecko/20070725 Firefox/2.0.0.6"
"""

def catch_urls(text):
    """From a given text, search for each url, printing repeateds"""
    urls = sorted(list(url for url in re.findall(r'([\S]+.jpg)',text) if url.find("puzzle")!=-1))
    
    urls_not_repeated = [urls[0],]
    #urls_not_repeated += \
        #(urls[i] for i in range(1,len(urls)) if urls[i] != urls[i-1])
    for i in range(1, len(urls)):
        if urls[i-1] == urls[i]:
            print("url repeated: " + urls[i])
        else:
            urls_not_repeated += [urls[i],]
    
    return urls_not_repeated
    
    

def read_urls(filename):
  """Returns a list of the puzzle urls from the given log file,
  extracting the hostname from the filename itself.
  Screens out duplicate urls and returns the urls sorted into
  increasing order."""
  text = ""
  with open(filename,"rt") as f:
      text = f.read()
  f.close()
  
  server = filename[filename.find('_')+1:]
  
  urls = catch_urls(text)
  
  urls = list(server+url for url in urls)
  
  #print(urls)
  
  return urls
  

def download_images(img_urls, dest_dir):
    """Given the urls already in the correct order, downloads
    each image into the given directory.
    Gives the images local filenames img0, img1, and so on.
    Creates an index.html in the directory
    with an img tag to show each local image file.
    Creates the directory if necessary.
    """
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
    with open(dest_dir+"index.html","wt") as f:
        f.write("<html>")
        for i,urls in enumerate(img_urls):
            fu = urllib.URLopener()
            fu.retrieve("http://"+urls, str(dest_dir)+"img"+str(i)+".jpg")
            f.write("<img src="+dest_dir+"img"+str(i)+".jpg>")
        f.write("</html>")
    img=Image.open(dest_dir+"img0.jpg",'r')
    img_w,img_h=img.size
    img_out = Image.new('RGBA', (img_w*len(img_urls),img_h))
    img_out.paste(img,(0, 0))
    for i in range(1,len(img_urls)): 
        img=Image.open(dest_dir+"img"+str(i)+".jpg",'r')
        offset=(i*img_w,0)
        img_out.paste(img,offset)
    img_out.save(dest_dir+'out.png')
      
def main():
  args = sys.argv[1:]

  if not args:
    print('usage: [--todir dir] logfile ')
    sys.exit(1)

  todir = ''
  if args[0] == '--todir':
    todir = args[1]
    del args[0:2]

  img_urls = read_urls(args[0])

  if todir:
    download_images(img_urls, todir)
  else:
    print('\n'.join(img_urls))

if __name__ == '__main__':
  main()
