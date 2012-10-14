# -*- coding: utf-8 -*-
from sqlalchemy import *
import urllib
import os.path
import string
import Image
import math

# db connection
engine = create_engine( 'mysql+pymysql://model_admin:model_admin@localhost:3306/carmodel_db?charset=utf8')
metadata = MetaData()
metadata.bind = engine;
# table
image_table = Table('image', metadata, autoload=True)
# select count of images
image_count = select( [func.count(image_table.c.id)] )
count_r = image_count.execute().fetchone();
count = count_r[0]
print '共有%d张图片' % count
page_count = count/100 #一次一百张图片
if count%100 > 0:
    page_count = page_count+1
print page_count

counter = 0;
error_ids = ''
for i in range(361, page_count+1):
    image_select = select( [image_table.c.id, image_table.c.link] ).offset(i*100).limit(100)
    for onelink in image_select.execute():
        print '------'
        counter = counter+1
        url = onelink['link'];
        image_id = onelink['id']
        print url
        pos = url.rfind('.')
        filepath = '/img' + url[pos:]
        try:
            data = urllib.urlretrieve(url,filepath)
        except:
            error_ids = error_ids + ',' + str(image_id)
        # read the image
        img = Image.open(data[0])
        imgsize = img.size
        imgsize_str = "%dx%d" % imgsize
        print 'image.info';
        print img.info;
        print '%d: %s -- %s' % (counter, image_id, imgsize_str)
        # update the record
        image_update = image_table.update().where(image_table.c.id==image_id).values(size=imgsize_str)
        image_update.execute()
print "errorids:" + error_ids
