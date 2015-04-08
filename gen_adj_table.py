#-*- coding:utf-8 -*-
import pprint
import re
import glob
import sys
import os
import time
import math

EBV_ITERR_TIMES = 30
ladj={}
radj={}
raw_text_substring=[]
wordhyp={}


def load_module(f_name):
    _curpath = os.path.normpath(os.path.join(os.getcwd(),os.path.dirname(__file__)))
    in_f = open(os.path.join(_curpath,f_name),'rb')
    with in_f:
        return eval(in_f.read())


    
def gen_all_substring(fname):
    global raw_text_substring

    for line in open(fname,"rb"):
        try:
            line = line.decode('utf-8')
        except:
            line = line.decode('gbk','ignore')
        line = line.strip().replace(" ","")
        if line != '':
            for i in range(len(line)-1):
                for j in range(2,10):
                    if j+i < len(line):
                        raw_text_substring.append(line[i:i+j])
    
    raw_text_substring = list(set(raw_text_substring))  #去重

def gen_adj():
    global raw_text_substring
    global ladj
    global radj
    global wordhyp

    wordhyp_set = set(wordhyp)  # 转化为set对判断元素属于关系效率更高
    if raw_text_substring:
        for i in range(len(raw_text_substring)):
            word = raw_text_substring[i]
            for j in range(len(word)-1):
                left_seq = word[0:j+1]
                right_seq = word[j+1:len(word)]
                if (left_seq in wordhyp_set) and (right_seq in wordhyp_set):
                    if ladj.has_key(right_seq):
                        ladj[right_seq].append(left_seq)
                    else:
                        ladj[right_seq]=[left_seq]
                    if radj.has_key(left_seq):
                        radj[left_seq].append(right_seq)
                    else:
                        radj[left_seq]=[right_seq]
        
        for node in ladj.keys():
            ladj[node] = list(set(ladj[node]))

        for node in radj.keys():
            radj[node] = list(set(radj[node]))
def dump():
#    global ladj
#    global radj

#    print "writing ladj to ladj_table.txt...",
#    pprint.pprint(ladj,open("ladj_table.txt","wb"))
#    print "done"

#    print "writing radj to radj_table.txt...",
#    pprint.pprint(radj,open("radj_table.txt","wb"))
#    print "done"
    global wordhyp_ebv
    pprint.pprint(wordhyp_ebv, open("ebv.txt","wb"))
    

if __name__== "__main__":
    time1=time.time()
    global wordhyp 
    wordhyp = load_module("word_hypothese.txt") #载入词假设
    wordhyp_freq = load_module("word_freq.txt")
    raw_txt = open("train_txt/pku_training.txt",'rb').read()
    size = len(raw_txt)
    
    print "generate substring ...\t",
    for fname in glob.glob("train_txt/*.txt"):
        gen_all_substring(fname)
    print "done"

    print "generate adj table",
    gen_adj()
    print "done"

    print "call ebv...\t",
    from gen_wordrank_model import cal_BV
    print "writing adj",
    pprint.pprint(ladj,open("ladj",'wb'))
    pprint.pprint(radj,open("radj",'wb'))
    print " done"
    #wordhyp_ebv = cal_EBV(wordhyp, ladj, radj, EBV_ITERR_TIMES)
   # pprint.pprint(wordhyp_ebv,open("ebv.txt","wb"))
   # wordhyp_ibv = gen_wordrank_model.cal_IBV(wordhyp,wordhyp_freq,size)
    cal_BV(wordhyp,ladj,radj,EBV_ITERR_TIMES,wordhyp_freq,size)
    print "done"

    time2=time.time()
    print time2-time1

#TODOrewrite this code depart the ebv() ,write trian.txt TODO
