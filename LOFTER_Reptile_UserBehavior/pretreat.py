import ast
import json

import pandas as pd
def addHexBlogPostid(csvFile,outputCsvFile):
    '''
    给csv文件添加 十六进制拼接的 Blog_Postid用于检查数据
    :return:
    '''
    df=pd.read_csv(csvFile)
    df['blog_postid']=df['blogid'].apply(lambda x:str(hex(x))[2:])+"_"+df['postid'].apply(lambda x:str(hex(x))[2:])
    df.to_csv(outputCsvFile,index=False)
def getPicUrl(csvFile,outputCsvFile):
    '''
    截取csv文件中  图片链接不为空的数据
    :param csvFile:
    :param outputCsvFile:
    :return:
    '''
    df=pd.read_csv(csvFile)
    df=df[~df['photoLinks'].isnull()]# 去掉空链接
    df=df.drop_duplicates(['blog_postid'])#去重blog post
    df=df[['blogid','blog_postid','photoLinks','createTime','tag',]]

    lofterPicInfoList=[]
    import uuid
    for i in range(0,len(df)):
        row=df.iloc[i]
        photoLinksList=json.loads(ast.literal_eval(row['photoLinks']))# [{},{},{},]
        for ele in photoLinksList:
            # 遍历  photoLinks 的 value
            # 四个质量等级的图片：[raw,small,middle,orign]:link
            for k in ele.keys():
                if (isinstance(ele[k], str) and len(ele[k]) >= 4 and ele[k][:4] == "http") \
                        and k == 'raw':
                    lofterPicInfoList.append(list(df.iloc[i].drop(['photoLinks']))+[ele[k]
                                                                    ,uuid.uuid3(namespace=uuid.NAMESPACE_URL,name=ele[k])])
                    break

    df=pd.DataFrame(lofterPicInfoList,columns=['blogid','blog_postid','createTime','tag','photoLink','eid'])
    df.to_csv(outputCsvFile, index=False)


def getUserBhvAndInfo(csvFile,outUserInfo,outUserBhv):
    '''
    1.导出用户信息和用户行为数据
    2.统计各用户出现的频率
    :return:
    '''
    dfUser=pd.read_csv(csvFile,usecols=['uid','type','blog_postid','title','gendar','birthday','bigAvaImg'])
    dfUser['type']=dfUser['type'].apply(lambda  x:x[2])
    # title= 昵称|时间
    print(dfUser['title'].head())
    dfUser['username']=dfUser['title'].apply(lambda x:str(x).split(' - ')[0]+'"')# 切分title列
    dfUser['bhvtime']=dfUser['title'].apply(lambda x:'"'+str(x).split(' - ')[-1])# 切分title列
    dfUser['bhvtime']=dfUser['bhvtime'].apply(lambda x:"\"2021/"+x[1:] if x.count('/')==1 else x)# 补全年份

    dfUser=dfUser[(dfUser['type']=="3") | (dfUser['type']=="1")]
    dfUserInfo=dfUser[['uid','username','gendar','birthday','bigAvaImg']]
    dfUserBhv=dfUser[['uid','type','blog_postid','bhvtime']]
    userFreq={}
    freqNum={}
    for uid in dfUserBhv['uid']:userFreq[uid]=userFreq.get(uid,0)+1
    for freq in userFreq.values():freqNum[freq]=freqNum.get(freq,0)+1
    print(freqNum)
    dfUserInfo.to_csv(outUserInfo,index=False)
    dfUserBhv.to_csv(outUserBhv,index=False)

    # user_item=dfUserBhv[['uid','blog_postid']]
    # user_item.to_csv('userItemPair',sep=' ',index=False,header=False)

def joinUserBhvAndEmojiByBlogpostid(usrBhvFile,emojiFile):
    '''
    用户在帖子下评论，默认的与帖子下所有图片产生评论行为:<user,blog_post>  ==>  <user,eidList>
    :return:
    '''
    userBhv=pd.read_csv(usrBhvFile)
    emoji=pd.read_csv(emojiFile)
    userBhv=pd.merge(userBhv,emoji[['blog_postid','eid']],on='blog_postid')
    userBhv.to_csv('PostHotsResult/userBhvAppendEid.csv',index=False)

def tagUnicode2utf8(csvFile,outCsvFile):
    '''
    将tag的 unicode编码转为 utf-8 ，转化不了的部分tag舍弃。 utf-8格式数据作为新列加在原数据中

    tags[1:-1].encode('utf-8').decode('unicode-escape')
    :return:
    '''
    emojiinfo=pd.read_csv(csvFile,encoding='utf-8')

    utf8_tags=[]
    error=[]
    import re
    for tags in emojiinfo['tag']:
        utf8_tag=tags[1:-1].encode('UTF-8', 'replace').decode('unicode-escape').encode('UTF-8', 'ignore').decode('UTF-8')
        utf8_tag = re.split(',{1,}', utf8_tag)  # 去除相邻','
        res = ""
        for tag in utf8_tag: res += ',' + tag  # 合并
        utf8_tag = res.strip(',')  # 去除首尾多余','
        utf8_tags.append(utf8_tag)

    emojiinfo['tag_utf8']=utf8_tags
    emojiinfo.to_csv(outCsvFile,encoding='utf-8')
