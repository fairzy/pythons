# -*- coding: utf-8 -*-
import urllib2
from BeautifulSoup import BeautifulSoup
from sqlalchemy import *
from datetime import datetime

def grab_topiclist( link ):
    print 'grab:' + link
    html = urllib2.urlopen(link).read()
    # soup 
    soup = BeautifulSoup( html ) 
    # grab topics
    topics = soup.findAll('img', {'width':'120', 'height':'160'})
    for atopic in topics:
        # topic_name
        topic_name = atopic['alt'].encode('utf-8', 'ignore')
        print 'topic_name:' + topic_name 
        # topic_cover 
        topic_cover = atopic['src']
        print 'topic_cover:' + topic_cover
        # topic_link 
        topic_link = 'http://auto.msn.com.cn' + atopic.next.next['href']
        print 'topic_link:' + topic_link
        topic_images = get_topicimages( topic_link )
        
        #### WRITE TO DATABASE ###
        #  connect to db
        engine = create_engine( 'mysql+pymysql://model_admin:model_admin@localhost:3306/carmodel_db?charset=utf8' )
        print engine
        metadata = MetaData()
        metadata.bind = engine
        # time
        now = datetime.now()
        nowstr = now.strftime( '%Y-%m-%d %H:%M:%S' )
        # insert into topic table
        topic_table = Table( 'topic', metadata, autoload=True )
        topic_insert = topic_table.insert()
        isresult = topic_insert.execute( name=topic_name, cover=topic_cover, create_date=nowstr, source='msn_auto' )
        topic_id = isresult.inserted_primary_key
        print '--insert topicid:' + str(topic_id) +'---'
        # insert into images table
        for aimage in topic_images:
            aimage['topic_id'] = topic_id
            aimage['create_date'] = nowstr
        image_table = Table( 'image', metadata, autoload=True )
        image_insert = image_table.insert()
        image_insert.execute( topic_images )

def get_topicimages( link ):
    print 'in_topic_images_link:' + link
    html = urllib2.urlopen(link)
    # soup
    soup = BeautifulSoup( html ) 
    # images
    image_list = []
    imageselement = soup.findAll('img', {'desc':''})
    print '\tfind_images: %d' % len(imageselement)
    for aimage in imageselement:
        image_list.append( {'link':aimage['bigpic'], 'thumbnail_link':aimage['src'], 'description':aimage['alt'].encode('utf-8', 'ignore') } )
        print '\t一张图片:' + aimage['bigpic'] + '--' + aimage['src'] + '--' + aimage['alt']
    return image_list

if __name__ == '__main__':
    grab_topiclist( 'http://auto.msn.com.cn/beauty/list/index.shtml' )
    for i in range(2, 21):
        url = 'http://auto.msn.com.cn/beauty/list/index_' + str(i) +'.shtml'
        grab_topiclist( url  )
        print '------抓取完一页-----'
    print '======抓取完毕======'
    