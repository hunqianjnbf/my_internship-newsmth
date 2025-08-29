import requests
import time
import threading
from bs4 import BeautifulSoup
import json
import Title_Time_Author_Scraping


class shuimu_craw:
    def __init__(self):
        self.dit = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 Edg/138.0.0.0"
        }
        self.content = []
        self.title = []
        self.zhuti = []
        self.images = []  # 新增：存储图片信息

        self.posts = []
        self.fetch_content()


    #字典get语法:从字典中获取 "键" 对应的 "值"。 字典.get("键","默认值")
    # 如果字典中存在这个 "键"，返回对应的值；
    # 如果字典中 不存在 这个 "键"，返回指定的 "默认值"。
    def get_image_data(self, image_url):
        try:
            print(f"正在获取图片数据: {image_url}")
            response = requests.get(image_url, headers=self.dit, timeout=10)
            response.raise_for_status()

            # 返回图片的二进制数据
            image_data = response.content
            print(f"图片数据获取成功: {len(image_data)} 字节")
            return image_data

        except Exception as e:
            print(f"获取图片数据失败 {image_url}: {str(e)}")
            return None

    def fetch_content(self):
        try:
            url = "https://m.newsmth.net/article/Botany/231676"
            r = requests.get(url, headers=self.dit)
            content = r.text
            soup = BeautifulSoup(content, "html.parser")

            ul_element = soup.find("ul", class_="list sec")
            if ul_element:
                #作者时间/跟帖人
                div_element0 = ul_element.find_all("div", class_="nav hl")
                if div_element0:
                    for div0 in div_element0:
                        div_text0 = div0.get_text(strip=True)
                        if div_text0:
                            self.title.append(div_text0)
                        else:
                            print("div_text0不正确")
                else:
                    print("div_element0不存在")

                #帖子内容
                div_element1 = ul_element.find_all("div", class_="sp")
                if div_element1:
                    for div1 in div_element1:
                        #如果有图片
                        if div1.find("a"):
                            div_text1 = div1.get_text(strip=True)
                            photo = div1.find("a").get("href")
                            photo_url ="https:"+photo
                            image_data = self.get_image_data(photo_url)
                            image_info = {
                                "url": photo_url,
                                "data": image_data,  # 图片的二进制数据
                            }
                            self.images.append(image_info)

                            if div_text1:
                                self.content.append(div_text1)
                            else:
                                self.content.append(f"[图片: {len(image_data) if image_data else 0} 字节]")
                        else:
                            div_text1 = div1.get_text(strip=True)
                            if div_text1:
                                self.content.append(div_text1)
                            else:
                                print("div_text1不正确")

                else:
                    print("div_element1不正确")

                # 新增：构建返回数据结构
                self.posts = [
                    {"主题": self.zhuti},
                    {"标题": self.title},
                    {"内容": self.content},
                    {"图片": self.images}  # 新增：图片信息
                ]


        except Exception as e:
            print(f"抓取失败{str(e)}")
            return False


if __name__ == "__main__":
    m = shuimu_craw()

    

