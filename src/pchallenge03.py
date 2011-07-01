#!/usr/bin/python3.1
# """File to try solve python challenge number 3"""
import urllib.request as rq
import re

text = ((rq.urlopen("http://www.pythonchallenge.com/pc/def/equality.html"))
    .read()).decode("utf8")

print("".join(re.findall(r'[a-z][A-Z]{3}([a-z])[A-Z]{3}[a-z]',text)))


