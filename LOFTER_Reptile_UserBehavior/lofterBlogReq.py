import urllib
import urllib.parse
from random import random
from time import sleep

import requests

def getReqTest(tag):
    '''
    测试乐乎网站对于某一tag的请求，获取返回的页面内容，写入到"lofterTest.txt"文件中。给开发者提供一个直观的感受
    :param tag: 待请求的tag
    :return:
    '''
    #显示的列表模式为  n行1列   请求方式为GET
    tagUrlCode=urllib.parse.quote(tag)
    response=requests.get("https://www.lofter.com/tag/{0}".format(tagUrlCode))
    print(tagUrlCode)
    file=open("lofterTest.txt","w",encoding="utf-8")
    file.write(response.text)
    file.close()
    response.close()

def postReq(blogNum,lastIdx,sleepTime=0.5,tag="表情包"):
    '''
    显示的列表模式为  n行m列   请求方式为POST
    测试Tag为表情包的帖子请求过程中的某一 .dwr文件
    :return: 
    '''
    tagUrlCode = urllib.parse.quote(tag)
    url="https://www.lofter.com/dwr/call/plaincall/TagBean.search.dwr"
    headers={
        "content-type": "text/plain",
        "referer":"https://www.lofter.com/tag/{0}/total?tab=archive".format(tagUrlCode)
    }
    data="""callCount=1
scriptSessionId=${scriptSessionId}187
httpSessionId=
c0-scriptName=TagBean
c0-methodName=search
c0-id=0
c0-param0=string:"""+tagUrlCode+\
    """
c0-param1=number:0
c0-param2=string:
c0-param3=string:total
c0-param4=boolean:false
c0-param5=number:1282300337
c0-param6=number:"""+str(blogNum)+\
    """
c0-param7=number:"""+str(lastIdx)+\
    """
c0-param8=number:0
batchId=113546
    """
    sleep(sleepTime*random())
    response = requests.post(url=url,data=data,headers=headers)
    file = open("lofterPost.txt", "a", encoding="utf-8")
    file.write(response.text)
    file.close()
    response.close()

def postReqNum(num,step=5,tag="表情包"):
    '''
    num: 请求的帖子总数
    step：步长
    :param num:
    :return:
    '''
    import numpy as np
    lastIdxArray=np.arange(0,num,step=step)
    print(lastIdxArray)
    for lastIdx in lastIdxArray:
        print(lastIdx," ",step)
        postReq(lastIdx=lastIdx,blogNum=step,tag=tag)

#getReqTest("表情包")
#postReqNum(3000,step=50,tag='原神')