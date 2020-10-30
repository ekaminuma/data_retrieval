# coding: utf-8
# 形態素の頻度を数える
import os
import sys
import string
import re
from collections import defaultdict

if __name__=='__main__':
    import argparse
    # コマンドラインオプション
    ap=argparse.ArgumentParser(description="形態素の頻度を数える")
    ap.add_argument('file',type=open,metavar='RES',help='形態素解析結果')
    ap.add_argument('--content','-c',action='store_true',help='内容語のみ')
    ap.add_argument('--debug','-d',action='store_true',help='for debug')
    args=ap.parse_args()

    freq=defaultdict(int) # 集計結果を格納する

    for ln in args.file:
        ln=ln.rstrip()
        if ln=='EOS':
            continue
        # 形態素解析結果をparseする
        line=re.split('\t',ln)
        features=re.split(',',line[1])

        # 表層を数える
        if not args.content or re.match('名詞|動詞|形容詞|副詞',features[0]):
            freq[line[0]]+=1

    # freqのkey(表層)をvalue(出現頻度)の逆順(多い順)で並び替える
    srted=sorted(freq.keys(),key=lambda x:freq[x],reverse=True)

    # 表示
    for s in srted:
        print(freq[s],s,sep='\t')
