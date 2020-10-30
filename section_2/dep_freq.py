# coding: utf-8
# 係り受け対の頻度
import os
import sys
import string
import re
from collections import defaultdict

if __name__=='__main__':
    import argparse
    # コマンドラインオプション
    ap=argparse.ArgumentParser(description="係り受け対の頻度")
    ap.add_argument('file',type=open,metavar='RES',help='係り受け解析の結果')
    ap.add_argument('--debug','-d',action='store_true',help='for debug')
    args=ap.parse_args()

    freq=defaultdict(int)
    chunk=defaultdict(str) # 文節の表層を保存
    pair=defaultdict(int) # 係り関係
    cid=-1
    for ln in args.file:
        ln=ln.rstrip()
        if ln=='EOS':
            # 対を作る
            for c in pair:
                freq[chunk[c]+'\t'+chunk[pair[c]]]+=1
            chunk=defaultdict(str)
            pair=defaultdict(int)
        elif re.match('\* ',ln):
            mat=re.match('\* (.*?) (.*?)D (.*?)/(.*?) ',ln)
            cid=int(mat.group(1))
            if mat.group(2)!='-1':
                pair[cid]=int(mat.group(2))
        else:
            line=re.split('\t',ln)
            chunk[cid]+=line[0]

    # freqのkey(表層)をvalue(出現頻度)の逆順(多い順)で並び替える
    srted=sorted(freq.keys(),key=lambda x:freq[x],reverse=True)

    # 表示
    for s in srted:
        print(freq[s],s,sep='\t')
