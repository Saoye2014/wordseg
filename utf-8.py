#-*- coding:utf-8 -*-
#import codecs  open('ebv2.txt','wa+',"utf8")可以直接写中文
import sys
filename=sys.argv[1]
print "decode"+filename
s=eval(open(filename+'.txt','rb').read())
s1=sorted(s.iteritems(),key=lambda abs:abs[0],reverse=False)
f = open(filename+'sotedbykey_.txt','wa+')
for word in s1:
    ss=word[0].encode('utf8')+"   "+str(word[1])+'\n'
    f.write(ss)

s2=sorted(s.iteritems(),key=lambda abs:len(abs[0]),reverse=False)
f = open(filename+'sortedbykey_len.txt','wa+')
for word in s2:
    ss=word[0].encode('utf8')+"   "+str(word[1])+'\n'
    f.write(ss)
    
s3=sorted(s.iteritems(),key=lambda abs:abs[1],reverse=True)
f = open(filename+'sortedby_ebv.txt','wa+')
for word in s3:
    ss=word[0].encode('utf8')+"   "+str(word[1])+'\n'
    f.write(ss)