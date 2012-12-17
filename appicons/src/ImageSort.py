# -*- coding: utf-8 -*-
import Image
from sqlalchemy import *
import urllib2
import urlparse
import os
import colorrange

if __name__ == '__main__': 
    # 从数据库取出img地址
    engine = create_engine( 'mysql+pymysql://root:root@localhost:3306/icon_db?charset=utf8' )
    metadata = MetaData()
    metadata.bind = engine
    # app_tag关系表操作
    app_tag_table = Table( 'app_tag_ref_copy', metadata, autoload=True ) 
    apptag_insert = app_tag_table.insert().prefix_with('ignore')
    # 首先写入app到表中
    app_table = Table( 'app_info_copy_copy', metadata, autoload=True ) 
    # select count of images
    image_count = select( [func.count(app_table.c.appID)] )
    count_r = image_count.execute().fetchone();
    count = count_r[0]
    print '共有%d个app' % count
    page_count = count/100 #一次一百张图片
    if count%100 > 0:
        page_count = page_count+1
    print page_count
    
    for i in range(0, page_count+1):
        print '======分页: %d======' % (i)
        image_select = select( [app_table.c.appID, app_table.c.appLogo] ).offset(i*100).limit(100)
        j = 0
        for onelink in image_select.execute():
            j = j+1
            print '------------计算一个: %d----------' % (j)
            appid = onelink['appID']
            applogo = onelink['appLogo']
            urllen = len(applogo)
            urlarray = applogo.split('.')
            suffix = urlarray[len(urlarray)-1]
            if suffix == 'png' or suffix == 'jpg':
                applogo = applogo[:(urllen-3)] + '114x114-75.' + suffix
            print appid, applogo, suffix
            # 下载logo到本地
            patharray = urlparse.urlsplit(applogo).path.split('/')
            filepath = './size/' + patharray[ len(patharray)-1]
            if os.path.exists(filepath) == False:
                imgdata = urllib2.urlopen(applogo).read()
                f = file(filepath, 'wb')
                f.write(imgdata)
                f.close()
            # 计算tag
            logotagid = colorrange.calculateColor(filepath)
            print 'logotag:' , logotagid
            if logotagid != None:
                # 将appid和color的tag写入数据库
                ati = apptag_insert.execute( app_id=appid, tag_id=logotagid )
                print '**app tag inserted key:'+  str(ati.inserted_primary_key)
            
            
            
            
            
            
            
            
            
            
            
