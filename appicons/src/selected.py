# -*- coding: utf-8 -*-
import urllib2
from BeautifulSoup import BeautifulSoup
import urlparse
from datetime import datetime
import appstore

if __name__ == '__main__':
    index = 13
    links = []
    for index in range(691, 897):
        url = 'http://www.iosinspires.me/category/appicons/post/%d' % index
        html = urllib2.urlopen(url).read()
        soup = BeautifulSoup(html)
        link = soup.find('li', {'class':'itemActionItunes'}).contents[1]['href']
        print index, link 
        links.append(link);
        if  index % 10 == 0 :
            print '------start-----'
            appstore.get_appinfo_with_ids( links, 19 )
            print '------done------' 
            links = []
    print '------start-----'
    appstore.get_appinfo_with_ids( links, 19 )
    print '------done------' 
    links = []
            
    