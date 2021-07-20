import os
import re
from time import sleep

import pandas as pd
from bs4 import BeautifulSoup
import requests

hd = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36',
    "content-type": "text/plain",
    'Referer': 'https://www.lofter.com/'
}

def getUrl_Raw():
    input2 = open("ResembleBlogPageUrlPar.txt", "r", encoding="utf-8")
    lines=input2.readlines()
    input2.close()


    with open("getUrlTask",'r') as file:
        beginIdx=int(file.readlines()[-1].strip())

    for i in range(beginIdx,len(lines)):
        line=lines[i].strip()
        blogName,uid = line.split(',')
        urls = open("./usr-urls/" + uid + ".txt", "w", encoding="utf-8")
        base = "https://" + blogName + ".lofter.com/"
        url = base
        print("{0},{1}".format(blogName,uid))

        maxPostNum=100
        postCnt=0
        while postCnt<maxPostNum:
            postCnt+=1
            response = requests.get(url, hd)
            print("response.content[:], {0}".format(response.content[:min(50,len(response.content))]))
            bs = BeautifulSoup(response.content, "html.parser")

            #post href 匹配
            hrefRegxStr="^https://{0}\.lofter\.com/post/{1}_".format(blogName,str(hex(int(uid)))[2:])
            tmp = bs.find_all(href=re.compile(hrefRegxStr))
            postUrlList=[]
            #为了避免postUrl重复，可以将这里的postUrlList向上移动，做一次大写入，而不是现在的一个帖子一次写入
            for i in range(0, len(tmp)):
                postUrlList.append(str(tmp[i]['href']))
            postUrlList=list(set(postUrlList))
            for posturl in postUrlList:
                urls.write(posturl+'\n')
            #翻页
            nex = bs.find_all("a", attrs={"class": "next"})
            try:
                if len(nex) == 0:
                    postCnt=maxPostNum
                else:
                    print(nex)
                    url = base + nex[0]['href']
            except Exception as e:
                print(e)

        urls.close()
        sleep(0.1)
        #频繁且快速的对同一文件写入，会发生大量的写入错误
        #猜测python的write是非阻塞的，因而该处代码存在一些问题，现行代码不能完成断点恢复（因为不能保证断点正确写入文件中 需要人工干预）
        with open("getUrlTask", 'a') as file:
            file.write(str(i)+"\n")

'''
最新测试，似乎得到的用户PostUrl会有较多的重复，但确实全部属于对应用户，因而正确性可以得到保证。
可行的一种方式是后处理url文件，即在上面的程序之后，添加一段文件内url去重的程序。
'''

def processRawUrlFile(inputFile):
    with open(inputFile,'r',encoding='utf-8') as file:
        lines=file.readlines()
    lines=list(set(lines))
    with open('tmp','w') as file:
        for line in lines:
            file.write(line)
    os.remove(inputFile)
    os.rename('tmp', inputFile)

def processAllRawUrlFile():
    path = './usr-urls/'
    urlFileList=os.listdir(path)
    for urlFile in urlFileList:
        urlFilePath=path+urlFile
        try:
            processRawUrlFile(urlFilePath)
        except Exception as e:
            print("err File: {0}".format(urlFilePath))


