#!/usr/bin/env python

import string

abc = string.ascii_lowercase

sol = ""

with open('./pych2') as f:
   text = f.read()
   for t in text:
      if t in abc:
         sol = sol + str(t)

print(sol)
