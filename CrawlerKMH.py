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

def getPicture(url):
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    driver = webdriver.Chrome(chrome_options = options)
    driver.get(url)
    
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    img = soup.find_all('img')[1]['src']
    manga_page = soup.find_all('span', class_ = 'manga-page')[0]
    pindex = manga_page.b.text.strip()
    ptotal = manga_page.text[len(pindex)+1:][:-1]
    driver.close()
    print('\t%s/%s, %s' %(pindex, ptotal, img))
    return int(pindex), int(ptotal), quote(img.encode('utf8'), safe = string.printable)

def getVolume(url, title, index):
    print('Volume %s' %(title))
    pindex, ptotal, img = getPicture(url)
    imgs = [img]
    for i in range(ptotal-1):
        u = url + '#p=' + str(i+2)
        pindex, ptotal, img = getPicture(u)
        imgs.append(img)
        
    chapters = []
    count = ptotal // 10 + 1
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
    title = soup.find_all('div', class_ = 'main-bar bar-bg1')[0].h1.text
    cont_list_dls = soup.find_all('div', class_ = 'cont-list')[0].find_all('dl')
    author = cont_list_dls[2].text.strip()[3:]
    update = cont_list_dls[1].text.strip()[4:]
    cover = soup.find_all('div', class_ = 'thumb')[0].img['src']
    introduction = formatContent(soup.find_all('div', class_ = 'book-intro book-intro-more')[0].text.strip())
        
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
    volumes = soup.find_all('div', class_ = 'chapter-list')[0].find_all('ul')[0]
    for volume in volumes.find_all('li')[::-1]:
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
    param.bookUrl = 'https://m.mhgui.com/comic/1062/'
    param.outputpath = './'
    param.start = 0
    param.maxChapters = 2000000
    param.sourceName = '看漫画'
    param.baseUrl = 'https://m.mhgui.com/'
    
    param = parseCommandLine(param)
    book = getBook(param)
    write2FCBP(book, param)
