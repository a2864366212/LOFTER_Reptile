import ast
import json

import numpy as np
import pandas as pd
import pymysql
from pandas.io.json import json_normalize
def readJsonData(filePath,outPutFilePath,needToSave=False,readLines=True,MAX_LINE=5000000):
    jsonObjArray = []
    if readLines:
        jsonData=open(filePath, "r", encoding="UTF-8").readlines()
        for jsonStr in jsonData:
            jsonObj=json.loads((jsonStr.strip()))
            jsonObjArray.append(jsonObj)
    else:
        with open(filePath, "r", encoding="UTF-8") as file:
            cnt=0
            while True:
                jsonStr = file.readline().strip()
                if not jsonStr:break
                cnt+=1
                if cnt>MAX_LINE:break
                print(cnt,end=' ')
                jsonObj = json.loads((jsonStr))
                jsonObjArray.append(jsonObj)
    df = pd.DataFrame(jsonObjArray)
    if needToSave: df.to_csv(path_or_buf=outPutFilePath, index=False)
    return df
def uploadToMySQLDb():
    db=[]
    #db = pymysql.connect(host='175.24.152.230',user = "root",passwd = "",db = "EmojiSIT")
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    #(uid,username,)




    # SQL 插入语句
    sql = """INSERT INTO EMPLOYEE(FIRST_NAME,
             LAST_NAME, AGE, SEX, INCOME)
             VALUES ('Mac', 'Mohan', 20, 'M', 2000)"""

    try:
        # 执行sql语句
        cursor.execute(sql)
        # 提交到数据库执行
        db.commit()
    except:
        # 如果发生错误则回滚
        db.rollback()
    db.close()

def getTagList(inputFile='./PostHotsResult/allUserInfo.csv',outPutFilePath='./PostHotsResult/EmojiTags.csv',needToSave=True):
    # 获取跟 表情包Tag相关的TagList
    df=pd.read_csv(inputFile)
    #print(list(df['tag']!='tag'))
    df_tag=df.iloc[(list(df['tag']!='"tag"'))]['tag']#剔除"tag"行
    df_tag=df_tag[~df['tag'].isna()]#剔除NaN行
    if needToSave:df_tag.to_csv(path_or_buf=outPutFilePath,index=False)

def calTagsFreq(filePath='./PostHotsResult/EmojiSITTags.txt',outPutFilePath='./PostHotsResult/EmojiTagsFreq.csv',needToSave=False):
    # 统计标签信息
    with open(filePath,'r',encoding='utf-8') as file:
        lines=file.readlines()
        tagFreq=dict()
        for line in lines:

            tagsInLine=line.strip().split(',')
            for tag in tagsInLine:
                tag=tag.replace('"','')
                if tag not in tagFreq.keys():
                    tagFreq[tag]=1
                else : tagFreq[tag]=tagFreq[tag]+1
        df = pd.DataFrame.from_dict(tagFreq, orient='index', columns=['freq'])
        df = df.reset_index().rename(columns={'index': 'tag'})
        tagFreqTop=df.sort_values(by=['freq'],ascending=False)
        if needToSave:tagFreqTop.to_csv(outPutFilePath,encoding='utf-8',index=False)

#calTagsFreq(needToSave=True)
#getTagList()
#uploadToMySQLDb()


