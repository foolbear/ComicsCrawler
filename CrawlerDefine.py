# -*- coding: utf-8 -*-

postfixOfFCBP = '.fcbp'

prefixOfContentLine = '        '
separatorBetweenLines = '\n\n'

def formatContent(content):
    lines = map(lambda x: x.strip(), content.strip().split('\n'))
    lines = filter(lambda x: x != '', lines)
    return prefixOfContentLine + (separatorBetweenLines + prefixOfContentLine).join(lines)

class Book:
    def __init__(self):
        self.author = ''
        self.coverUrl = ''
        self.introduction = ''
        self.name = ''
        self.sourceName = ''
        self.sourceUrl = ''
        self.refererUrl = ''
        self.sourceUpdateAt = ''
        self.chapters = []
        
class Chapter:
    def __init__(self):
        self.index = 0
        self.name = ''
        self.sourceUrl = ''
        self.pictures = []

class Picture:
    def __init__(self):
        self.index = 0
        self.slices = []
        
class Slice:
    def __init__(self):
        self.index = 0
        self.sourceUrl = ''
