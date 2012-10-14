# -*- coding: utf-8 -*-
import urllib2
from myHTMLParser import MyHTMLParser
from BeautifulSoup import BeautifulSoup
from sqlalchemy import *
from datetime import datetime

''' 通过某页面抓取所有图片主题以及主题内图片链接到数据库'''
def grab_thelink( link ):
    print '------\ngrab:' + link
    html = urllib2.urlopen(link).read()
    html = unicode(html,'gb2312','ignore').encode('utf-8','ignore')
    # soup 
    soup = BeautifulSoup( html )
    # category 当前抓取的页面的分类, 建议的默认分类，添加到topic的备注信息里
    sug_category = soup.find('a', text='首页').next.encode( 'utf-8', 'ignore' )
    print sug_category
    # topic info
    topics = soup.findAll( 'i', {'class' : 'iPic'} )
    print '共有:' + str(len(topics)) + '个主题'
    index_count = 0
    for onetopic in topics:
        if ++index_count > 16:
            return
        try:
            topic_name = onetopic.next['title'].encode('utf-8', 'ignore')
        except:
            print '发生异常，返回了'
            return
        print topic_name
        try:
            topic_cover = onetopic.next.next['src']
        except:
            print '跳过一个主题'
            break;
        print topic_cover   # ../../photo/8004.html
        topic_link = 'http://beauty.pcauto.com.cn/photolist/' + onetopic.next['href'][12:]
        print topic_link
        topic_imagelist = get_imagelist(topic_link)
        if topic_imagelist == None:
            return
        print '本主题内图片共有:'
        print len(topic_imagelist)
        ### 将采集到的信息写入数据库###
            # 新增主题
        engine = create_engine( 'mysql+pymysql://model_admin:model_admin@localhost:3306/carmodel_db?charset=utf8' ) 
        metadata = MetaData()
        metadata.bind = engine
        topic_table = Table('topic', metadata, autoload=True)
        topic_insert = topic_table.insert()
        # with now time
        now = datetime.now()
        nowstr = now.strftime( '%Y-%m-%d %H:%M:%S' )
        topicnew = topic_insert.execute( name=topic_name, cover=topic_cover, create_date=nowstr, other=sug_category )
        topic_id = topicnew.inserted_primary_key
            # 主题内的图片s
        image_table = Table( 'image', metadata, autoload=True )
        image_insert = image_table.insert()
        imageinsert = []
        for aimage in topic_imagelist:
            imageinsert.append( { 'link':aimage, 'topic_id':topic_id, 'create_date':nowstr } )
        image_insert.execute( imageinsert )
        print '----一个主题抓完了----'
    
    
''' 通过每一个主题的图片的链接抓取这个主题下所有的图片链接'''
def get_imagelist( plink ):
    print '--get image list--' + plink
    try:
        page = urllib2.urlopen( plink ).read()
        page = unicode(page,'gb2312','ignore').encode('utf-8','ignore')
        # soup 
        parser = MyHTMLParser( )
        parser.feed( page )
        # get a link 
        imagelinks = parser.image_urls
    except:
        print '打开网址错误，跳过'
        return None
    return imagelinks
    
# 20 条数据源
wait_links = {
              'http://beauty.pcauto.com.cn/cate/11/': 79 ,
              'http://beauty.pcauto.com.cn/cate/14/': 77 ,
              'http://beauty.pcauto.com.cn/cate/32/': 1 ,
              'http://beauty.pcauto.com.cn/cate/36/': 4 ,
              'http://beauty.pcauto.com.cn/cate/37/': 1 ,
              'http://beauty.pcauto.com.cn/cate/47/': 8 ,
              'http://beauty.pcauto.com.cn/cate/50/': 1 ,
              'http://beauty.pcauto.com.cn/cate/49/': 5 ,
              'http://beauty.pcauto.com.cn/cate/51/': 11 ,
              'http://beauty.pcauto.com.cn/cate/52/': 16 ,
              'http://beauty.pcauto.com.cn/cate/57/': 2 ,
              'http://beauty.pcauto.com.cn/cate/58/': 3 ,
              'http://beauty.pcauto.com.cn/cate/59/': 10 ,
              'http://beauty.pcauto.com.cn/cate/65/': 2 ,
              'http://beauty.pcauto.com.cn/cate/67/': 9 ,
              'http://beauty.pcauto.com.cn/cate/70/': 2 ,
              'http://beauty.pcauto.com.cn/cate/78/': 1 
              }

''' 开始 '''
if __name__ == '__main__':
    for alink, count in wait_links.items():
        for i in range(1, count+1):
            thelink = alink + str(i) + '.html'
            grab_thelink( thelink )
        print '========抓取完一个页面========='
    print '========所有抓取完毕!========='
        
        