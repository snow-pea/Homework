# -*- coding: utf-8 -*-

import urllib2
import HTMLParser
import re

import datetime
import time

from bs4 import BeautifulSoup

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

#urlopen()
sock = urllib2.urlopen('http://www.eps.bnu.edu.cn/bbs/index.asp?boardid=376')
html = sock.read()
sock.close()

# parse html to get the main section
soup = BeautifulSoup(html, "html.parser")
posts = soup.findAll('tr')

file = open("last_update.txt", 'r')
lastupdate_string = file.read()
file.close()
                
Y,m,d,H,M,S = time.strptime(lastupdate_string, "%Y-%m-%d %H:%M:%S")[0:6]
latest = datetime.datetime(Y,m,d,H,M,S)

isfirst = 1
nomorenewpost = 0

for p in posts:
    li_subject=p.find('td',attrs={'class':'list2'})
    li_time = p.find('td', attrs={'class':'list5'})
    
    if li_subject!=None and li_time!=None:
    
        #subject
        subject = li_subject.a.text.strip()
        link = li_subject.a.get('href').strip()
        
        #post time
        a_time = li_time.find('a', attrs={'class':'font10'})
        timestring = a_time.text.strip()
        
        Y1,m1,d1,H1,M1,S1 = time.strptime(timestring, "%Y-%m-%d %H:%M:%S")[0:6]
        timestamp = datetime.datetime(Y1,m1,d1,H1,M1,S1 )

        if timestamp > latest:
            print '\n ------ ', subject, timestring, '\n'
            
            # crawl the new post
            html_post = urllib2.urlopen('http://www.eps.bnu.edu.cn/bbs/' + link).read()
            
            segments = re.split('<p>', html_post)
            for s in segments:
                if '</p>' in s and s.index('</p>')>1:
                    content = s[0:s.index('</p>')]
                    print content

                    # the first record is always on top
            if isfirst == 1:
                isfirst = 0
                file = open("last_update.txt", 'w')
                file.write(timestring)
                file.close()
            
# store a copy of the downloaded results
#file = open("GTrends_rawdata_%s.txt" % datetime.date.today(), 'w')
#file.write(homework)
#file.close()

# store the timestamp of latest published homework

