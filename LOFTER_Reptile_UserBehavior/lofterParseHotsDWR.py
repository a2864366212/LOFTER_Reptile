import ast
import json
import re


import emoji
import execjs
import js2py


def parseHotsDWR(DWR_FilePath):
    '''
        期望的目标结果数据
    1. 评论用户的行为和用户信息
        1.1. 用户信息：<用户id，用户昵称，用户头像，用户性别，用户注册时间？，用户生日>
        1.2. 用户行为：<用户id，行为类型，反馈的图片ID，行为发生时间>
    2. 图片-标签信息
        2.1. 图片 <图片Url Array>
        2.2. 标签 <标签 Array>
    3. DWR 属性含义解析
        3.1.用户id: s_{i}.publisherUserId
        3.2.用户昵称: s_{i}.blogNickName
        3.3.用户头像: s_{i}.bigAvaImg（还有一个smallAvaImg，但几乎都是null）
        3.4.用户性别: s_{i}.gendar 已知的取值为[1,2,3]，可能是[男，女，未知]
        3.5.用户注册时间: 猜测为 s_{i}.blogCreateTime  ，但不确定
        3.6.用户生日: s_{i}.birthday 该属性对应用户生日（时间戳 ms 表示），可能为空（为空的话值为0）
        3.7.行为类型: s_{i}.type 该属性为提供反馈的用户行为类型，猜测为 type=1代表"喜欢"；type=3代表"推荐"
        3.8.反馈的图片: s_{i}.photoLinks 该属性为帖子的图片地址列表，在整个DWR文件中只有一个（有效）
        3.9.行为发生时间: s_{i}.title  解码后 显示格式为  "用户昵称-数小时前"，该相对时间数值计算行为发生时间
        3.10.图片标签列表： s_{i}.tag 该属性对应帖子图片所打上的Tags，整个文件唯一（有效）

        3.11. 帖子的创建时间：s_{i}.createTime
    :param DWR_FilePath:
    :return:
    '''
    with open(DWR_FilePath,"r") as file:
        pass


import os
def listdir(path, list_name,exceptFile):  # 传入存储的list
    for file in os.listdir(path):
        file_path = os.path.join(path, file)
        if os.path.isdir(file_path):
            listdir(file_path, list_name,exceptFile)
        else:
            if(file_path != exceptFile):
                list_name.append(file_path)
def genDirFileInfo(rootPath="./PostHots/",listFile="dirInfo.txt"):
    fileList=[]
    listFile=rootPath+listFile
    listdir(rootPath,fileList,listFile)
    with open(listFile,'w') as file:
        for fileName in fileList:
            if fileName!=listFile:file.write(fileName+'\n')
#genDirFileInfo()

def unicodeToChineseStr(text):
    #去除emoji 对应的unicode编码
    # 过滤表情
    return text.encode('utf-8', 'replace').decode('unicode_escape')

def unicodeToChineseFile(inputFile,outputFile):
    processedTextArr=[]
    with open(inputFile,'r') as file:
        lines = file.readlines()
        for line in lines:
            line=line.strip()
            if line:
                try:
                    processedTextArr.append(unicodeToChineseStr(line))
                except:
                    #简单丢弃
                    pass
    with open(outputFile,'w',encoding='utf-8') as file:
        for text in processedTextArr:
            try:
                file.write(text+'\n')
            except:
                # 简单丢弃
                pass


import html


def unicodeToChineseStrByJson(jsFilePath,text):
    #读取js文件
    pass
    jsCode=""
    with open(jsFilePath,'r',encoding='utf-8') as file:
        jsCode=file.read()
        print(jsCode)
    context = js2py.EvalJs()
    context.execute(jsCode)
    return context.unicode2Chinese(text)



#text="s27 blogNickName '\u9732\u897F\u4E9A\u662F\u5C0F\u5929\u4F7F\uD83C\uDDF7\uD83C\uDDFA\u2764\uFE0F\uD83C\uDDE8\uD83C\uDDF3'"
#text="s27 blogNickName '\u9732\u897F\u4E9A\u662F\u5C0F\u5929\u4F7F'"
#print(unicodeToChineseStrByJson("unicode2ChineseJSUtil.js",text))

#text="s27 blogNickName '\u9732\u897F\u4E9A\u662F\u5C0F\u5929\u4F7F\uD83C\uDDF7\uD83C\uDDFA\u2764\uFE0F\uD83C\uDDE8\uD83C\uDDF3'"
#print("s27 blogNickName '露西亚是小天使🇷🇺❤️🇨🇳'")


def process_Si_Attr_Val(filePath,debugEncodeMode=True):
    '''
    处理单行文本为 s{i}.attr="value"  形式的数据文件
    处理后格式为： s{i} attr "value"  空格分隔
    :return:
    '''
    new_list = []
    with open(filePath,encoding='utf-8') as f:
        contents = f.readlines()
        for line in contents:
            if '\n' in line and len(line) == 1:#消除空行
                line = line.replace('\n', '')
            # s{i}.attr="value"   ==>  s{i} attr value
            line = line.replace('.', ' ',1)  # '.' ==> ' '
            line = line.replace('=', ' ',1)  # '=' ==> ' '
            line = line.replace('"', '\'')  # '"' ==> '''
            #处理后格式为：  s{i} attr "value"或者 value
            #unicode编码转中文字符
            print(line)
            new_list.append(line)
    if not debugEncodeMode:
        with open('tmp.txt', 'a',encoding='utf-8') as f:
            f.writelines(new_list)
        os.remove(filePath)
        os.rename('tmp.txt', filePath)
def process_Si_Attr_Val_AllFileOfDir(rootPath="./PostHots/",dirInfoFilePath="Si_Attr_Val_FileInfo.txt"):
    with open(rootPath+dirInfoFilePath) as Si_Attr_Val_FileInfo:
        while True:
            Si_Attr_Val_FilePath=Si_Attr_Val_FileInfo.readline()
            Si_Attr_Val_FilePath =Si_Attr_Val_FilePath.strip()
            if len(Si_Attr_Val_FilePath)>0:
                process_Si_Attr_Val(Si_Attr_Val_FilePath)
            else:
                break
def parseUnicode(filePath):
    with open(filePath) as file:
        lineList=[]
        while True:
            line = file.readline()
            line = line.strip().split()
            if(len(line)==0):
                print(lineList)
                break
            line=line[-1]
            line=unicodeToChineseStr(line)
            lineList.append(line)

def Si_Attr_Val2DictAndGetUrl(filePath,debugEncodeMode=True,needGetUrl=False):
    '''
    将filePath文件  中的   s{i}.attr="value"  数据转化为 map对象
    :param filePath:
    :param debugEncodeMode:
    :return: dict()  dict_si[i][attr]=value
    '''
    Si=dict()
    with open(filePath) as f:
        while True:
            line=f.readline().strip()
            if(len(line)==0):break
            if debugEncodeMode:print(line)
            firstSplitIdx=line.index('.')
            try:
                secondSplitIdx=line.index('=')
            except:
                continue
            si_idx=line[:firstSplitIdx]
            si_attr=line[firstSplitIdx+1:secondSplitIdx]
            si_val=line[secondSplitIdx+1:]

            if debugEncodeMode:print("si_idx:{0} si_attr:{1} si_val:{2}".format(si_idx,si_attr,si_val))

            if si_idx not in Si.keys():
                Si[si_idx]=dict()
            if si_attr not in Si[si_idx].keys():
                Si[si_idx][si_attr]=si_val
            else:
                Si[si_idx][si_attr] = si_val
        lofterPicUrlList=[]
        for si in Si.keys():
            for attr in Si[si].keys():
                #解析图片的Url 并放在 lofterPicUrls.txt 中
                if needGetUrl and  attr == 'photoLinks':
                    Si[si][attr]=json.loads(ast.literal_eval(Si[si][attr]))
                    for ele in Si[si][attr]:
                        #遍历  photoLinks 的 value
                        #四个质量等级的图片：[raw,small,middle,orign]:link
                        for k in ele.keys():
                            if(isinstance(ele[k],str) and len(ele[k])>=4 and ele[k][:4]=="http")\
                                    and k=='raw':lofterPicUrlList.append("{0}\n".format(ele[k]))
        if needGetUrl:
            lofterPicUrlList=list(set(lofterPicUrlList))
            with open('./PostHots/lofterPicUrls.txt', 'a',encoding='utf-8') as f:
                f.writelines(lofterPicUrlList)
    return Si
def getAllUrls():
    with open("./PostHots/dirInfo_Parhot.txt") as file:
        while True:
            line=file.readline().strip()
            if(len(line)==0):break
            filePath=line
            Si_Attr_Val2DictAndGetUrl(filePath=filePath,debugEncodeMode=False,needGetUrl=True)


def getAllUserInfo(dirInfo_ParhotFilePath="./PostHots/dirInfo_Parhot.txt",
                   outFile='./PostHotsResult/allUserInfo.txt',
                   outJsonFile='./PostHotsResult/allUserInfoJson.txt'):
    allUserInfo=[]
    with open(dirInfo_ParhotFilePath) as file:
        while True:
            line=file.readline().strip()
            if(len(line)==0):break
            filePath=line
            usersInfo = dict()  # (uid,userInfo)
            Si_Attr_Val=Si_Attr_Val2DictAndGetUrl(filePath=filePath,debugEncodeMode=False)
            for user in Si_Attr_Val.keys():
                if 'publisherUserId' in Si_Attr_Val[user].keys():
                    #print("publisherMainBlogInfo: {0}".format(Si_Attr_Val[user]['publisherMainBlogInfo']))
                #if 'blogNickName' not in usersTmp[user].keys(): continue
                    publisherUserId=Si_Attr_Val[user]['publisherUserId']
                    if  publisherUserId not in usersInfo.keys(): usersInfo[publisherUserId] = dict()

                    for attr,val in Si_Attr_Val[user].items():

                        if attr =='publisherMainBlogInfo':
                            publisherMainBlogInfo=Si_Attr_Val[user]['publisherMainBlogInfo']
                            #print("publisherUserId:{0} {1}".format(publisherUserId,Si_Attr_Val[publisherMainBlogInfo]))
                            for k,v in Si_Attr_Val[publisherMainBlogInfo].items():
                                #代表个人信息的数据
                                usersInfo[publisherUserId][k]=v
                        elif attr =='type':
                            if type not in usersInfo[publisherUserId].keys():
                                usersInfo[publisherUserId][attr]=[]#typeList
                            usersInfo[publisherUserId][attr].append(val)
                        elif attr != 'publisherUserId': usersInfo[publisherUserId][attr] = val
            allUserInfo.append(usersInfo)

    jsonArray = []
    with open(outFile,'w') as f:
        for usersInfo in allUserInfo:
            for userId in usersInfo.keys():
                 jsonUserObj=dict()
                 jsonUserObj['uid']=userId
                 f.write("userId:::{0}\n".format(userId))
                 for attr,val in usersInfo[userId].items():
                     jsonUserObj[attr]=val
                     f.write("{0}:::{1}\n".format(attr,val))
                 jsonArray.append(jsonUserObj)
                 f.write('\n')
    with open(outJsonFile,'w') as f:
        for jsonstr in jsonArray:
            f.write(json.dumps(jsonstr)+'\n')

def getAllUserBehaviorLog(dirInfo_ParhotFilePath="./PostHots/dirInfo_Parhot.txt",
                   outFile='./PostHotsResult/allUserBehaviorLog.txt',
                   outJsonFile='./PostHotsResult/allUserBehaviorLogJson.txt'):
    allUserIBehaviorLog=[]
    with open(dirInfo_ParhotFilePath) as file:
        while True:
            line=file.readline().strip()
            if(len(line)==0):break
            filePath=line
            blog_postid = filePath[filePath.index('_')+1:filePath.rindex('_')]
            blogid,postid=blog_postid.split('_')
            #print("blog_posid: {0}".format(blog_postid))
            usersInfo = dict()  # (uid,userInfo)
            Si_Attr_Val=Si_Attr_Val2DictAndGetUrl(filePath=filePath,debugEncodeMode=False)
            for user in Si_Attr_Val.keys():
                if 'publisherUserId' in Si_Attr_Val[user].keys():
                    #print("publisherMainBlogInfo: {0}".format(Si_Attr_Val[user]['publisherMainBlogInfo']))
                #if 'blogNickName' not in usersTmp[user].keys(): continue
                    publisherUserId=Si_Attr_Val[user]['publisherUserId']
                    if  publisherUserId not in usersInfo.keys():
                        usersInfo[publisherUserId] = dict()
                        usersInfo[publisherUserId]['blogid']=blogid
                        usersInfo[publisherUserId]['postid'] = postid
                    for attr,val in Si_Attr_Val[user].items():

                        if attr =='publisherMainBlogInfo':
                            publisherMainBlogInfo=Si_Attr_Val[user]['publisherMainBlogInfo']
                            #print("publisherUserId:{0} {1}".format(publisherUserId,Si_Attr_Val[publisherMainBlogInfo]))
                            for k,v in Si_Attr_Val[publisherMainBlogInfo].items():
                                #代表个人信息的数据
                                usersInfo[publisherUserId][k]=v
                        elif attr =='type':
                            if type not in usersInfo[publisherUserId].keys():
                                usersInfo[publisherUserId][attr]=[]#typeList
                            usersInfo[publisherUserId][attr].append(val)
                        elif attr != 'publisherUserId': usersInfo[publisherUserId][attr] = val
            allUserIBehaviorLog.append(usersInfo)

    jsonArray = []
    with open(outFile,'w') as f:
        for usersBehaviorLog in allUserIBehaviorLog:
            for userId in usersBehaviorLog.keys():
                 jsonUserObj=dict()
                 jsonUserObj['uid']=userId
                 f.write("userId:::{0}\n".format(userId))
                 for attr,val in usersBehaviorLog[userId].items():
                     jsonUserObj[attr]=val
                     f.write("{0}:::{1}\n".format(attr,val))
                 jsonArray.append(jsonUserObj)
                 f.write('\n')

    with open(outJsonFile,'a') as f:
        for jsonstr in jsonArray:
            f.write(json.dumps(jsonstr)+'\n')