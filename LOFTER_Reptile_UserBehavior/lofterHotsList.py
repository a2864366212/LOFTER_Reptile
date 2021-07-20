import os
import urllib
import urllib.parse
from random import random
from time import sleep

import numpy as np
import requests
rootPath='./PostHots/'

def postReqHotsList(rootPath,postid,blogid,blogNum,lastIdx,sleepTime=4,debugMode=False,tag="表情包"):
    '''
    获取某一帖子的热度（其实是其他用户的收藏、转发、点赞行为）列表
    :return:
    '''
    tagUrlCode = urllib.parse.quote(tag)
    url="https://www.lofter.com/dwr/call/plaincall/PostBean.getPostHots.dwr"
    headers={
        "content-type": "text/plain",
        "referer":"https://www.lofter.com/tag/{0}/total".format(tagUrlCode)
    }
    data="""callCount=1
scriptSessionId=${scriptSessionId}187
httpSessionId=
c0-scriptName=PostBean
c0-methodName=getPostHots
c0-id=0
c0-param0=number:"""+str(postid)+\
"""
c0-param1=number:"""+str(blogid)+\
"""
c0-param2=number:"""+str(blogNum)+\
"""
c0-param3=number:"""+str(lastIdx)+\
"""
batchId=246855"""
    if debugMode:
        print(data)
    else:
        if not os.path.isfile(rootPath+"lofterPostHots_{0}_{1}.txt".format(blogid,postid)):
            sleep(sleepTime * random())
            response = requests.post(url=url, data=data, headers=headers)
            if debugMode: print(response.text)
            file = open(rootPath+"lofterPostHots_{0}_{1}.txt".format(blogid,postid), "a", encoding="utf-8")
            file.write(response.text)
            file.close()
            response.close()

def reqDWRfileOfHots(rootPath,targetBlogUrlsFile="blogPageUrl.txt",blogNum=1500,step=100,tag="表情包",sleepTime=1):

    '''
    目标帖子地址的格式
    https://mao20260.lofter.com/post/1e8a1f76_1cb2541fb
    1e8a1f76:512368502  blogid
    1cb2541fb:7703183867    postid
    '''
    with open(targetBlogUrlsFile,"r") as file:
        cnt=0
        while True:
            line=file.readline().strip().split('="')[-1].strip('"')
            url=line
            if url:
                print("targetBlogUrlsFile cnt: ", cnt)
                cnt+=1
                blogid_postid = url[url.rindex("/")+1:].split('_')
                blogid,postid=blogid_postid
                print(blogid,postid)
                print(int(blogid,16), int(postid,16))

                lastIdxArray=np.arange(0,blogNum,step=step)
                for lastIdx in lastIdxArray:
                    print("reqDWRfileOfHots(): now the lastIdx: {0}".format(lastIdx))
                    try:
                        postReqHotsList(rootPath=rootPath,postid=int(postid,16), blogid=int(blogid,16), lastIdx=lastIdx, blogNum=step,
                                        debugMode=False,tag=tag,sleepTime=sleepTime)
                    except Exception as e:
                        print("reqDWRfileOfHots() error",":",e)
            else:
                print("cnt: ",cnt)
                break
        #postReqHotsList(postid=7703183867,blogid=512368502,lastIdx=0,blogNum=10,debugMode=True)
#reqDWRfileOfHots(tag="原神")
