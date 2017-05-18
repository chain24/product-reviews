#!/usr/bin/env python
# encoding=utf-8
import requests
import re
import codecs
import sys
from bs4 import BeautifulSoup
import MySQLdb


DOWNLOAD_URL = 'http://www.ebay.com/itm/142371326162'

def download_page(url):
    """获取url地址页面内容"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36'
    }
    data = requests.get(url, headers=headers).content
    return data

def check_pagination(doc):
    soup = BeautifulSoup(doc, 'html.parser')
    a = soup.find('a', attrs={'class': 'sar-btn right'}) #评论数超过5
    if a:
        page = a['href']
        return page
    else:
        return False
def get_li(doc):
    soup = BeautifulSoup(doc, 'html.parser')
    div = soup.find('div', class_='reviews')
    if div == None:
    	sys.exit('No reviews')   	
    name = []  # 买家
    star_con = []  # 星级
    score = []  # 评分
    info_list = []  # 短评
    info_title = [] #短评标题
    seller = [] #卖家
    time = [] #评论日期
    store = []
    for i in div.find_all('div',class_='ebay-review-section'):    
    	author = i.find('a', attrs={'class': 'review-item-author'}).get_text()
    	date = i.find('span', attrs={'class', 'review-item-date'}).get_text()
    	title = i.find('p', attrs={'class', 'review-item-title wrap-spaces'}).get_text()           	
    	p = i.find('p', attrs={'class', 'review-item-content rvw-wrap-spaces'})
        if p:
            content = p.get_text()
        else:
            body = i.find('p', attrs={'class', 'review-item-content wrap-spaces'})
            if body:
                content = body.get_text()
            else:
                content = 'None'                
        detail = i.find('p',attrs={'class', 'review-attr'})
    	rating = i.find('div',attrs={'class','ebay-star-rating'})
    	span = rating.find('span',attrs={'class', 'star-rating'})
    	li = span.find_all('i',attrs={'calss', 'fullStar'})
    	score.append(len(li))    	
    	if detail:
            for x in detail.find_all('span',attrs={'class', 'rvw-val'}):    	    
                store.append(x.get_text())
        else:
            store.append('None')        	
    	name.append(author)        
    	seller.append(store[-1])
    	info_list.append(content)
    	info_title.append(title)
    	time.append(date)
    a = soup.find('a', attrs={'class', 'spf-link'})  # 获取下一页
    ul = soup.find('ul', attrs={'class', 'large pagination'})
    if ul:
        li = ul.find_all('li')    
    pageSize = len(li) - 2
    if a:        
        return time, name, seller, info_list, info_title, score, a['href'], pageSize             
    else:
        return time, name, seller, info_list, info_title, score, None, None
def main():
    url = DOWNLOAD_URL
    custome = []
    review_title = []
    score = []
    sold_by = []
    review_body = []
    review_date = []    
    doc = download_page(url)
    page = check_pagination(doc)
    if page == False:
        date, name, seller, content, title, star_con, url, pageSize = get_li(doc)
    else:
        doc = download_page(page)
        date, name, seller, content, title, star_con, url, pageSize = get_li(doc)
        custome = custome + name
        review_title = review_title + title
        review_body = review_body + content
        score = score + star_con
        sold_by = sold_by + seller
        review_date = review_date + date
        if url:
            pageSize = pageSize + 1
            for i in xrange(2,pageSize):
                url = url.strip('&pgn=1')            
                nextPage = url + '&pgn=' + str(i)                      
                doc = download_page(nextPage)              
                date, name, seller, content, title, star_con, url, pageSize = get_li(doc)
                custome = custome + name
                review_title = review_title + title
                review_body = review_body + content
                score = score + star_con
                sold_by = sold_by + seller
                review_date = review_date + date
        print custome    
        sys.exit()
if __name__ == '__main__':
    main()
   