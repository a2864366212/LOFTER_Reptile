LOFTER_Reptile

网易乐乎LOFTER的爬取工具，提供待爬取的目标标签，得到对应博主和评论者的社交数据

# 项目结构

```
|-- LOFTER_Reptile
|   |-- README
|   |-- LOFTER_Reptile_UserBehavior
|   |   |--PostHots
|   |   |--PostHotsResult
|   |   |--downHotsPicture.py
|   |   |--lofterBlogReq.py
|   |   |--lofterHotsList.py
|   |   |--lofterParseHotsDWR.py
|   |   |--main_user_publish.py
|   |   |--main_userinfo_behaviorlog.py
|   |   |--parseDWRUtil.py
|   |   |--uploadDataToDb.py

|   |-- LOFTER_Reptile_UserInfo
|   |   |--
```

## LOFTER_Reptile_UserBehavior

爬取**目标标签**的博主和评论者社交数据

### 调用时序图

**getUserInfoJsonByTag(tag):**

```python
传入tag
->main_userinfo_behaviorlog.getUserInfoJsonByTag(tag)
->main_userinfo_behaviorlog.initFile()
->lofterBlogReq.postReqNum(num=1500, step=100, tag=tag)
->parseDWRUtil.parseMultiAttr(parseDWRUtil.oneAttr, input_path="./lofterPost.txt",output_file="blogPageUrl.txt", flag=0)
->lofterHotsList.reqDWRfileOfHots(rootPath="./PostHots/", targetBlogUrlsFile=targetBlogUrlsFile,blogNum=10000, step=100, tag=tag,sleepTime=sleepTime)
->lofterParseHotsDWR.genDirFileInfo(rootPath="./PostHots/",listFile="dirInfo.txt")
->parseDWRUtil.parseDWRFilesOfDir(rootPath="./PostHots/", dirInfoFilepath="./PostHots/dirInfo.txt",attrList=parseDWRUtil.attrList, flag=1)
->lofterParseHotsDWR.getAllUserBehaviorLog()                      

```



### downHotsPicture.py

函数说明

函数名 | 参数                           | 返回值 | 解释 
:- | - | -|- 
download_file | url: string,store_path: string | None | 传入HotsPicture的url，下载图片资源存储到指定的store_path 

### lofterBlogReq.py

函数说明	

函数名 | 参数                           | 返回值 | 函数说明 | 参数说明 
:- | - | -|- |- 
getReqTest | tag: string | None | 测试乐乎网站对于某一tag的请求，获取返回的页面内容，写入到"lofterTest.txt"文件中。给开发者提供一个直观的感受 | tag  ：待请求标签 
postReq | blogNum: int, lastIdx : int, sleepTime=0.5:float, tag="表情包": string | None | 根据传入的"tag"，请求对应标签的帖子，获得某一 .dwr文件，将dwr文件内容末尾追加到"lofterPost.txt"文件中。请求的帖子范围为[lastIdx,lastIdx+blogNum]，数目为blogNum | blogNum: 请求帖子总数; lastIdx : 已请求帖子数; sleepTime=0.5:睡眠一段时间的反爬虫策略; tag="表情包": 待请求标签 
postReqNum | num:int,step=5:int, tag="表情包": string | None | 对postReq函数的高一级别封装。以step步长循环请求tag标签下的帖子，总共请求num个帖子 | num: 请求帖子总数；step=5: 请求步长；tag="表情包": 请求标签 

### lofterHotsList.py

函数说明

函数名 | 参数                           | 返回值 | 解释 | 参数说明 
:- | - | -|- |- 
postReqHotsList | rootPath: string, postid:int, blogid:int, blogNum:int, lastIdx:int, sleepTime=4:float, debugMode=False: bool, tag="表情包": string | None | 获取某一帖子的热度列表（其实是其他用户的收藏、转发、点赞行为）。请求的帖子范围为[lastIdx,lastIdx+blogNum]，数目为blogNum |rootPath: 结果文件的根目录; postid:帖子id; blogid:博客id; blogNum: 请求的blog_post_hotsList总数; lastIdx: 已经请求的 blog_post_hotsList数目; sleepTime: 睡眠一段时间的反爬虫策略; debugMode: debug信息输出控制参数; tag="表情包": 请求标签
reqDWRfileOfHots | rootPath: string, targetBlogUrlsFile= "blogPageUrl.txt": string, blogNum:int, step=100: int, sleepTime=4:float, tag="表情包": string | None | postReqHotsList的高一级别封装。以step步长循环请求tag标签下各个帖子的热度列表，总共请求blogNum个帖子。其中各个帖子的url由targetBlogUrlsFile指定 |rootPath: 结果文件的根目录; targetBlogUrlsFile:存储某标签下的各个帖子的url; blogNum: 请求的blog_post_hotsList总数; ttstep=100: 请求的步长; sleepTime: 睡眠一段时间的反爬虫策略; tag="表情包": 请求标签

### lofterParseHotsDWR.py

函数说明

函数名 | 参数                           | 返回值 | 解释 | 参数说明 
:- | - | -|- |- 
模板 | 模板 | 模板 | 模板 |模板

### main_userinfo_behaviorlog.py

函数说明

函数名 | 参数                           | 返回值 | 解释 | 参数说明 
:- | - | -|- |- 
getUserInfoJsonByTag | tag: string | None | 调用一系列高级别封装的函数，获取指定tag下的用户行为数据，以json格式存储到文件中 |tag: 请求标签
getTagList | TagsFile: string | list(set(tagsList)) | 传入存有多个标签的文件路径，读取文件中的标签，去重后返回标签序列。标签文件中一行可含有多个标签，需以英文逗号分隔。 |TagsFile:存有多个标签的文件路径
autoGetTagListInfo | None | None | getUserInfoJsonByTag的高一级封装。从标签文件中读取数据，得到标签序列，获取所有序列中所有标签对应的用户行为数据。 |None
### uploadDataToDb.py

函数说明

函数名 | 参数                           | 返回值 | 解释 | 参数说明 
:- | - | -|- |- 
calTagsFreq | filePath: string, outPutFilePath: string, needToSave: bool | None | 统计爬取的用户行为数据的标签-频率分布 |filePath: 标签文件; outPutFilePath: 输出文件保存路径; needToSave: 是否需要保存到文件中，为1写入到文件中
 readJsonData | filePath, outPutFilePath, needToSave=False, readLines=True, MAX_LINE=5000000 | Dataframe |  |
 uploadToMySQLDb （还未实现） |  |  | 将本地格式化后的数据上传大Mysql数据库中 |
 getTagList | filePath: string, outPutFilePath: string, needToSave: bool | df['tag'] | 将输入的用户行为信息转化为df,从df中获取df['tag'] |filePath: 用户行为信息文件; outPutFilePath: 输出文件保存路径; needToSave: 是否需要保存到文件中，为1写入到文件中
### parseDWRUtil.py

函数说明

函数名 | 参数                           | 返回值 | 解释 | 参数说明 
:- | - | -|- |- 
parseDWRFile | keyword: string, input_path: string, output_file: string, flag: int | None | 解析dwr文件，将含有keyword的行数据写入到output_file中。可以理解为一个filter |keyword: 在文件中搜索的目标关键字; input_path: 输入文件路径; output_file: 输出文件路径; flag: 结果写入方式，1表示末尾追加、0表示覆写
parseMultiAttr | attrList: List[string], input_path: string, output_file: string, flag: int | None | parseDWRFile的高一级封装。传入一组keyword，即attrList。将所有keyword在input_path文件中的数据写入到output_file中。 |attrList: 在文件中搜索的目标关键字数组; input_path: 输入文件路径; output_file: 输出文件路径; flag: 结果写入方式，1表示末尾追加、0表示覆写
parseDWRFilesOfDir | rootPath: string, dirInfoFilepath: string , attrList: List[String], flag: int | None | parseMultiAttr的高一级别封装。传入一组keyword，解析某文件夹下的所有dwr文件，将数据分别写入到对应的{dwrfileName}_Parhot.txt结果文件中 |rootPath: 输入输出文件的根目录; dirInfoFilepath: 待解析文件夹所在路径 ; attrList: 在文件中搜索的目标关键字数组; flag: 结果写入方式，1表示末尾追加、0表示覆写

其中常用的attr如下，对应属性的解释参照之前的描述

```python
attrList=[
    ".publisherUserId",
	".blogNickName",
	".bigAvaImg",
	".gendar",
	".blogCreateTime",
	".birthday",
	".type",
	".photoLinks",
	".title",
	".tag",
	".createTime",
	]
oneAttr=[".blogPageUrl"]
```

## LOFTER_Reptile_UserInfo








