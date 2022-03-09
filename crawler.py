from googlesearch import search
import requests as rs 
from bs4 import BeautifulSoup
import urllib3

target='蠱真人'   #目標書名
urllib3.disable_warnings()
target_list=[]
for page in range(2):
    url='https://www.ptt.cc/bbs/CFantasy/search?page=%d&q=%s'%(page,target)
    res=rs.session().get(url,verify=False)
    soup=BeautifulSoup(res.text,features="html.parser")
    for entry in soup.find_all("div",class_='r-ent'):    
        if target in entry.find('div',class_="title").text:
            target_list.append("https://www.ptt.cc/"+entry.find('a')['href'])

comments = []

for links in target_list:
    res=rs.session().get(links,verify=False)
    soup=BeautifulSoup(res.text,features="html.parser")
    metalines = soup.find_all("div", "article-metaline")
    # 回應內容
    bs_comments = soup.find_all("div", "push")
    if bs_comments:
        for c in bs_comments:
            # 處理 "檔案過大！部分文章無法顯示" 的 "warning-box" class
            if "warning-box" in c.get("class"):
                continue
            c_content = c.find("span", class_="push-content").get_text()
            comments.append(c_content.strip(": "))

with open('comment.txt','w',encoding='utf-8') as f:
    for comment in comments:
        f.writelines(comment+'\n')