#!/usr/bin/python3.1
# Copyright 2010 Google Inc.
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

# Google's Python Class
# http://code.google.com/edu/languages/google-python-class/

import sys
import re
import os
import shutil
#import commands
import zipfile

"""Copy Special exercise
"""

# +++your code here+++
# Write functions and modify main() to call them

def get_special_files(dir_list):
   """For each dir in dir_list finds all special files(__w__, w word
   character)
   """
   special_files = []
   try:
      for dirs in dir_list:
         if dirs[len(dirs)-1] != '/':
            dirs = dirs + '/'
         for files in os.listdir(dirs):
            if re.findall(r'(__[a-z]+__)|(__[A-Z]+__)', files) != []:
               special_files += [dirs + files,]
   except:
      print("Error inside get_special_files")
      raise
   
   return special_files
   
def to_zip(dst_zip, source_dir_list):
   """ Zips all dirs in source_dir_list in file: dst_zip.zip"""
   
   special_files = get_special_files(source_dir_list)
   
   if special_files == []:
      print("No special files found")
      sys.exit(1)
   
   try:
      if dst_zip[:-4]!=".zip":
         dst_zip = dst_zip + ".zip"
      f_dst= zipfile.ZipFile(dst_zip,'w')
      for files in special_files:
         f_dst.write(files, os.path.basename(files), zipfile.ZIP_DEFLATED)
      f_dst.close()
   except:
      print("Error inside to_zip")
      raise

def to_dir(dst_dir, list_source_dir):
   """ Copy all files in list_source_dir to target_dir"""
   special_files = get_special_files(list_source_dir)
   
   if special_files == []:
      print("No special files found")
      sys.exit(1)
   elif dst_dir in list_source_dir:
      print("Destination dir can't be source dir")
      sys.exit(1)
      
   try:
      for files in special_files:
         shutil.copy(files,dst_dir)
   except:
      print("Error inside to_dir")
      raise
   
   

def main():
   # This basic command line argument parsing code is provided.
   # Add code to call your functions below.

   # Make a list of command line arguments, omitting the [0] element
   # which is the script itself.
   args = sys.argv[1:]
   if not args:
      print("usage: [--todir dir][--tozip zipfile] dir [dir ...]")
      sys.exit(1)

   # todir and tozip are either set from command line
   # or left as the empty string.
   # The args array is left just containing the dirs.
   todir = ''
   if args[0] == '--todir':
      todir = args[1]
      del args[0:2]

   tozip = ''
   if args[0] == '--tozip':
      tozip = args[1]
      del args[0:2]

   if len(args) == 0:
      print("error: must specify one or more dirs")
      sys.exit(1)
   try:
      if tozip != '':
         to_zip(tozip, args)
      elif todir != '':
         to_dir(todir, args)
   except RuntimeError as err:
      print("RuntimeError: {0}".format(err))
      sys.exit(1)
   except OSError as ose:
      print("OS error: {0}".format(ose))
      sys.exit(1)
   except:
      print("Unexpected error:", sys.exc_info()[0])
      sys.exit(1)
  
if __name__ == "__main__":
  main()
