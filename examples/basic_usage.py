#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
基本使用示例
展示如何使用Web Scraping Toolkit的基本功能
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.scrapers.newsmth_scraper import NewsmthScraper
from src.login.newsmth_login import NewsmthLogin

def main():
    """基本使用示例"""
    print("=== Web Scraping Toolkit 基本使用示例 ===")
    
    # 创建爬虫实例
    scraper = NewsmthScraper()
    
    # 创建登录实例
    login = NewsmthLogin()
    
    # 示例：获取水木社区首页信息
    try:
        print("正在获取水木社区首页信息...")
        # 这里可以添加实际的爬取逻辑
        print("爬取完成！")
    except Exception as e:
        print(f"爬取失败: {e}")
    
    print("示例运行完成！")

if __name__ == "__main__":
    main()

