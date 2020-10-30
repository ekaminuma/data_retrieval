# coding: utf-8

import os
import sys
#sys.path.append(os.environ['HOME']+'/lib/python3')
import string
import re
from collections import defaultdict

if __name__=='__main__':
    import argparse
    # コマンドラインオプション
    ap=argparse.ArgumentParser(description="形態素の共起を求める")
    ap.add_argument('file',type=open,metavar='RES',help='形態素解析結果')
    ap.add_argument('--content','-c',action='store_true',help='内容語のみ')
    ap.add_argument('--debug','-d',action='store_true',help='for debug')
    args=ap.parse_args()

    freq=defaultdict(int)
    morphs=[]
    for ln in args.file:
        ln=ln.rstrip()
        if ln=='EOS':
            # 文内での共起を見る
            morphs=sorted(morphs)
            for i in range(len(morphs)-1):
                for j in range(i+1,len(morphs)):
                    freq[morphs[i]+'\t'+morphs[j]]+=1
            morphs=[]
        else:
            line=re.split('\t',ln)
            features=re.split(',',line[1])
            lemma=features[6]
            if lemma=='*':
                lemma=line[0]
            if not args.content or re.match('名詞|動詞|形容詞|副詞',features[0]):
                morphs.append(lemma)

    srted=sorted(freq.keys(),key=lambda x:freq[x],reverse=True)
    for s in srted:
        print(freq[s],s,sep='\t')
