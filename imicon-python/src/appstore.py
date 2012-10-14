# -*- coding: utf-8 -*-
import urllib2
import json
import urlparse
from sqlalchemy import *
import time

# 根据appstore的链接获取此app的详细信息
def get_appinfo_with_ids( hrefs, tagid ):
#    try:
    for href in hrefs:
        print '------href:' + href + '------'
        patharray = urlparse.urlsplit(href).path.split('/')
        arraycount = len(patharray)
        appid = patharray[arraycount-1][2:]
        print '------抓取appid:' + appid + '------'
        #itunes look up url
        lookupurl = 'http://itunes.apple.com/lookup?id=%s' % (appid)
        json_str = urllib2.urlopen(lookupurl).read()
        # read
        result = (json.loads(json_str))['results']
        if len( result ) <= 0 :
            return
        appjson = result[0]
        iapp_title = appjson['trackName']
        iapp_logo = appjson['artworkUrl512']
        iapp_cate = appjson['primaryGenreName']
        iapp_cateid = appjson['primaryGenreId']
        rtime = time.strptime(appjson['releaseDate'], '%Y-%m-%dT%H:%M:%SZ')
        iapp_uptime = time.strftime('%Y-%m-%d %H:%M:%S', rtime) 
        iapp_price = appjson['price']
        iapp_pricetxt = appjson['currency']
        iapp_size = float(appjson['fileSizeBytes'])/1000000
        iapp_ver = appjson['version']
        iapp_founder = appjson['sellerName']
        iapp_age = appjson['trackContentRating']
        iapp_rate = 0
        if appjson.has_key( 'averageUserRatingForCurrentVersion' ):
            iapp_rate = appjson['averageUserRatingForCurrentVersion']
        elif appjson.has_key('averageUserRating'):
            iapp_rate = appjson['averageUserRating']
        iapp_ratecount = 0
        if appjson.has_key('userRatingCountForCurrentVersion'):
            iapp_ratecount = appjson['userRatingCountForCurrentVersion']
        elif appjson.has_key('userRatingCount'):
            iapp_ratecount = appjson['userRatingCount']
        iapp_allrate = 0
        if appjson.has_key('averageUserRating'):
            iapp_allrate = appjson['averageUserRating']
        iapp_allratecount = 0
        if appjson.has_key('userRatingCount'):
            iapp_allratecount = appjson['userRatingCount']
        iapp_detail = appjson['description']
        iapp_notes = appjson['releaseNotes']
        iapp_pics = appjson['screenshotUrls']
        for i in range(len(iapp_pics), 5):
            iapp_pics.append( None )
        iapp_padpics = appjson['ipadScreenshotUrls']
        for i in range( len(iapp_padpics), 6 ):
            iapp_padpics.append(None)
        iapp_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        # 写入数据库
        # DB
        engine = create_engine( 'mysql+pymysql://root:root@localhost:3306/apps?charset=utf8' )
        metadata = MetaData()
        metadata.bind = engine
        # 首先写入app到表中
        app_table = Table( 'app_info_copy', metadata, autoload=True )
        app_insert = app_table.insert().prefix_with('ignore')
        air = app_insert.execute( appID=appid, title=iapp_title, appLink=href, appLogo=iapp_logo, appCate=iapp_cate, 
                                  appCateCode=iapp_cateid,
                                  appUpTime=iapp_uptime, appPrice=iapp_price, appPriceTxt=iapp_pricetxt, appVersion=iapp_ver,
                                  appByte=iapp_size, appLang=1, appFounder=iapp_founder, appWebsite=iapp_founder, 
                                  appCopyright=iapp_founder, appAge=iapp_age,iosVersion='4.0', iosProduct=1, appRating=iapp_rate,
                                  appRatingCount=iapp_ratecount, appAllrating=iapp_allrate,  appAllratingCount=iapp_allratecount,
                                  appDetail=iapp_detail, appChangelog=iapp_notes, app_pic1=iapp_pics[0], app_pic2=iapp_pics[1],
                                  app_pic3=iapp_pics[2],app_pic4=iapp_pics[3],app_pic5=iapp_pics[4], ipad_pic1=iapp_padpics[0],
                                  ipad_pic2=iapp_padpics[1],ipad_pic3=iapp_padpics[2],ipad_pic4=iapp_padpics[3],
                                  ipad_pic5=iapp_padpics[4], ipad_pic6=iapp_padpics[5], addTime=iapp_time, upTime=iapp_time, 
                                  like_count=0, down_count=0)
        print '**app info inserted key:'+  str(air.inserted_primary_key)
        # 再次app和tag的对应关系插入到表中
        apptag_table = Table( 'app_tag', metadata, autoload=True )
        apptag_insert = apptag_table.insert().prefix_with('ignore')
        ati = apptag_insert.execute( app_id=appid, tag_id=tagid )
        print '**app tag inserted key:'+  str(ati.inserted_primary_key)
        # 
#    except Exception as x:
#        print 'exception:'
#        print x
#        continue
    

