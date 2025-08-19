import json
import requests
from bs4 import BeautifulSoup
with open ("favorites.json","r",encoding="utf-8") as f:
            data = json.load(f) #将文件对象 f 转换成 Python 数据类型（这里是字典）
board_detail = data.get("收藏的版块详情",[])
urls = []
names = []
content = [] #字典列表
link_all = [] #字典列表

for item in board_detail:
    url = item.get("url")
    name = item.get("name")
    if url:
        urls.append(url)
    if name:
        names.append(name)


        for url,name in zip(urls,names):
            try:
                r = requests.get(url)
                if r:
                    soup = BeautifulSoup(r.text,"html.parser")
                    ul_elements = soup.find_all("ul",class_="list sec")
                    for ul in ul_elements:
                        li_elements = ul.find_all("li")
                        if li_elements:
                            for li in li_elements:
                                div_elements = li.find_all("div")
                                if div_elements:
                                   #抓取文章标题
                                   title_div = div_elements[0]
                                   text0 = title_div.find("a")
                                   title = text0.get_text(strip=True) if text0 else ""
                                   link = text0.get("href")
                                   link_all.append(
                                       {
                                           "版面": name,
                                           "文章": f"https://m.newsmth.net/{link}"
                                       })


                                   if title == "版面积分变更记录":
                                       continue
                                   #抓取作者和时间
                                   info_div = div_elements[1]
                                   part = []

                                   for child in info_div.children:
                                       if child.name == "a":  #标签节点
                                           part.append(child.get_text(strip=True))
                                       else: #文本节点
                                           text = (child.get_text(strip=True)).replace("&nbsp;"," ")
                                           if text:
                                               part.append(text)

                                   post_time = part[0] if len(part)>=1 else ""
                                   author = part[1] if len(part)>=2 else ""
                                   content.append(
                                       {
                                           "版面": name,
                                           "标题": title,
                                           "作者": author,
                                           "时间": post_time,
                                       }
                                   )


            except Exception as e:
                print(f"爬取失败{str(e)}")


