import shutil

import  lofterBlogReq
import lofterHotsList
import lofterParseHotsDWR
import uploadDataToDb
import parseDWRUtil
import os, sys
import pandas as pd

sleepTime=0
targetBlogUrlsFile="blogPageUrl.txt"
lofterPost="lofterPost.txt"
PostHots="./PostHots/"
PostHotsResult="./PostHotsResult/"
TagsFile="./EmojiTag.txt"
def initFile():
    '''
    删除一些临时文件
    :return:
    '''

    try:
        os.remove(lofterPost)
    except Exception as e: print(e)
    try:
        os.remove(targetBlogUrlsFile)
    except Exception as e: print(e)
    try:
        shutil.rmtree(PostHots)
    except Exception as e: print(e)
    try:
        os.mkdir(PostHots)
    except Exception as e:print(e)

def getUserInfoJsonByTag(tag):

    initFile()

    '''请求目标Tag的帖子展示列表'''
    lofterBlogReq.postReqNum(num=1500, step=100, tag=tag)

    '''
    解析结果，获取各个帖子的Url（实际属性名为blogPageUrl） "lofterPost.txt" ==> "blogPageUrl.txt"
    目前的实现是调用parseDWR.cpp
    call  parseMultiAttr() of parseDWR.cpp
    最新的实现已经采用python实现 在parseDWRUtil.py中'''
    parseDWRUtil.parseMultiAttr(parseDWRUtil.oneAttr,input_path="./lofterPost.txt",output_file="blogPageUrl.txt", flag=0)

    '''请求blogPageUrl中的各Url,获取帖子对应的热度列表（用户反馈、帖子信息）'''
    lofterHotsList.reqDWRfileOfHots(rootPath="./PostHots/",targetBlogUrlsFile=targetBlogUrlsFile,blogNum=10000, step=100, tag=tag,sleepTime=sleepTime)


    '''统计PostHots文件夹下文件名，写入到 dirInfo.txt 中'''
    lofterParseHotsDWR.genDirFileInfo(rootPath="./PostHots/",listFile="dirInfo.txt")


    '''解析原始的DWR文件
    目前的实现是调用parseDWR.cpp
    最新的实现已经采用python实现 在parseDWRUtil.py中
    call  read_dir() of parseDWR.cpp'''
    parseDWRUtil.parseDWRFilesOfDir(rootPath="./PostHots/",dirInfoFilepath="./PostHots/dirInfo.txt",
                                    attrList=parseDWRUtil.attrList, flag=1)


    '''解析处理后的DWR文件，获取用户-标签数据'''
    try:
        lofterParseHotsDWR.getAllUserBehaviorLog()
    except Exception as e:
        print(e)
    # uploadDataToDb.readJsonData(filePath='./PostHotsResult/allUserBehaviorLogJson.txt',outPutFilePath='./PostHotsResult/allUserBehaviorLog.csv',needToSave=True)
    # uploadDataToDb.getTagList(inputFile='./PostHotsResult/allUserBehaviorLog.csv',needToSave=True)
    # lofterParseHotsDWR.unicodeToChineseFile(inputFile="./PostHotsResult/EmojiTags.csv",outputFile="./PostHotsResult/EmojiSITTags.txt")
    # uploadDataToDb.calTagsFreq(needToSave=True)

def getTagList(TagsFile):
    tagsList=[]
    with open(TagsFile,'r',encoding='utf-8') as file:
        lines=file.readlines()
        for line in lines:
            line=line.strip()
            tags=line.split(',')
            for tag in tags:
                tag=tag.replace(" ", "")
                tag="".join(tag.split())
                if len(tag)>0:tagsList.append(tag)
    return list(set(tagsList))

# tagsReq=getTagList(TagsFile)
# with open("tagsReq.txt",'w',encoding='utf-8') as file:
#     for tags in tagsReq:
#         file.write(tags+'\n')
#

def autoGetTagListInfo():
    #0~1000 Tag
    endTagsIdx=1000

    with open("tagsReqResult.txt",'r',encoding='utf-8') as file:
        #checkPoint 从断点继续
        begin=file.readline().strip()
        begin=int(begin)
    with open("tagsReq.txt",'r',encoding='utf-8') as file:
        tags=file.readlines()
        for i in range(begin,len(tags)):
            if(i>endTagsIdx):break
            tag=tags[i]
            tag=tag.strip()
            print("tag: {0}".format(tag))
            getUserInfoJsonByTag(tag)
            with open("tagsReqResult.txt",'w',encoding='utf-8') as res:
                res.write(str(i))

# getUserInfoJsonByTag("表情包")
# uploadDataToDb.readJsonData(filePath='./PostHotsResult/allUserBehaviorLogJson.txt',outPutFilePath='./PostHotsResult/allUserBehaviorLog.csv',needToSave=True)
# uploadDataToDb.getTagList(inputFile='./PostHotsResult/allUserBehaviorLog.csv',needToSave=True)
# lofterParseHotsDWR.unicodeToChineseFile(inputFile="./PostHotsResult/EmojiTags.csv",outputFile="./PostHotsResult/EmojiSITTags.txt")
# uploadDataToDb.calTagsFreq(needToSave=True)


