# -*- coding: utf-8 -*-
# @Time    : 2017/12/23 9:35
# @Author  : Jiqiang Zhou
# @File    : get_youtube_videos.py
# @Software: PyCharm
# @Desc    : get_youtube_videos
#          : using keywords to get videoes from youtube
#Warning   : 此脚本需要与youtube-dl.exe配合使用，仅能下载youtube视频，且需要科学上网。
#Version   : 0.1.0 : creat
import os
import re
import urllib2


def getHtml(url):
    print url
    page = urllib2.urlopen(url)
    html = page.read()
    return html


def getUrl(html, video_url_list):
    reg = r"(?<=a\shref=\"/watch).+?(?=\")"
    urlre = re.compile(reg)
    urllist = re.findall(urlre, html)
    format = "https://www.youtube.com/watch%s\n"
    #f = open("\output.txt", 'a')
    for url in urllist:
        result = (format % url)
        #f.write(result)
        print result
        video_url_list.append(result)
    #f.close()


root = 'D:/VideoDatasets/zhian_fight/'                   #youtube-dl.exe存放路径
video_path = 'crawle_get_video/'                         #视频存储路径，默认在root路径下
video_list = 'crawle_get_video.txt'                      #存储已经下载过的视频的ID

pages = 20                                               #爬取youtube搜索结果的前x页
search_words = ['Fighting+and+brawling+in+surveillance']

video_list = []
#读取已经存在的视频，避免重复下载
# video_folder_list = os.listdir(root + video_path)
# for folder in video_folder_list:
#     videos_in_folder = os.listdir(root + video_path +'/'+folder)
#     for video in videos_in_folder:
#         video_list.append(video.split('.')[0])

f = open(root+video_list, 'a')
f.flush()

for key_word in search_words:
    for i in range(1, pages):
        print "parsing page {}".format(i)
        html = getHtml("https://www.youtube.com/results?sp=EgIYAQ%253D%253D&search_query={}&page={}".format(key_word, i))
        #print html
        video_url_list = []
        getUrl(html, video_url_list)
        for video_url in video_url_list:
            video_url = video_url.strip()
            f.write(video_url+'\n')
            f.flush()
            video_name = video_url.split('v=')[1]
            print video_name
            print root+'youtube-dl.exe -f best -f mp4 {} -o {}.mp4'.format(video_url,root+video_name)
            if video_name not in video_list:#判断是否已经下载过
                os.system('{0}youtube-dl.exe -f best -f mp4 {1} -o {0}{2}{3}/{4}.mp4'.format(root,video_url,video_path,key_word,video_name))
print "done"
