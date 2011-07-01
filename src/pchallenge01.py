#!/usr/bin/env python

texto = "map"
texto_final = ""
for i in range(len(texto)):
    if texto[i].isalpha():
        if texto[i] not in ('y','z'):
            num = ord(texto[i])
            num += 2
            texto_final = texto_final + chr(num)
        elif texto[i] == 'y':
            texto_final = texto_final + 'a'
        elif texto[i] in 'z':
            texto_final = texto_final + 'b'
    else:
        texto_final = texto_final + texto[i]
print(texto_final)
