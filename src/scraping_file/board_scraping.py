# -*- coding: utf-8 -*-
import requests
import time
import threading
from bs4 import BeautifulSoup
import json  # 新增导入 json 模块

class banmian_craw:
    def __init__(self):
        self.dit = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 Edg/138.0.0.0"
        }
        self.banmian = {
            "社区管理": [],
            "国内院校": [],
            "休闲娱乐": [],
            "五湖四海": [],
            "游戏运动": [],
            "社会信息": [],
            "知性感性": [],
            "文化人文": [],
            "学术科学": [],
            "电脑技术": []
        }
        # 存储版面URL的字典
        self.board_urls = {}
        # 分类与页面编号的映射
        self.category_mapping = {
            "社区管理": 0,
            "国内院校": 1,
            "休闲娱乐": 2,
            "五湖四海": 3,
            "游戏运动": 4,
            "社会信息": 5,
            "知性感性": 6,
            "文化人文": 7,
            "学术科学": 8,
            "电脑技术": 9
        }
        self.fetch_banmian()

    def fetch_banmian(self):
        for category, page in self.category_mapping.items():
            page_url = f"https://m.newsmth.net/section/{page}"
            print(f"正在爬取分类: {category}")

            try:
                content = requests.get(page_url, headers=self.dit).text
                soup = BeautifulSoup(content, "html.parser")
                bankuai = soup.find("ul", {"class": "slist sec"})

                if not bankuai:
                    print(f"未找到版面列表: {category}")
                    continue

                li_elements = bankuai.find_all("li")

                for li in li_elements:
                    text = li.get_text(strip=True)

                    if self.is_directory(text):
                        # 如果是目录，递归爬取
                        dir_name = self.extract_name(text)
                        print(f"发现目录: {dir_name}")
                        dir_url = self.get_directory_url(li)
                        if dir_url:
                            self.crawl_directory(dir_url, category)

                    elif self.is_board(text):
                        # 如果是版面，直接添加
                        board_name = self.extract_name(text)
                        if board_name and board_name not in self.banmian[category]:
                            self.banmian[category].append(board_name)
                            # 获取版面URL
                            board_url = self.get_board_url(li)
                            if board_url:
                                self.board_urls[board_name] = board_url
                            print(f"添加版面: {board_name}")

            except Exception as e:
                print(f"抓取失败 {category}: {str(e)}")
                continue

        return self.banmian

    def is_directory(self, text):
        return "目录" in text
    
    def is_board(self, text):
        return "版面" in text
    
    def extract_name(self, text):
        if "|" in text:
            parts = text.split("|")
            if len(parts) >= 2:
                return parts[1].strip()
        return text.strip()
    
    def get_directory_url(self, li_element):
        try:
            a_tag = li_element.find("a")
            if a_tag and a_tag.has_attr('href'):
                href = a_tag['href']
                # 如果是相对路径，转换为完整URL(补链接)
                if href.startswith('/'):
                    return f"https://m.newsmth.net{href}"
                elif href.startswith('http'):
                    return href
                else:
                    return f"https://m.newsmth.net/{href}"
        except Exception as e:
            print(f"获取目录URL失败: {str(e)}")
        return None

    def get_board_url(self, li_element):
        try:
            a_tag = li_element.find("a")
            if a_tag and a_tag.has_attr('href'):
                href = a_tag['href']
                # 如果是相对路径，转换为完整URL
                if href.startswith('/'):
                    return f"https://m.newsmth.net{href}"
                elif href.startswith('http'):
                    return href
                else:
                    return f"https://m.newsmth.net/{href}"
        except Exception as e:
            print(f"获取版面URL失败: {str(e)}")
        return None

    def crawl_directory(self, directory_url, category):
        try:
            print(f"正在爬取目录: {directory_url}")
            content = requests.get(directory_url, headers=self.dit).text
            soup = BeautifulSoup(content, "html.parser")
            
            # 查找所有列表项
            bankuai = soup.find("ul", {"class": "slist sec"})
            if not bankuai:
                return
            
            li_elements = bankuai.find_all("li")
            
            for li in li_elements:
                # 获取完整的文本内容
                text = li.get_text(strip=True)
                
                if self.is_directory(text):
                    # 如果是目录，递归爬取
                    dir_name = self.extract_name(text)
                    print(f"发现目录: {dir_name}")
                    dir_url = self.get_directory_url(li)
                    if dir_url:
                        self.crawl_directory(dir_url, category)
                        
                elif self.is_board(text):
                    # 如果是版面，添加到结果中
                    board_name = self.extract_name(text)
                    if board_name and board_name not in self.banmian[category]:
                        self.banmian[category].append(board_name)
                        # 获取版面URL
                        board_url = self.get_board_url(li)
                        if board_url:
                            self.board_urls[board_name] = board_url
                        print(f"添加版面: {board_name}")
                        
        except Exception as e:
            print(f"爬取目录失败 {directory_url}: {str(e)}")

    def save_to_json(self, filename="bk_content1.json"):
        try:
            # 创建包含URL信息的完整数据结构
            complete_data = {
                "版面数据": self.banmian,
                "版面URL": self.board_urls
            }
            
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(complete_data, f, ensure_ascii=False, indent=4)
            print("已经转化成功")
            return True
        except Exception as e:
            print(f"转化失败{str(e)}")
            return False


if __name__ == "__main__":
    m = banmian_craw()
    m.save_to_json()