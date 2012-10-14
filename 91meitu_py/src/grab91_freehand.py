# -*- coding: utf-8 -*-
import urllib2
import urllib
import json
import os

allcount = 0;
lastid = 1;
running = True;
while running:
    # 读取网页
    try:
        url = "http://www.91meitu.net/img-item/free-hands-next?1&lastid=%d" % (lastid)
        #url = "http://www.91meitu.net/img-item/get-next?1&lastid=%d" % (lastid)
        print '========\nlast id: %d'  % (lastid)
        json_str = urllib2.urlopen(url).read()
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
                realurl = "http://www.91meitu.net/userupload/orig/" + image['filename'];
                print 'realurl:' + realurl
                ps = os.path.split( image['filename'] );
                savedir = 'E:/91meitu/' + ps[0]
                if os.path.exists(savedir) == False:
                    print 'dir not exist'
                    os.makedirs(savedir)
                filepath = "E:/91meitu/" + image['filename'];
                print 'filepath:' + filepath
                try:
                    imgdata = urllib2.urlopen(realurl).read()
                except:
                    continue
                    
                f = file(filepath, 'wb')
                f.write(imgdata)
                f.close()
    except:
        continue
else:
    print 'all done, there is:%d pictures' % (allcount);
    
  
  
    
