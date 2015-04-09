#-*- coding:utf-8 -*-
#import codecs  open('ebv2.txt','wa+',"utf8")可以直接写中文
import sys
filename=sys.argv[1]
type1 = sys.argv[2]

s=eval(open(filename,'rb').read())
f = open(filename+'readable.txt','wa+')
if type1 == '1':
    for word in s:
        ss=word.encode('utf8')+'\n'
        f.write(ss)
if type1 == '2':
    for word in s.keys():
        f.write(word.encode('utf8')+':')  
        for w in s[word]:
            ss=w.encode('utf8')+','
            f.write(ss)
        f.write('\n')