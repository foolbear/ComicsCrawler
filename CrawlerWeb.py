# -*- coding: utf-8 -*-

import sys
import json
import getopt
import requests
from user_agent import generate_user_agent
from CrawlerDefine import postfixOfFCBP
        
request_timeout = 60

class Param:
    def __init__(self):
        self.bookUrl = ''
        self.outputPath = './'
        self.start = 0
        self.maxChapters = 2000000
        self.sourceName = ''
        self.baseUrl = ''

def parseCommandLine(defaultParam):
    param = defaultParam
    usage = 'Usage: %s -u <url> -o <outputpath> -s <start> -m <maxchapters>' %(sys.argv[0])
    
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'hu:o:s:m:', ['help', 'url=', 'opath=', 'start=', 'max='])
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
        elif key in ('-m', '--max'):
            param.maxChapters = int(value)
    print('request book from %s(%s), outputPath=%s, start=%d, maxChapters=%d' %(param.sourceName, param.bookUrl, param.outputPath, param.start, param.maxChapters))
    return param
    
def write2FCBP(book, param):
    path = param.outputPath + book.name + '_s' + str(param.start) + '_m' + str(param.maxChapters) + postfixOfFCBP
    with open(path, 'w') as file:
        json.dump(obj = book, fp = file, encoding = 'UTF-8', ensure_ascii = False, default = lambda x : x.__dict__, sort_keys = False, indent = 4)
    print('write2FCBP success, output file: %s' %(path))

def request(url):
    userAgent = generate_user_agent()
    referrer = 'http://shurufa.baidu.com/dict.html'
    headers = {'User-Agent': userAgent, 'Referer': referrer}
    try:
        response = requests.get(url, timeout = request_timeout, headers = headers)
        if response.status_code == 200:
            return response
        else:
            raise Exception('response for ' + url + ', status_code = ' + str(response.status_code))
    except requests.exceptions.RequestException as e:
        raise Exception('exception when request ' + url + ', ' + str(e))
