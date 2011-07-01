'''
Created on 24/02/2011

@author: rdc
'''
print '\n'.join(''.join(i[0] * i[1] for i in l) for l in
                __import__('pickle').loads(__import__('urllib').urlopen(
                'http://www.pythonchallenge.com/pc/def/banner.p'
                ).read()))
