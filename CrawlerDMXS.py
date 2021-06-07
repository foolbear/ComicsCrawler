# -*- coding: utf-8 -*-

import os
import sys
import time
import json
import string
import getopt
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from urllib import quote

from CrawlerDefine import formatContent, Book, Chapter, Picture, Slice, postfixOfFCBP
from CrawlerWeb import request

reload(sys)
sys.setdefaultencoding('utf8')

class Param:
    def __init__(self):
        self.bookUrl = ''
        self.outputPath = './'
        self.start = 0
        self.startVolume = 0
        self.maxVolumes = 2000000
        self.sourceName = ''
        self.baseUrl = ''

def parseCommandLine(defaultParam):
    param = defaultParam
    usage = 'Usage: %s -u <url> -o <outputpath> -s <start> -v <startvolume> -m <maxvolumes>' %(sys.argv[0])
    
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'hu:o:s:v:m:', ['help', 'url=', 'opath=', 'start=', 'svolume=', 'max='])
    except getopt.GetoptError:
        print(usage)
        sys.exit(2)
    for key, value in opts:
        if key in ('-h', '--help'):
            print(usage)
            sys.exit()
        elif key in ('-u', '--url'):
            param.bookUrl = value
        elif key in ('-o', '--opath'):
            param.outputPath = value
        elif key in ('-s', '--start'):
            param.start = int(value)
        elif key in ('-v', '--svolume'):
            param.startVolume = int(value)
        elif key in ('-m', '--max'):
            param.maxVolumes = int(value)
    print('request book from %s(%s), outputPath=%s, start=%d, startVolume=%d, maxVolumes=%d' %(param.sourceName, param.bookUrl, param.outputPath, param.start, param.startVolume, param.maxVolumes))
    return param
    
def write2FCBP(book, param):
    path = param.outputPath + book.name + '_s' + str(param.start) + '_v' + str(param.startVolume) + '_m' + str(param.maxVolumes) + postfixOfFCBP
    with open(path, 'w') as file:
        json.dump(obj = book, fp = file, encoding = 'UTF-8', ensure_ascii = False, default = lambda x : x.__dict__, sort_keys = False, indent = 4)
    print('write2FCBP success, output file: %s' %(path))

def getVolume(url, title, index):
    req = request(url = url)
    soup = BeautifulSoup(req.text, 'html.parser')
    pics = soup.find('div', {'id': 'pic_list'}).find_all('div')
    
    imgs = []
    for pic in pics:
        if not (pic.has_attr('id') and pic.has_attr('_src')): continue
        pic_url = pic['_src']
        imgs.append(pic_url)
#        pic_id = pic['id']
#        print('\t%s: %s' %(pic_id, pic_url))
    ptotal = len(imgs)
    print('Volume %s, totoal %d pictures' %(title, ptotal))
        
    chapters = []
    count = ptotal // 10 + (0 if ptotal % 10 == 0 else 1)
    pindex = 0
    for ci in range(count):
        chapter = Chapter()
        chapter.index = index + ci
        chapter.name = title + '(P' + str(ci+1) + ')'
        chapter.sourceUrl = url
        
        while len(chapter.pictures) < 10 and pindex < ptotal:
            picture = Picture()
            picture.index = pindex % 10
            slice = Slice()
            slice.index = 0
            slice.sourceUrl = imgs[pindex]
            picture.slices.append(slice)
            chapter.pictures.append(picture)
            pindex += 1
        
        print('\tchapter %04d: %s, include %d picture(s)' %(chapter.index, chapter.name, len(chapter.pictures)))
        chapters.append(chapter)
    return chapters

def getBook(param):
    req = request(url = param.bookUrl)
    soup = BeautifulSoup(req.text, 'html.parser')
    title = soup.find_all('div', class_ = 'list_navbox')[0].h3.a.text
    infos = soup.find_all('li', class_ = 'mss')
    author = infos[0].span.a.text
    latest = infos[4].span
    latest_all = latest.text.strip().replace(' ', '')
    latest_title = latest.a.text.strip()
    update = latest_all[latest_all.find(latest_title)+len(latest_title):][1:-1]
    dds = soup.find_all('div', class_ = 'box_info2')[0].find_all('dd')
    cover = param.baseUrl + dds[0].a.img['src']
    introduction = formatContent(dds[1].text.strip())
        
    book = Book()
    book.sourceName = param.sourceName
    book.sourceUrl = param.bookUrl
    book.author = author
    book.coverUrl = cover
    book.introduction = introduction
    book.name = title
    book.sourceUpdateAt = update
    print(title)
    
    chapterIndex = param.start
    volumeIndex = 0
    volumes = soup.find('div', {'id': 'comic_chapter'}).find_all('ul')[0].find_all('li')[::-1]
    for volume in volumes:
        if volumeIndex >= param.startVolume + param.maxVolumes:
            break
        if volumeIndex < param.startVolume:
            volumeIndex += 1
            continue
            
        url = param.baseUrl + volume.a['href']
        title = volume.a.text.strip()
        chapters = getVolume(url, title, chapterIndex)
        book.chapters += chapters
        chapterIndex += len(chapters)
        volumeIndex += 1
    return book
    
if __name__ == '__main__':
    param = Param()
    param.bookUrl = 'https://comic.acgn.cc/manhua-chengshilieren.htm'
    param.outputpath = './'
    param.start = 0
    param.maxChapters = 2000000
    param.sourceName = '動漫戲說'
    param.baseUrl = 'https://comic.acgn.cc/'
    
    param = parseCommandLine(param)
    book = getBook(param)
    write2FCBP(book, param)
