# -*- coding: utf-8 -*-
from BeautifulSoup import BeautifulSoup 
import urllib2

class AppInfo:
    def __init__(self, link ):
        self.app_link = link

    ''' 根据自己的link解析到所有其他app信息'''
    def parseself(self):
        if self.app_link == '':
            print 'error: no link'
            exit(1)
        print 'app_link:' + self.app_link
        html = urllib2.urlopen( self.app_link ).read()
        #parse it
        soup = BeautifulSoup( html )
        self.app_name = soup.h1.string#.encode('utf-8', 'ignore')
        f = file('app_name.txt', 'w')
        f.write(self.app_name)
        f.close()
        print 'app_name:' + self.app_name
        self.app_icon = soup.findAll( 'img', {'class':'artwork'}, width='175' )[0].string
        print self.app_icon


