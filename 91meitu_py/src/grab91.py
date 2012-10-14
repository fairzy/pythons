# -*- coding: utf-8 -*-
import urllib2
import json
import os
from sqlalchemy import *
import httplib

allcount = 0;
insert_count = 0
lastid = 1;
running = True;
while running:
    # 读取网页
    try:
        #url = "http://www.91meitu.net/img-item/get-next?1&lastid=%d" % (lastid)
        url = "http://www.91meitu.net/img-item/free-hands-next?1&lastid=%d" % (lastid)
        textdata = None
        rheaders = {
                   #'Accept': '*/*',
                   #'Accept-Charset':'GBK,utf-8;q=0.7,*;q=0.3',
                   #'Accept-Encoding':'gzip,deflate,sdch',
                   #'Accept-Language':'zh-CN,zh;q=0.8',
                   #'Connection' : 'keep-alive',
                   #'Referer' :'http://www.91meitu.net/',
                   #'Host' : 'www.91meitu.net',
                   'DK_AJAX_REQUEST':'ajax-reqeust',
                   #'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.168 Safari/535.19',
                   #'Cookie':'Hm_lvt_f284ad652b187fce86e85484571cacfb=1336537209994; Hm_lpvt_f284ad652b187fce86e85484571cacfb=1336537209994'
                   }
#        conn = httplib.HTTPConnection( 'www.91meitu.net' )
#        conn.request('GET', url, headers=rheaders)
#        response = conn.getresponse();
        print '========\nlast id: %d'  % (lastid)
        opener = urllib2.build_opener()
        urllib2.install_opener(opener)
        request = urllib2.Request(url, textdata, rheaders)
        response = urllib2.urlopen(request)
        print response.geturl()
        req_info = response.info()
        print req_info
        
        json_str = response.read()
        print  json_str

        obj = json.loads(json_str)
        count = obj['count']
        if count == 0:
            running = False;
        else:
            images = obj['images']
            lastid = obj['lastId']
            for image in images:
                allcount = allcount+1
                print '-----\nallcount: %d' % (allcount)
               
                # 存储文件
                realurl = "http://meitu91.b0.upaiyun.com/" + image['filename'];
                print 'realurl:' + realurl
                ps = os.path.split( image['filename'] );
                savedir = 'E:/Projects/91meitu/' + ps[0]
                # 创建目录
                if os.path.exists(savedir) == False:
                    print '目录不存在'
                    os.makedirs(savedir)
                # 创建文件
                filepath = "E:/Projects/91meitu/" + image['filename'];
                print 'filepath:' + filepath
                if os.path.exists(filepath)==False:
                    print '图片不存在'
                    try:
                        imgdata = urllib2.urlopen(realurl).read()
                    except:
                        print '读取图片出错'
                        continue
                    f = file(filepath, 'wb')
                    f.write(imgdata)
                    f.close()
                else:
                    print '图片已存在'         
                # 存储数据库
                print 'save to db:'
                image_title = image['title']
                image_id = int(image['id'])
                image_width = int(image['width'])
                image_height = int(image['height'])
                image_create_time = image['created_time']
                image_filename = image['filename']
                
                #DB
                engine = create_engine( 'mysql+pymysql://meitu_admin:meitu_admin@localhost:3306/meitu91?charset=utf8' )
                metadata = MetaData()
                metadata.bind = engine
                image_table = Table( 'image', metadata, autoload=True )
                image_insert = image_table.insert().prefix_with('ignore')
                print image_insert
                # insert
                ir = image_insert.execute( id=image_id, title=image_title, width=image_width, height=image_height,\
                                       created_time=image_create_time, filename=image_filename )
                print 'inserted key:'+  str(ir.inserted_primary_key)
                insert_count = insert_count+1
    except Exception as x:
        print 'exception:'
        print x
        continue
else:
    print '抓取完毕，共有:%d张图片' % (allcount);
    print '抓取完毕，插入:%d张图片' % (insert_count);
  
  
    
