# -*- coding: utf-8 -*-
import urllib2
from BeautifulSoup import BeautifulSoup
import urlparse
from datetime import datetime
import appstore

def grab_tag_apps( tagurl, thetagid ):
    page = 1
    running = True
    while running:
        realtagurl = '%s%d' % (tagurl, page)
        print '开始抓取:' + realtagurl
        html = urllib2.urlopen(realtagurl).read()
        # soup 
        soup = BeautifulSoup( html ) 
        # li节点
        lis = soup.findAll('img', {'class':'icon'})
        if lis == None or len(lis)==0:
            print '没找到相关icon的li !'
            return
        # 寻找其中的appicon的link
        apphrefs = []
        for ali in lis:
            href = ali.parent['href']
            apphrefs.append(href);
            # 根据这个href去appstore抓取
            print 'one href:'
            print href
        print 'href个数:%d' % (len(apphrefs))
        # 将本页的所有链接解析并写入数据库
        appstore.get_appinfo_with_ids( apphrefs, thetagid )
        # 下一页
        page = page+1

if __name__ == '__main__':
    tags = {'Colorful': 1, 'Fabric' : 2, 'Leather' : 3, 'Metal' : 4, 'Minimalistic' : 5, 'Pixel+art' : 6, 'Wooden' : 7} #
    for tagname, tagid in tags.items():
        print '======抓取tag:' + tagname +'======'
        tagurl = 'http://www.iicns.com/?tag=%s&page=' % (tagname)
        grab_tag_apps( tagurl, tagid )
        print '======抓取完毕======'
    
    
    