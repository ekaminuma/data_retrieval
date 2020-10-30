# coding: utf-8
# Document Frequencyを求める
import os
import sys
import string
import re
import glob
from collections import defaultdict

if __name__=='__main__':
    import argparse
    # コマンドラインオプション
    ap=argparse.ArgumentParser(description="形態素解析結果からDFを求める")
    ap.add_argument('dir',type=str,metavar='DIR',help='text directory')
    ap.add_argument('--content','-c',action='store_true',help='内容語のみ')
    ap.add_argument('--debug','-d',action='store_true',help='for debug')
    args=ap.parse_args()

    files=glob.glob(args.dir+'/*')

    df=defaultdict(int)
    for f in files:
        dfh=open(f,'r')
        word=set() # テキストに出現するかしないかだけ見るので頻度を数えなくてもいい
        for ln in dfh:
            ln=ln.rstrip()
            if ln=='EOS':
                continue
            line=re.split('\t',ln)
            if line[0]=='　':
                continue
            features=re.split(',',line[1])
            if not args.content or re.match('名詞|動詞|形容詞|副詞',features[0]):
                # 原形を用いる．ただし，未知語だった場合は表層を使う
                lemma=features[6]
                if lemma=='*' :
                    lemma=line[0]
                word.add(lemma)
                
        for w in word:
            df[w]+=1
        dfh.close()
    df['##NOD##']=len(files) # テキスト集合に含まれるテキストの数(tfidfの計算に使う)

    srted=sorted(df.keys(),key=lambda x:df[x],reverse=True)
    for s in srted:
        if s=='':
            print(s)
        print(df[s],s,sep='\t')
    
#    print('\n'.join([str(df[x])+'\t'+x for x in sorted(df.keys(),key=lambda k:df[k],reverse=True)]))
