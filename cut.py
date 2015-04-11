#-*- coding:utf-8 -*-
import glob
import sys
import os
wordrank_value={}
Lmax = 5
def load_module(f_name):
    _curpath = os.path.normpath(os.path.join(os.getcwd(),os.path.dirname(__file__)))
    in_f = open(os.path.join(_curpath,f_name),'rb')
    with in_f:
        return eval(in_f.read())


def cut(str):
    global wordrank_value
    result=[]
    str=' '+str
    global Lmax
    str_len = len(str)
    op=[-float('inf')]*str_len
    op[0]=1
    path= [0]*str_len
    for i in range(1,str_len):
        pos_start = max(0,i-Lmax)
        for k in range(pos_start,i):
#            print "(",
#            print i,',',k,")   "
#            print path
#            print op
            if wordrank_value.has_key(str[k+1:i+1])==False:
                wrv = 0
            else:
                wrv = wordrank_value[str[k+1:i+1]]
                
            if op[k]*wrv > op[i]:
                op[i]=op[k]*wrv
                path[i]=k;
    d=[i for i in path]
    print d
    i = str_len-1
    out=[]
    while  path[i]!=0:
        out.append(path[i])
        i = path[i]
    if i==0:
        out.append(path[0])
    out = out[::-1]
    print out
    if out ==[]:
        result = str[1:str_len]
    else:
        pre = 1
        for pos in out:
            result.append(str[pre:pos+1])
            pre = pos+1
        result.append(str[pre:str_len])

    for s in result:
        print s
    
    return result
        

if __name__ == "__main__":
    global wordrank_value
    if sys.argv[1]=='0':
       	wordrank_value = load_module("ibv.txt")
    elif sys.argv[1]=='1':
        wordrank_value = load_module("ebv.txt")
    elif sys.argv[1]=='2':
        wordrank_value = load_module("wr_model.txt")

    while True :
        str=raw_input()
        if str!='':
            str = str.decode("utf-8")
            cut(str)
            
