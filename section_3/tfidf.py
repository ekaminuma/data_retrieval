# coding: utf-8

import os
import sys
import string
import re
from collections import defaultdict
from math import log2

if __name__=='__main__':
    import argparse
    # コマンドラインオプション
    ap=argparse.ArgumentParser(description="TFIDFの計算")
    ap.add_argument('dffile',type=open,metavar='DF',help='df file')
    ap.add_argument('file',type=open,metavar='RES',help='形態素解析結果')
    ap.add_argument('--content','-c',action='store_true',help='内容語のみ')
    ap.add_argument('--debug','-d',action='store_true',help='for debug')
    args=ap.parse_args()

    # dfの読み込み (<freq>\t<word>)
    # ##NOD##はテキスト数
    df=defaultdict(int)
    for ln in args.dffile:
        ln=ln.rstrip()
        line=re.split('\t',ln)
        df[line[1]]=int(line[0])

    # tfの計算
    # tf(w)=n_w/単語数
    tf=defaultdict(float) # 後で割合を求めるので
    number_of_word=0
    for ln in args.file:
        ln=ln.rstrip()
        if ln=='EOS':
            continue
        line=re.split('\t',ln)
        if line[0]=='　':
            continue
        features=re.split(',',line[1])
        lemma=features[6]
        if lemma=='*':
            lemma=line[0]
        if not args.content or re.match('名詞|動詞|形容詞|副詞',features[0]):
            tf[lemma]+=1
            number_of_word+=1
                
    # tfidfの計算
    tfidf=defaultdict(float)
    if args.debug:
        print('number of words :',number_of_word)
        print('word','tf','df',sep='\t')
    for w in tf:
        if args.debug:
            print(w,tf[w],df[w],sep='\t')
        tfidf[w]=(tf[w]/number_of_word)*(log2(df['##NOD##']/df[w])+1)

    srted=sorted(tfidf.keys(),key=lambda x:tfidf[x],reverse=True)
    for s in srted:
        print(tfidf[s],s,sep='\t')
