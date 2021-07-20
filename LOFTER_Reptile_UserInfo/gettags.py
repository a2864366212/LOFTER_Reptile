import re

import pandas as pd
from bs4 import BeautifulSoup
import json
import requests


hd = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36',
    "content-type": "text/plain",
    'Referer': 'https://www.lofter.com/'
}

uidList=[]
with open("ResembleBlogPageUrlPar.txt") as file:
    lines=file.readlines()
    for line in lines:
        blogname_uid = line.strip()
        _,uid=blogname_uid.split(',')
        uidList.append(uid)


with open("getTagsUidIdx",'r') as file:
    beginIdx=int(file.readlines()[-1].strip())
    print("beginIdx:",beginIdx)

for i in range(beginIdx,len(uidList)):
    uid=uidList[i]
    print("{0} uid: {1}".format(i,uid))
    try:
        nein = open("./usr-urls/" + str(uid) + ".txt", "r", encoding="utf-8")
        line = nein.readline()
    except Exception as e:
        continue
    tot = 0
    a = dict()
    while line:
        ss = line.strip()
        if(len(ss)==0):break
        response = requests.get(ss, hd)
        bs = BeautifulSoup(response.content, "html.parser")

        tagsDiv = bs.find_all(attrs={"class":{"tag","tags"}})
        tags=[]
        print(tagsDiv)
        for tagDiv in tagsDiv:
            try:
                #tmpTag = tagDiv.text.split('\n')
                tmpTag=re.split('[\n#●\s]', tagDiv.text)
                for i in tmpTag:
                    if(i != ''):tags.append(i)
            except Exception as e:
                print(e)
        tags=list(set(tags))
        print(tags)
        tot += len(tags)
        for tag in tags:
            name = tag
            if a.get(name):
                a[name] += 1
            else:
                a[name] = 1
            # print(name)
        line = nein.readline()
    if(len(a.keys())>0):
        outs = "{\"uid\":" + str(uid) + ",\"tagcnt\":" + str(tot) + ",\"tags\":" + json.dumps(a, ensure_ascii=False) + "}"
        with open("out.txt", "a", encoding="utf-8") as outfile:
            outfile.write(outs + "\n")
        print(outs)
    with open("getTagsUidIdx", 'a') as file:
        file.write(str(i)+'\n')

