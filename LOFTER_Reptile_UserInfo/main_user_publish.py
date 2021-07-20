import urllib.parse
from random import random
from time import sleep
import pandas as pd
import requests

import parseDWRUtil


def postReqBlogStatNew(publisherid,sleepTime=1.0,tag="表情包",outFile="BlogStatNew.txt"):
    '''
    显示的列表模式为  n行m列   请求方式为POST
    测试Tag为表情包的帖子请求过程中的某一 .dwr文件
    :return:
    '''
    tagUrlCode = urllib.parse.quote(tag)
    url="https://www.lofter.com/dwr/call/plaincall/BlogBean.getBlogStatNew.dwr"
    headers={
        "content-type": "text/plain",
        #"referer": "https://www.lofter.com/tag/{0}/total?tab=archive".format(tagUrlCode)
        "referer": "https://www.lofter.com/tag/%E8%A1%A8%E6%83%85%E5%8C%85/total"
    }
    data="""callCount=1
scriptSessionId=${scriptSessionId}187
httpSessionId=
c0-scriptName=BlogBean
c0-methodName=getBlogStatNew
c0-id=0
c0-param0=number:"""+publisherid+\
    """
batchId=599819"""
    sleep(sleepTime * random())
    response = requests.post(url=url, data=data, headers=headers)
    file = open(outFile, "w", encoding="utf-8")
    file.write(response.text)
    file.close()
    response.close()

def getPageUrlRaw():
    df=pd.read_csv("./allUserInfo.csv")
    uidList=df['uid']
    for i in range(0,len(uidList)):
        uid=uidList[i]
        print(uid)
        postReqBlogStatNew(str(uid),tag="表情包",outFile="ResembleBlog.txt",sleepTime=0.05)
        parseDWRUtil.parseMultiAttr(['.blogName'],input_path="ResembleBlog.txt",output_file="ResembleBlogPageUrl.txt", flag=1,endChr='')
        with open("ResembleBlogPageUrl.txt",'a') as file:
            file.write(','+str(uid)+'\n')

def parseRawPageUrl(RawPageUrlFile,outputFile):
    blogname_uidList=[]
    with open(RawPageUrlFile,'r') as file:
        lines=file.readlines()
        for line in lines:
            line=line.strip()
            line = line.replace(",", "")
            blogname_uid = line.split('"')
            if (len(blogname_uid) >= 3 and blogname_uid[0][:2] == 's0'):
                '''
                len(blogname_uid)>=3：s0.blogName="ziyuelinxi"s3.blogName="todyhu"s4.blogName="historicalpics",509212280
                经验证，取s0.blogName。保险起见，增加blogname_uid[0][:2]=='s0'保证爬取的数据中一定取得s0.blogName
                '''
                blogname = blogname_uid[1]
                uid = blogname_uid[-1]
                blogname_uidStr="{0},{1}\n".format(blogname,uid)
                blogname_uidList.append(blogname_uidStr)
    blogname_uidList=list(set(blogname_uidList))
    with open(outputFile,'w') as file:
        for blogname_uid in blogname_uidList:
            file.write(blogname_uid)

#parseRawPageUrl('./ResembleBlogPageUrl.txt',"./ResembleBlogPageUrlPar.txt")

