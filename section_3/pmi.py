# coding: utf-8

import os
import sys
#sys.path.append(os.environ['HOME']+'/lib/python3')
import string
import re
from collections import defaultdict
from math import log2

if __name__=='__main__':
    import argparse
    # コマンドラインオプション
    ap=argparse.ArgumentParser(description="形態素の共起のPMIを求める")
    ap.add_argument('file',type=open,metavar='RES',help='形態素解析結果')
    ap.add_argument('--content','-c',action='store_true',help='内容語のみ')
    ap.add_argument('--debug','-d',action='store_true',help='for debug')
    args=ap.parse_args()

    freq=defaultdict(int)
    cooccur=defaultdict(lambda:defaultdict(int))
    total=0
    morphs=[]
    for ln in args.file:
        ln=ln.rstrip()
        if ln=='EOS':
            # 文内での共起を見る
            morphs=sorted(morphs)
            # 単独の出現
            for m in morphs:
                freq[m]+=1
                total+=1
            # 共起ペア
            for i in range(len(morphs)-1):
                for j in range(i+1,len(morphs)):
                    cooccur[morphs[i]][morphs[j]]+=1
            morphs=[]
        else:
            line=re.split('\t',ln)
            features=re.split(',',line[1])
            lemma=features[6]
            if lemma=='*':
                lemma=line[0]
            if not args.content or re.match('名詞|動詞|形容詞|副詞',features[0]):
                morphs.append(lemma)

    # PMIの計算
    pmi=defaultdict(float)
    for k in cooccur:
        for l in cooccur[k]:
            pmi[k+'\t'+l]=log2((total*cooccur[k][l])/(freq[k]*freq[l]))


                
    srted=sorted(pmi.keys(),key=lambda x:pmi[x],reverse=True)
    for s in srted:
        print(pmi[s],s,sep='\t')
