
def parseDWRFile(keyword, input_path, output_file, flag,endChr='\n'):
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
                output.write(ss + endChr)
                break
        line = input.readline()
    input.close()
    output.close()

def parseMultiAttr(attrList, input_path, output_file, flag,endChr='\n'):
    for i in range(len(attrList)):
        parseDWRFile(attrList[i],input_path,output_file, flag,endChr=endChr)

def read_dir(filepath, attrList, flag):
    input = open(filepath, "r", encoding="utf-8")
    line = input.readline()
    while line:
        inPath = line.strip()
        index = line.find(".txt")
        line = line[:index]
        outPath = line + "_Parhot.txt"
        outdir = "PostHots/"
        outdir += "dirInfo_Parhot.txt"
        output = open(outdir, "a")
        output.write(outPath + "\n")

        parseMultiAttr(attrList, inPath, outPath, flag)
        line = input.readline()

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

