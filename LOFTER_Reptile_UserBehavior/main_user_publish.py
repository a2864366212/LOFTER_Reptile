import urllib.parse
from random import random
from time import sleep

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
        "referer": "https://www.lofter.com/tag/{0}/total?tab=archive".format(tagUrlCode)

    }
    data="""callCount=1
scriptSessionId=${scriptSessionId}187
httpSessionId=
c0-scriptName=BlogBean
c0-methodName=getBlogStatNew
c0-id=0 
c0-param0=number:"""+publisherid+\
    """
batchId=113546
    """
    sleep(sleepTime * random())
    response = requests.post(url=url, data=data, headers=headers)
    file = open(outFile, "w", encoding="utf-8")
    file.write(response.text)
    file.close()
    response.close()


postReqBlogStatNew("839522389",tag="表情包",outFile="ResembleBlog.txt",sleepTime=0.5)
parseDWRUtil.parseMultiAttr(['.blogName'],input_path="ResembleBlog.txt",output_file="ResembleBlogPageUrl.txt", flag=0)


