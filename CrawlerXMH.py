# -*- coding: utf-8 -*-

import os
import sys
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By

from CrawlerDefine import formatContent, Book, Chapter, Picture, Slice
from CrawlerWeb import Param, parseCommandLine, request, write2FCBP

reload(sys)
sys.setdefaultencoding('utf8')

def getChapter(url, title, index):
    chapter = Chapter()
    chapter.index = index
    chapter.name = title
    chapter.sourceUrl = url
    print('\tchapter %04d: %s' %(chapter.index, chapter.name))
    
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('user-agent=Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Mobile Safari/537.36')
    options.page_load_strategy = 'eager'
    driver = webdriver.Chrome(chrome_options = options)
    driver.get(url)
    
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    imgs = soup.find('div', {'id': 'cp_img'}).find_all('img')
    urls = []
    for img in imgs:
        urls.append(img['data-src'])
    
    pindex = 0
    for url in urls:
        picture = Picture()
        picture.index = pindex
        slice = Slice()
        slice.index = 0
        slice.sourceUrl = url
        picture.slices.append(slice)
        chapter.pictures.append(picture)
        pindex += 1
        print('\t\t%s' %(url))
    return chapter

def getBook(param):
    req = request(url = param.bookUrl)
    req.encoding = req.apparent_encoding
    soup = BeautifulSoup(req.text, 'html.parser')
    title = soup.find_all('p', class_ = 'detail-info-title')[0].text.strip()
    author = soup.find_all('p', class_ = 'detail-info-tip')[0].find_all('span')[0].text[3:].strip()
    this = soup.find_all('div', class_ = 'detail-list-form-title')[0]
    atext = this.a.text.strip()
    spantext = this.find_all('span', class_ = 's')[0].text.strip()
    thistext = this.text.strip()[len(atext):]
    update = thistext[:len(thistext) - len(spantext)].strip()[-10:]
    cover = soup.find_all('img', class_ = 'detail-info-cover')[0]['src']
    introduction = formatContent(soup.find_all('p', class_ = 'detail-info-content')[0].text.strip())

    book = Book()
    book.sourceName = param.sourceName
    book.sourceUrl = param.bookUrl
    book.refererUrl = param.refererUrl
    book.author = author
    book.coverUrl = cover
    book.introduction = introduction
    book.name = title
    book.sourceUpdateAt = update
    print(title)
    
    chapters = []
    list = soup.find_all('div', class_ = 'detail-list-form-con')[0].find_all('a')
    for a in list:
        atext = a.text.strip()
        spantext = a.find_all('span')[0].text.strip()
        title = atext[:len(atext)-len(spantext)].strip()
        url = param.baseUrl + a['href']
        chapters.insert(0, (url, title))

    chapterIndex = 0
    for c in chapters:
        if chapterIndex >= param.start + param.maxChapters:
            break
        if chapterIndex < param.start:
            chapterIndex += 1
            continue
        chapter = getChapter(c[0], c[1], chapterIndex)
        book.chapters.append(chapter)
        chapterIndex += 1
    return book
    
if __name__ == '__main__':
    param = Param()
    param.bookUrl = 'https://www.xmanhua.com/550xm/'
    param.outputpath = './'
    param.start = 0
    param.maxChapters = 2000000
    param.sourceName = 'X漫画'
    param.baseUrl = 'https://www.xmanhua.com/'
    param.refererUrl = ''
    
    param = parseCommandLine(param)
    book = getBook(param)
    write2FCBP(book, param)

