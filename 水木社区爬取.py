import requests
import time
import threading
from bs4 import BeautifulSoup
import json  # 新增导入 json 模块


class shuimu_craw:
    def __init__(self):
        self.dit = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 Edg/138.0.0.0"
        }
        self.banmian = []
        self.fetch_banmian()


    def fetch_banmian(self):
        self.banmian = []
        for page in range(0, 10):
            page_url = f"https://m.newsmth.net/section/{page}"
            try:
                content = requests.get(page_url, headers=self.dit).text
                soup = BeautifulSoup(content, "html.parser")
                bankuai = soup.find("ul", {"class": "slist sec"}).find_all("li", {"class": "hl"})
                if bankuai:
                    for li in bankuai:
                        title = li.find("a")
                        text = title.get_text(strip=True)
                        self.banmian.append(text)
                        print(text)
            except Exception as e:
                print(f"抓取失败{str(e)}")
                return False
        return self.banmian
    def save_to_json(self,filename="bankuai_content.json"):
        try:
            with open(filename, "w",encoding="utf-8") as f:
                json.dump(self.banmian,f,ensure_ascii=False,indent=4)
            print("已经转化成功")
            return True
        except Exception as e:
            print(f"转化失败{str(e)}")
            return False




if __name__ == "__main__":
    m = shuimu_craw()
    m.save_to_json()
    # 调用存储方法