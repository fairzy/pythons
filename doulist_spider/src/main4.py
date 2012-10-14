# -*- coding: utf-8 -*-
import urllib2
import json
from sqlalchemy import *
from BeautifulSoup import BeautifulSoup
import re
import string
import mylog4

def getUserId( href ):
    tmparray = href.split('/')
    count = len( tmparray )
    if href[count-1] == '/':
        uid = tmparray[count-2]
    else:
        uid = tmparray[count-1]
    return uid
    
def getUserName( oname ):
    try:
        pos = oname.index('(')
        return oname[0:pos]
    except:
        return oname
def getTime( timestr ):
    find= re.compile(r'\d+\-\d+\-\d+\s\d+:\d+:\d+').findall(timestr)
    if find:
        if len(find) < 2:
            find.append('0000-00-00 00:00:00')
        return find
    else:
        return None
    
def getAndSaveUserInfo(userid):
    api = 'http://api.douban.com/people/%s?alt=json' % userid
    logger.info( 'save user:' + userid)
    json_str = urllib2.urlopen(api).read()
    obj = json.loads(json_str)
    u_uid = userid
    u_sig = obj['db:signature']['$t']
    if hasattr(obj, 'db:location'):
        u_loc_t = obj['db:location']['$t']
        u_loc_i = obj['db:location']['@id']
    else:
        u_loc_t = None
        u_loc_i = None
    u_title = obj['title']['$t']
    u_id = getUserId( obj['id']['$t'] )
    u_content = obj['content']['$t']
    u_icon = obj['link'][2]['@href']
    # 写入数据库
    engine = create_engine( 'mysql+pymysql://dadmin:admin@localhost:3306/douban?charset=utf8' )
    metadata = MetaData()
    metadata.bind = engine
    user_table = Table( 'user', metadata, autoload=True )
    user_insert = user_table.insert().prefix_with('ignore')
    # insert
    ir = user_insert.execute( uid=u_uid, id=u_id, title=u_title, signature=u_sig, content=u_content, icon=u_icon,\
                              location=u_loc_t, loc_id=u_loc_i )
    logger.info( 'user inserted key:'+  str(ir.inserted_primary_key) )
    
    
if '__main__' == __name__:
    logger= mylog4.initlog()
    list_id = 560000
             #366716
    baseurl = 'movie'
    response = None;
    while True:
        logger.info( '-----------------------------------------')
        list_id = list_id + 1
        url = 'http://%s.douban.com/doulist/%d/' % (baseurl, list_id)
        logger.info('visit: ' + url)
        try:
            ###########################################################
            #html = urllib2.urlopen(url).read()
            textdata = None
            rheaders = {
                       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                       'Accept-Charset':'GBK,utf-8;q=0.7,*;q=0.3',
                       'Accept-Encoding':'gzip,deflate,sdch',
                       'Accept-Language':'zh-CN,zh;q=0.8',
                       'Connection' : 'keep-alive',
                       #'Referer' :'http://book.douban.com/',
                       'Host' : ('%s.douban.com' % baseurl),
                       #'DK_AJAX_REQUEST':'ajax-reqeust',
                       'Cookie':'bid="bid="Ic2C4NAhWaI"; __gads=ID=e38f104e6dc35ced:T=1340953376:S=ALNI_MYsJjJ81NjFi8hLqB1dib_-wzDk_w; ll="118281"; viewed="4920528_2002743_3908071_4218768"; regfromurl=http://movie.douban.com/photos/photo/1506180982/#next_photo; regfromtitle=%E9%82%A3%E4%BA%9B%E5%B9%B4%EF%BC%8C%E6%88%91%E4%BB%AC%E4%B8%80%E8%B5%B7%E8%BF%BD%E7%9A%84%E5%A5%B3%E5%AD%A9%20%E5%89%A7%E7%85%A7; ue="fancylst6@163.com"; __utma=30149280.734334845.1341813661.1341813661.1341813661.1; __utmb=30149280.79.10.1341813661; __utmc=30149280; __utmz=30149280.1341813661.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utmv=30149280.289; __utma=81379588.655389362.1341202315.1341552275.1341813715.9; __utmb=81379588.34.8.1341820002464; __utmc=81379588; __utmz=81379588.1341472908.5.3.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/group/topic/9975616/; RT=s=1341820007999&r=http%3A%2F%2Fbook.douban.com%2Fdoulist%2F10977%2F',
                       'User-Agent':'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.47 Safari/536.11'
                       }
            opener = urllib2.build_opener()
            urllib2.install_opener(opener)
            request = urllib2.Request(url, textdata, rheaders)
            response = urllib2.urlopen(request)
            fheader = response.info()
            print 'realurl' + response.geturl()
            rawdata = response.read()
            if ('Content-Encoding' in fheader and fheader['Content-Encoding']) or \
            ('content-encoding' in fheader and fheader['content-encoding']):
                import gzip
                import StringIO
                data = StringIO.StringIO(rawdata)
                gz = gzip.GzipFile(fileobj=data)
                rawdata = gz.read()
                gz.close()
            ########################################################33
            # soup 
            html =  rawdata
            soup = BeautifulSoup( html )
            # 找到header, 根据header判断是电影还是图书
            nav_header = soup.find('div', {'class':'site-nav'})
            ttype = nav_header['id']
            if ttype == 'db-nav-movie':
                list_type = 1
            elif ttype == 'db-nav-book':
                list_type = 0
            else:
                list_type = -1
            # 豆列name
            list_name = soup.h1.string
            logger.info( 'list_name:' + list_name )
            # 创建者id, name
            usera = soup.find('div', {'class':'col2_doc_text'}).next.next.next
            print usera
            uesrhref = usera['href']
            user_id = getUserId(uesrhref)
            #
            user_name = getUserName(usera.string)
            # 创建时间/更新时间
            timestr = usera.next.next.next
            list_time = getTime(timestr)
            # 推荐数
            rec_ele = soup.find('span', {'class':'rec-num'})
            if hasattr(rec_ele, 'string'):
                rec_str = rec_ele.string
            else:
                rec_str = u'0人'
            print rec_str
            list_rec = string.atoi( rec_str[:(len(rec_str)-1)] )
            # 介绍
            introele = soup.find('p', {'class':'indent'})
            
            ################# 写数据库 #################
            # 取用户信息并写入数据库
            getAndSaveUserInfo(user_id)
            # 写入doulist信息
            # 写入数据库
            engine = create_engine( 'mysql+pymysql://dadmin:admin@localhost:3306/douban?charset=utf8' )
            metadata = MetaData()
            metadata.bind = engine
            doulist_table = Table( 'doulist', metadata, autoload=True )
            list_insert = doulist_table.insert().prefix_with('ignore')
            # insert
            ir = list_insert.execute( id=list_id, name=unicode(list_name), type=list_type, author_id=user_id, rec_count=list_rec,\
                                      like_count=0, desc=unicode(introele), create_date=list_time[0], update_date=list_time[1] )
        
            logger.info( 'doulist inserted key:'+  str(ir.inserted_primary_key))
        

        except urllib2.HTTPError, ex:
            print 'oldbase:' + baseurl
            if ex.code == 301 :
                if baseurl == 'movie':
                    baseurl = 'book'
                elif baseurl == 'book':
                    baseurl = 'www'
                else:
                    baseurl = 'movie'
                    logger.error( 'jump:' + baseurl )
                    continue
                list_id = list_id - 1
                logger.error( 'redirect:' + baseurl )
            logger.error( 'rquest url error, code:%d' % ex.code)
        except Exception as e:
            logger.error('unknow Error'+ str(e))
    
    logger.info( '============END==============')

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    