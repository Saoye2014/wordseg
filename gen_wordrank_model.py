#-*- coding:utf-8 -*-
from __future__ import division
import os
import sys
import pprint
import glob
import math
#@param ladj={}
#@param radj={}
#@param wordhyp={}
#wordhyp_ebv=[]
# wordhyp_bv={}
#@return wordrank_value = []

def cal_EBV(wordhyp, ladj, radj, iter_times):
    wordhyp_ebv={}
    wordhyp_bv={}
    

    wordhyp_list = wordhyp.keys()
    for word in wordhyp_list:
        wordhyp_bv[word]={"lbv":1,"rbv":1}
    for i in (range(iter_times+1)):
        for word in wordhyp_list:
            if ladj.has_key(word):  #word有左邻接的词
                sum_rv = 0
                for element in ladj[word]:
                    sum_rv = sum_rv+wordhyp_bv[element]["rbv"]
                wordhyp_bv[word]["lbv"] = sum_rv

        for word in wordhyp_list:
            if radj.has_key(word):
                sum_lv = 0
                for element in radj[word]:  #word有右邻接的词
                    sum_lv = sum_rv + wordhyp_bv[element]["lbv"]
                wordhyp_bv[word]["rbv"] = sum_lv
        
        sum_lv=sum_rv=0
        for word in wordhyp_list:
            sum_lv = sum_lv + wordhyp_bv[word]["lbv"] * wordhyp_bv[word]["lbv"]
            sum_rv = sum_rv + wordhyp_bv[word]["rbv"] * wordhyp_bv[word]["rbv"]

        for word in wordhyp_list:
            wordhyp_bv[word]["lbv"]=wordhyp_bv[word]["lbv"]/math.sqrt(sum_lv)
            wordhyp_bv[word]["rbv"]=wordhyp_bv[word]["rbv"]/math.sqrt(sum_rv)

        for word in wordhyp_list:
            wordhyp_bv[word]["lbv"]=wordhyp_bv[word]["lbv"]/math.sqrt(sum_lv)
            wordhyp_bv[word]["rbv"]=wordhyp_bv[word]["rbv"]/math.sqrt(sum_rv)
    
    for word in wordhyp_list:
        wordhyp_ebv[word]=wordhyp_bv[word]["lbv"]*wordhyp_bv[word]["rbv"]
    return wordhyp_ebv



def cal_IBV(wordhyp, prop_character):
    prop_xy={}
    wordhyps_ibv={}

#    print raw_trainning_text
#    print "ss",raw_xy[1],"ss"
    for word in wordhyp:
        for i in range(len(word)-1):
            xy = word[i:i+2]
            if prop_xy.has_key(xy):
                ibv = (prop_xy[xy]/(prop_character[xy[0]]*prop_character[xy[1]]))
                if ibv ==0:
                    ibv=1
                else :
                    ibv = math.log(ibv,2)
                ibv = math.log((prop_xy[xy]/(prop_character[xy[0]]*prop_character[xy[1]])),2)
            else:
                ibv = math.log(prop_character[xy]/(prop_character[xy[0]]*prop_character[xy[1]]),2)#避免再次查询prop，提高效率？
                prop_xy[xy] = prop_character[xy]#添加key，value对
            if wordhyps_ibv.has_key(word):
                if wordhyps_ibv[word] > ibv:#取假设词字串中MI最小的值
                    wordhyps_ibv[word] = ibv
            else:
                wordhyps_ibv[word]=ibv

    return wordhyps_ibv

def cal_BV(wordhyp,prop_character,raw_trainning_text,ladj, radj, iter_times):
    wordhyps_ebv = cal_EBV(wordhyp,ladj,radj,iter_times)
    wordhyps_ibv = cal_IBV(wordhyp,prop_character,raw_trainning_text)
    
    wordhyp_wrv = {}#WordRank Value
    for word in wordhyp:
        wordhyp_wrv[word] = wordhyp_ebv * math.pow(wordhyp_ibv[wor],4.4) 

    return wordhyp_wrv
#LOT NEED TODO
