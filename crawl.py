import requests
from bs4 import BeautifulSoup
import os
import time
from datetime import datetime

# 修改这里的起始日期，输出结果为日期内的所有省长和省委书记出现的新闻
# 输出结果为txt文档，包括标题和链接，按照时间从旧到新顺序排列
begin_year = 2024
begin_month = 7
begin_date = 22
end_year = 2024
end_month =7
end_date = 29
name1 = '许昆林'
name2 = '信长星'
user_agent="Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.6261.95 Safari/537.36"


def visit_website(html):
    soup = BeautifulSoup(html,'html.parser') #html.parser 为解析器
    title = soup('title') 
    soup = BeautifulSoup(html, 'html.parser', from_encoding="gb18030")
    paras = soup.select('p')
    result = False
    for i in range(len(paras)):
        #print(paras[i].text)
        if (name1 in paras[i].text) or (name2 in paras[i].text):
            result = True
            print('本段有省长或省委书记出现！')
    return result

def date_between(target_date):
    begin_diff = target_date - datetime(begin_year,begin_month,begin_date)
    end_diff = datetime(end_year,end_month,end_date) - target_date
    #print('begin:',begin_diff.days)
    #print('end:',end_diff.days)
    if (begin_diff.days >= 0) and (end_diff.days >= 0):
        return True
    else:
        return False

#函数1：请求网页
def page_def(url,ua):
    session = requests.session()
    session.headers = ua
    response = session.get(url=url)
    #print("响应头中set-cookie：",response.headers.get("set-cookie"))
    #print("会话现有cookie：",dict(session.cookies))
    response.encoding = response.apparent_encoding
    html = response.text
    #with open('test%d.txt'%(i),'w',encoding='utf-8') as f:
    #    f.write(html)
    return html

def time_date(str):
    format_pattern = '%Y-%m-%d  %H:%M'
    news_date = datetime.strptime(str , format_pattern)
    print(news_date)
    time_right = date_between(news_date)
    return time_right

def info_def(html):
    soup = BeautifulSoup(html,'html.parser') #html.parser 为解析器
    title = soup('title') 
    
    soup = BeautifulSoup(html, 'html.parser', from_encoding="gb18030")
    news = soup.find_all('div', class_='newslist')
    #print(news)   
    times = soup.select('div.newslist > ul > li > span')
    news_list = soup.select('div.newslist > ul > li > a')
    #print(news_list)
    #print(times)
    href_list=[]
    title_list=[]
    for i in range(len(news_list)):
        #print(news_list[i].text)
        #print(news_list[i]['href'])
        base_href = 'http://www.zgjssw.gov.cn/yaowen/'
        if news_list[i]['href'][0] != '.':
            print('该网址为视频链接，无需收录')
            continue
        target_href = base_href + news_list[i]['href']
        print(target_href)
        if time_date(times[i].text):
            print('该新闻在时效中')
        else:
            print('该新闻不在本周时效中，无需收录')
            continue
        href_list.append(target_href)
        title_list.append(news_list[i].text)
    
    #for i in range(len(sentence)):
    return [href_list,title_list]

if __name__ == '__main__':
    print("**************开始江苏政务网站爬虫********************")
    headers={"User-Agent":user_agent}#,"Cookie":cookie}
    now_date = datetime.now().strftime('%Y-%m-%d')
    result_file = open(now_date + '.txt','w',encoding='utf-8')
    news_dict = []
    for i in range(0,7):
        url = 'http://www.zgjssw.gov.cn/yaowen/index_%d.shtml'%(i)
        if i==0:
            url = 'http://www.zgjssw.gov.cn/yaowen/index.shtml'
        print(url)
        time.sleep(1)
        html = page_def(url,headers)
        href_list,title_list = info_def(html)
        #print(href_list)
        #print(title_list)
        for i in range(len(title_list)):
            sub_html = page_def(href_list[i],headers)
            if visit_website(sub_html):
                print('本文中有省长或省委书记出现，加入名单')
                print(title_list[i]+'\n'+href_list[i]+'\n\n')
                news_dict.append(title_list[i]+'\n'+href_list[i]+'\n\n')
            else:
                print('本文为无关文章，略去')
    for news_item in reversed(news_dict):
        result_file.write(news_item)
    result_file.close()     
