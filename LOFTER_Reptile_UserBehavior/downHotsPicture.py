import os
from urllib.request import urlretrieve

def download_file(url, store_path):
    filename = url.split("/")[-1]
    filepath = os.path.join(store_path, filename)
    urlretrieve(url, filepath)

url="https://www.baidu.com/img/flexible/logo/pc/result.png"
store_path="./"
download_file(url,store_path)
