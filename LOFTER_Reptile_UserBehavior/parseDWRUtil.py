
def parseDWRFile(keyword, input_path, output_file, flag):
    input = open(input_path, "r", encoding="utf-8")
    line = input.readline()
    if flag == 1:
        output = open(output_file, "a")
    else:
        output = open(output_file, "w")
    while line:
        str = line.split(";")
        for ss in str:
            if keyword in ss:
                output.write(ss + '\n')
                break
        line = input.readline()

def parseMultiAttr(attrList, input_path, output_file, flag):
    for i in range(len(attrList)):
        parseDWRFile(attrList[i],input_path,output_file, flag)

def parseDWRFilesOfDir(rootPath,dirInfoFilepath, attrList, flag):
    input = open(dirInfoFilepath, "r", encoding="utf-8")
    line = input.readline()
    outdir = rootPath.strip('/') + '/'
    outdir += "dirInfo_Parhot.txt"
    output = open(outdir, "a")
    while line:
        inPath = line.strip(    )
        index = line.find(".txt")
        line = rootPath.strip('/')+'/'+line[:index]
        outPath = line + "_Parhot.txt"
        output.write(outPath + "\n")
        parseMultiAttr(attrList, inPath, outPath, flag)
        line = input.readline()
    output.close()

attrList=[".publisherUserId",
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

