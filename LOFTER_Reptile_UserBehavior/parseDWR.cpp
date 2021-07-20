#include <iostream>
#include <fstream>
#include <string>
#include <vector>
using namespace std;
void parseDWRFile(string keyword, string input_path, string output_file, bool flag)
{
	ifstream f(input_path, ios::in);
	vector<string> words;
	string line;
	ofstream output;
	if(flag == 1)
	{
		output.open(output_file, ios::app);
	}
	else
		output.open(output_file);
	while(getline(f,line)) 
 	{
  		int index = line.find(keyword);
		if(index == -1)
			continue;
		string url;
		for(int i = index; ; i--)
		{
			if(line[i] == ';')
			{
				index = i+1;
				break;
			}
		}
		for(int i = index; i < line.length(); i++)
		{
			if(line[i] != ';')
			{
				url.push_back(line[i]);
			}
			else
				break;
		}
		output << url << '\n';
 	}
	f.close();
}

void parseMultiAttr(vector<string>&attrList, string input_path, string output_file, bool flag)
{
	for(int i=0;i<attrList.size();i++){
		parseDWRFile(attrList[i],input_path,output_file,flag);//0是覆盖写；1是增量写
	} 
}

void read_dir(string filepath, vector<string> attrList, bool flag)
{
	ifstream input(filepath);
	string line;
	while(getline(input, line))
	{
		string inPath = "";
		inPath = line;
		string outPath = inPath;
		int index = line.find(".txt");
		outPath.erase(index);
		outPath += "_Parhot.txt";
		string outdir = "PostHots/";
		outdir += "dirInfo_Parhot.txt";
		ofstream out(outdir, ios::app);
		out << outPath << '\n';
		parseMultiAttr(attrList,inPath,outPath,flag);
		out.close();
	}
	input.close();
}



int main()
{	
	vector<string> attrList={".publisherUserId",
	".blogNickName",
	".bigAvaImg",
	".gendar",
	".publisherMainBlogInfo", 
	".blogCreateTime",
	".birthday",
	".type",
	".photoLinks",
	".title",
	".tag",
	".createTime",
	}; 
	
	vector<string>oneAttr={"blogPageUrl"};
	read_dir("Posthots/dirInfo.txt", attrList, true);//0覆盖写，1增量写 
	//parseMultiAttr(oneAttr,"lofterPost.txt","blogPageUrl.txt", false);
	return 0;
}

