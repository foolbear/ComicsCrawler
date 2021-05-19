# -*- coding: utf-8 -*-

import os
import sys
import time
import string
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from urllib import quote

from CrawlerDefine import formatContent, Book, Chapter, Picture, Slice
from CrawlerWeb import Param, parseCommandLine, request, write2FCBP

reload(sys)
sys.setdefaultencoding('utf8')

def getPicture(url):
    driver = webdriver.Chrome()
    driver.set_window_size(100, 100)
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    img = soup.find_all('img')[1]['src']
    manga_page = soup.find_all('span', class_ = 'manga-page')[0]
    pindex = manga_page.b.text.strip()
    ptotal = manga_page.text[len(pindex)+1:][:-1]
    driver.close()
    print(pindex + '/' + ptotal + ', ' + img)
    return int(pindex), int(ptotal), quote(img.encode('utf8'), safe = string.printable)

def getChapter(url, title, index):
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
        
        print('\tchapter %04d: %s, include %d pictures' %(chapter.index, chapter.name, len(chapter.pictures)))
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
    
    chapterIndex = 0
    chapters = soup.find_all('div', class_ = 'chapter-list')[0].find_all('ul')[0]
    for chapter in chapters.find_all('li')[::-1]:
        if chapterIndex >= param.start + param.maxChapters:
            break
        if chapterIndex < param.start:
            chapterIndex += 1
            continue
        chapter_url = param.baseUrl + chapter.a['href']
        chapter_title = chapter.a.text.strip()
        
        chapters = getChapter(chapter_url, chapter_title, chapterIndex)
        book.chapters += chapters
        chapterIndex += len(chapters)
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
