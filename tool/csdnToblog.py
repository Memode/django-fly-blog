#coding:utf-8
import re,urllib,urllib2,os
import MySQLdb
from bs4 import BeautifulSoup
import datetime
import hashlib
hostUrl="http://blog.csdn.net/cq361106306"
re_getPage=re.compile(r'共(.*?)页')
re_getUrlByPage=re.compile(r'class="link_title"><a href=".*?">')
re_getUrlByPage2=re.compile(r'class="link_title"><a href="(.*?)">')
re_getCategory=re.compile(r'panel_Category.*?div',re.S)
re_getCategory2=re.compile(r'href=".*?" onclick.*>.*<')
re_getCategory3=re.compile(r'href="(.*)" onclick.*?>(.*?)<')
def getReadByUrl(url):
    headers={
            'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:14.0) Gecko/20100101 Firefox/14.0.1', 
            }
    req=urllib2.Request(url,headers=headers)
    return urllib2.urlopen(req).read()
def getPageByCategory(url):
    urldata=getReadByUrl(url)
    #共多少页
    data=re_getPage.search(urldata)
    if data:
        return data.group(1)
    else:
        return 1
def getUrlByPage(url):
    urldata=getReadByUrl(url)
    data=re_getUrlByPage.findall(urldata)
    articleUrl=[]
    for div in data:
        urlLst=re_getUrlByPage2.search(div)
        articleUrl.append('http://blog.csdn.net'+urlLst.group(1))
    return articleUrl

def getCategory():
    category=getReadByUrl(hostUrl)
    data=re_getCategory.findall(category)
    dataUrlList=re_getCategory2.findall(data[1]) 
    urlLst=[]
    nameLst=[]
    for div in  dataUrlList:
        data=re_getCategory3.search(div)
        urlLst.append(data.group(1))
        nameLst.append(data.group(2))
    return urlLst,nameLst

def getArticleByUrl(url):
    data=getReadByUrl(url)
    soup = BeautifulSoup(data)
    title=soup.find_all('span',attrs={"class":"link_title"})
    title=re.search(r'href.*?>(.*?)<',str(title[0]),re.S)
    title=title.group(1).strip()
    #print title
    content=re.search(r'class="article_content">(.*)</div>.*Baidu Button BEGIN.*bdsharebuttonbox',data,re.S)
    content=content.group(1)
    #print content
    tag=re.findall(r'blog_articles_tag.*?</a>',data,re.S)
    tags=''
    for t in tag:
        tags+=re.search(r'blog_articles_tag.*?>(.*?)</a>',t,re.S).group(1)+','
    tags=tags[:-1]
    return title,tags,content

def sqlExeCategory(category):
    #search and insert category
    try:
        conn=MySQLdb.connect(host='localhost',user='root',passwd='199288',db='flyblog',port=3306,charset='utf8')
        cur=conn.cursor()
        cur.execute('select * from blog_category where name=%s',[category])
        result=cur.fetchone()
        if not result:
            print '分类%s不存在'% category
            print '创建分类中..'
            cur.execute('''insert into blog_category(`name`,`alias`,`is_nav`,`desc`,`rank`,`status`,`create_time`,`update_time`)  
                    values(%s,%s,0,%s,0,0,now(),now())''',
                    [category,category,category])
        else:
            print '分类已经存在,继续'
        conn.commit()
        cur.close()     
        conn.close()
    except MySQLdb.Error,e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])

def sqlExeArticle(category,name=None,tags=None,content=None):
    try:
        conn=MySQLdb.connect(host='localhost',user='root',passwd='199288',db='flyblog',port=3306,charset='utf8')
        cur=conn.cursor()
        cur.execute('select id from blog_category where name=%s',[category])
        result=cur.fetchone()
        id=result[0]
        cur.execute('''insert into blog_post(`author_id`,`category_id`,`title`,`alias`,`is_top`,`summary`
                    ,`content`,`content_html`,`view_times`,`tags`,`status`,`is_old`,`pub_time`,`create_time`,`update_time`)  
                    values(1,%s,%s,%s,0,%s,%s,%s,1,%s,0,0,now(),now(),now())''',
                    [id,name,hashlib.md5(name).hexdigest(),content[0:min(len(content), 200)],content
                        ,content,tags])
        conn.commit()
        cur.close()     
        conn.close()
    except MySQLdb.Error,e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
if __name__ == "__main__":
    url,name= getCategory()
    cat=0
    urllen=len(url)
    flag='1'
    while cat<urllen and flag=='1':
        count=int(getPageByCategory(url[cat]))
        print '开始分类',name[cat]
        sqlExeCategory(name[cat])
        print '共有页数',count
        i=0
        while i<count:
            articleUrlList= getUrlByPage(url[cat]+'/'+str(i+1))
            print '该分类第%d页共有:%d文章'%(i+1,len(articleUrlList))
            for articleUrl in articleUrlList:
                title,tags,content=getArticleByUrl(articleUrl)
                print '开始读取文章:',title
                sqlExeArticle(name[cat],title,tags,content)
                print '文章写入成功',title
            i+=1
        cat+=1
        flag=raw_input('是否继续? 1 or 0')

