#-*- coding:utf-8 -*-
import pprint
import re
import glob
import sys
wordhyp={}
def get_word_hypo(line):
    re_not_han = re.compile(ur"[^\u4E00-\u9FA5]+") #非汉字过滤正则表达式模型
    sentences = re_not_han.split(line)
    global wordhyp
    for sentence  in sentences:
        if sentence != '' :
            word = []
            for i in range(len(sentence)):#记录每个片段中连续出现字符串，最大长度为5,
                for j in range(1,6):
                    if j+i < len(sentence)+1:
                        word.append(sentence[i:i+j])
            for key in word:
                if wordhyp.has_key(key):
                    wordhyp[key]+=1
                else:
                    wordhyp[key]=1

def wordhyp_reduction():
    global wordhyp
    for word in wordhyp.keys(): #消除频数小于1的词假设
        if wordhyp[word]<=1:
            wordhyp.pop(word)
    wordhyp_list=wordhyp.keys()
    mark = dict.fromkeys(wordhyp_list, True)
    wordhyp_list.sort()
    wordhyp_size = len(wordhyp_list)
    for i in range(wordhyp_size - 1):
        if ((wordhyp[wordhyp_list[i]] == wordhyp[wordhyp_list[i+1]])and(wordhyp_list[i+1].find(wordhyp_list[i])!=-1)):
            mark[wordhyp_list[i]] = False

    for i in range(wordhyp_size):
        wordhyp_list[i] = wordhyp_list[i][::-1]

    wordhyp_list.sort()

    for i in range(wordhyp_size - 1):
#需要对wordhyp_list[i]做一次字符串反转以用作假设词字典wordhyp的索引
        if ((wordhyp[wordhyp_list[i][::-1]] == wordhyp[wordhyp_list[i+1][::-1]])and(wordhyp_list[i+1].find(wordhyp_list[i])!=-1)):
            mark[wordhyp_list[i][::-1]] = False

    for i in range(wordhyp_size):
        wordhyp_list[i] = wordhyp_list[i][::-1]
        if mark[wordhyp_list[i]] == False:
            wordhyp.pop(wordhyp_list[i])

#def wordhyp_reduction():
#    global wordhyp
#    for word in wordhyp.keys():
#        if wordhyp[word]<=1:
#            wordhyp.pop(word)

#    wordhypotheses = wordhyp.keys()
#    mark = dict.fromkeys(wordhypotheses,True)
#    size = len(wordhypotheses)
#    for i in range(size):
#        for j in range(size):
#            if wordhyp[wordhypotheses[j]]==wordhyp[wordhypotheses[i]] and wordhypotheses[j].find(wordhypotheses[i])==True:
#                mark[wordhypotheses[i]]=False

#    for i in range(size):
#       if mark[wordhypotheses[i]] == False:
#            wordhyp.pop(wordhypotheses[i])

def dump():
    global wordhyp
    pprint.pprint(wordhyp.keys(),open("word_hypothese.txt",'wb'))

if __name__=="__main__":
    global wordhyp
    for fname in glob.glob("train_txt/*.txt"):
        print "reading ",fname
        for line in open(fname,"rb"):
            try:
                line = line.decode('utf8')
            except:
                line = line.decode('gbk','ignore')
            line = line.strip().replace(" ","")
            get_word_hypo(line)

    pprint.pprint(wordhyp,open("word_freq.txt",'wb'))#保存未降噪前的假设词和其词频率，求IBV 时用
    wordhyp_reduction()
    dump()
            
