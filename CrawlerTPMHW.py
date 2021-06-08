# -*- coding: utf-8 -*-

import os
import sys
import time
from bs4 import BeautifulSoup

from CrawlerDefine import formatContent, Book, Chapter, Picture, Slice
from CrawlerWeb import Param, parseCommandLine, request, write2FCBP

reload(sys)
sys.setdefaultencoding('utf8')

def getChapter(url, index, title, param):
    chapter = Chapter()
    chapter.index = index
    chapter.name = title
    chapter.sourceUrl = url
    print('\tchapter %04d: %s' %(chapter.index, title.strip()))
    
    pageUrl = url
    pindex = 0
    while pageUrl != None:
        req = request(url = pageUrl)
        req.encoding = req.apparent_encoding
        soup = BeautifulSoup(req.text, 'html.parser')
        print('\t\tpage: ' + pageUrl)
        
        imgs = soup.find_all('div', class_ = 'mip-box-body book-detail-content')[0].find_all('img')
        for img in imgs:
            picture = Picture()
            picture.index = pindex
            slice = Slice()
            slice.index = 0
            slice.sourceUrl = img['data-original']
            picture.slices.append(slice)
            chapter.pictures.append(picture)
            pindex += 1
            print('\t\t\t' + slice.sourceUrl)
            
        down_pages = soup.find_all('a', class_ = 'down-page')
        pageUrl = None
        for a in down_pages:
            if a.text == '下一页':
                pageUrl = param.baseUrl + a['href']
    
    return chapter

def getBook(param):
    req = request(url = param.bookUrl)
    req.encoding = req.apparent_encoding
    soup = BeautifulSoup(req.text, 'html.parser')
    right = soup.find_all('div', class_ = 'right')[0]
    title = right.h1.text.strip()
    infos = right.find_all('div')
    author = infos[0].text[3:]
    update = infos[1].text[3:]
    left = soup.find_all('div', class_ = 'left')[0]
    cover = param.baseUrl + left.img['src']
    introduction = formatContent(right.find_all('p', class_ = 'hidden-xs')[0].text.strip())
        
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
    list = soup.find_all('ul', class_ = 'list-unstyled bookAll-item-list')[1].find_all('li')
    for chapter in list:
        url = param.baseUrl + chapter.a['href']
        title = chapter.a.text
        chapters.append((url, title))
    chapters = sorted(chapters, key = lambda x: x[0])
#    for chapter in chapters:
#        print("%s %s" %(chapter[0], chapter[1]))
    
    chapterIndex = 0
    for c in chapters:
        if chapterIndex >= param.start + param.maxChapters:
            break
        if chapterIndex < param.start:
            chapterIndex += 1
            continue
        chapter = getChapter(c[0], chapterIndex, c[1], param)
        book.chapters.append(chapter)
        chapterIndex += 1
    return book
    
if __name__ == '__main__':
    param = Param()
    param.bookUrl = 'https://www.tptoon.com/book/6262.html'
    param.outputpath = './'
    param.start = 0
    param.maxChapters = 2000000
    param.sourceName = '头牌漫画网'
    param.baseUrl = 'https://www.tptoon.com/'
    param.refererUrl = 'http://www.mhw.one'
    
    param = parseCommandLine(param)
    book = getBook(param)
    write2FCBP(book, param)
