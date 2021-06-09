# -*- coding: utf-8 -*-

import os
import sys
import time
from bs4 import BeautifulSoup

from CrawlerDefine import formatContent, Book, Chapter, Picture, Slice
from CrawlerWeb import Param, parseCommandLine, request, write2FCBP

reload(sys)
sys.setdefaultencoding('utf8')

def getChapter(url, index):
    chapter = Chapter()
    chapter.index = index
    chapter.name = '第' +  str(index+1) + '画'
    chapter.sourceUrl = url
    print('\tchapter %04d: %s' %(chapter.index, chapter.name))
    
    req = request(url = url)
    req.encoding = req.apparent_encoding
    soup = BeautifulSoup(req.text, 'html.parser')
    
    pindex = 0
    imgs = soup.find_all('article', class_ = 'article-content')[0].p.find_all('img')
    for img in imgs:
        url = img['src']
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
    title = soup.find_all('h1', class_ = 'article-title')[0].a.text.strip()
    update = soup.find_all('ul', class_ = 'article-meta')[0].find_all('li')[0].text.strip()[5:]
    cover = soup.find_all('div', class_ = 'c-img')[0].img['src']
    introduction = formatContent(soup.find_all('span', class_ = 'dis')[0].text.strip().replace('==>', ''))
        
    book = Book()
    book.sourceName = param.sourceName
    book.sourceUrl = param.bookUrl
    book.refererUrl = param.refererUrl
    book.author = ""
    book.coverUrl = cover
    book.introduction = introduction
    book.name = title
    book.sourceUpdateAt = update
    print(title)
    
    urls = [param.bookUrl]
    list = soup.find_all('div', class_ = 'article-paging')[0].find_all('a', class_ = 'post-page-numbers')
    for a in list:
        if '页' in a.text: continue
        urls.append(a['href'])
#    for index in range(len(urls)):
#        print('\t%d: %s' %(index, urls[index]))
    
    chapterIndex = 0
    for url in urls:
        if chapterIndex >= param.start + param.maxChapters:
            break
        if chapterIndex < param.start:
            chapterIndex += 1
            continue
        chapter = getChapter(url, chapterIndex)
        book.chapters.append(chapter)
        chapterIndex += 1
    return book
    
if __name__ == '__main__':
    param = Param()
    param.bookUrl = 'https://www.3004xx.com/100875725.html'
    param.outputpath = './'
    param.start = 0
    param.maxChapters = 2000000
    param.sourceName = '三四娱乐'
    param.baseUrl = 'https://www.3004xx.com/'
    param.refererUrl = ''
    
    param = parseCommandLine(param)
    book = getBook(param)
    write2FCBP(book, param)
