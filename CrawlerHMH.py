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

def getChapter(bookName, url, index, param):
    req = request(url = url)
    req.encoding = req.apparent_encoding
    soup = BeautifulSoup(req.text, 'html.parser')
    title = soup.title.text.strip()[len(bookName)+1:]
    
    chapter = Chapter()
    chapter.index = index
    chapter.name = title
    chapter.sourceUrl = url
    print('\tchapter %04d: %s' %(chapter.index, title))
    
    pictureIndex = 0
    imgList = soup.find('p', {'id': 'imgList'})
    if imgList != None:
        divs = imgList.find_all('div', {'style': 'display: flex;align-items: center;'})
        if len(divs) != 0:
            for div in divs:
                sys.stdout.write('(')
                picture = Picture()
                picture.index = pictureIndex
                sliceIndex = 0
                for img in div.find_all('img'):
                    sys.stdout.write('.')
                    slice = Slice()
                    slice.index = sliceIndex
                    slice.sourceUrl = param.baseUrl + img['src']
                    picture.slices.append(slice)
                    sliceIndex += 1
                sys.stdout.write(')')
                chapter.pictures.append(picture)
                pictureIndex += 1
            sys.stdout.write('\n')
        else:
            imgs = imgList.find_all('img')
            for img in imgs:
                if len(img['src']) == 0:
                    continue
                sys.stdout.write('*')
                picture = Picture()
                picture.index = pictureIndex
                slice = Slice()
                slice.index = 0
                slice.sourceUrl = param.baseUrl + img['src']
                picture.slices.append(slice)
                chapter.pictures.append(picture)
                pictureIndex += 1
            sys.stdout.write('\n')
            
    return chapter

def getBook(param):
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    driver = webdriver.Chrome(chrome_options = options)
    driver.get(param.bookUrl)
    alert = driver.switch_to.alert
    alert.accept()

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    book_header = soup.find_all('div', class_ = 'book-header')[0]
    h1 = book_header.h1
    h1_text = h1.text.strip()
    span_text = h1.span.text.strip()
    title = h1_text[:h1_text.find(span_text)].replace('/', "-")
    writer = book_header.find_all('p', class_ = 'writer')
    author = writer[1].text.strip()[4:]
    update = writer[2].text.strip()[5:]
    cover = param.baseUrl + writer[0].img['src']
    introduction = formatContent(book_header.find_all('p', class_ = 'desc')[0].text.strip())
        
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
    url = ""
    elements = driver.find_elements(By.XPATH, '//*[@id=\'chapter-list\']/div/div[' + str(chapterIndex+1) + ']/a')
    while len(elements) != 0 and chapterIndex < param.start + param.maxChapters:
        elements[0].click()
        while url == driver.current_url:
            time.sleep(2)
        url = driver.current_url
        if url == param.bookUrl:
            break
        if chapterIndex >= param.start:
            chapter = getChapter(book.name, url, chapterIndex, param)
            book.chapters.append(chapter)
        chapterIndex += 1
        elements = driver.find_elements(By.XPATH, '//*[@id="div_width"]/p[4]/a[3]')
    
    driver.close()
    return book
    
if __name__ == '__main__':
    param = Param()
    param.bookUrl = 'https://www.mhnew.xyz/manhua/info/1390429720578883584.html'
    param.outputpath = './'
    param.start = 0
    param.maxChapters = 2000000
    param.sourceName = 'H漫画'
    param.baseUrl = 'https://www.mhnew.xyz/'
    
    param = parseCommandLine(param)
    book = getBook(param)
    write2FCBP(book, param)
