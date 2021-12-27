# -*- coding: utf-8 -*-
# @Time    : 2021/12/27 9:08
# @Author  : lisong
# @File    : postblogid2blogurl.py
# @Comment :



import urllib3
import requests
import scrapy
def getBlogUrl(blogid, postid):
    # 521787492 4005033291
    post_blogid = "{:x}_{:x}".format(blogid,postid)
    templateUrl = "https://anything.lofter.com//post/{}".format(post_blogid)
    resp = requests.get(templateUrl,allow_redirects=False)#不允许重定向
    true_url=resp.headers.get('Location')
    return true_url
