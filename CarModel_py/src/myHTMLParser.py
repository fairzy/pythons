# -*- coding: utf-8 -*-
from HTMLParser import HTMLParser
class MyHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.image_urls=[]
    def handle_starttag(self, tag, attrs):
        if tag == 'img':
            theurl = ''
            findit = 0
            for (name, value) in attrs:
                if name == 'align' and value=='absmiddle':
                    findit = 1
                if name == 'src':
                    theurl = value
            if findit == 1:
                self.image_urls.append(theurl)
                print 'find one:' + theurl
                    