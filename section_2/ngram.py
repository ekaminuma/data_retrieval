# coding: utf-8

import os
import sys
import string
import re
from collections import defaultdict

if __name__=='__main__':
    import argparse
    # コマンドラインオプション
    ap=argparse.ArgumentParser(description="Ngram")
    ap.add_argument('file',type=open,metavar='RES',help='形態素解析結果')
    ap.add_argument('--n','-n',type=int,metavar='INT',help='N-gram (default=3)',default=3)
    ap.add_argument('--type','-t',choices=['word','char'],help='element type (default=word)',default='word')
    ap.add_argument('--debug','-d',action='store_true',help='for debug')
    args=ap.parse_args()

    freq=defaultdict(int)
    sentence=[]
    for ln in args.file:
        ln=ln.rstrip()
        if ln=='EOS':
            # 文単位でn-gramを考える
            sentence.insert(0,'<s>') # 文頭マーカを挿入
            sentence.append('</s>') # 文末マーカを挿入
            if len(sentence)>=args.n:
                for i in range(args.n-1,len(sentence)):
                    temp=[]
                    for j in range(i-args.n+1,i+1):
                        temp.append(sentence[j])
                    freq['|'.join(temp)]+=1
            sentence=[]
            continue
        line=re.split('\t',ln)
        if args.type=='word':
            sentence.append(line[0])
        elif args.type=='char':
            sentence+=list(line[0])

    # freqのkey(表層)をvalue(出現頻度)の逆順(多い順)で並び替える
    srted=sorted(freq.keys(),key=lambda x:freq[x],reverse=True)

    # 表示
    for s in srted:
        print(freq[s],s,sep='\t')
