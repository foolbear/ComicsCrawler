# -*- coding: utf-8 -*-

import os
import sys
import time

from CrawlerHMH import getChapter, getBook
from CrawlerWeb import Param, parseCommandLine, request, write2FCBP

reload(sys)
sys.setdefaultencoding('utf8')
    
if __name__ == '__main__':
    param = Param()
    param.bookUrl = 'https://www.dstop.xyz/manhua/info/1498.html'
    param.outputpath = './'
    param.start = 0
    param.maxChapters = 2000000
    param.sourceName = '抖手韩漫'
    param.baseUrl = 'https://www.dstop.xyz/'
    
    param = parseCommandLine(param)
    book = getBook(param)
    write2FCBP(book, param)
