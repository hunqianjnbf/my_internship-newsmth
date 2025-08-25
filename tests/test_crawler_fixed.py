#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试修复后的爬虫代码
"""

import sys
import os
import time

# 添加src/main目录到Python路径
sys.path.append(os.path.join(os.path.dirname(__file__), 'src', 'main'))

def test_crawler():
    """测试爬虫功能"""
    try:
        from newsmth_GUI import favorite_posts_content_craw
        print("✅ 成功导入 favorite_posts_content_craw 类")
        
        # 创建爬虫实例
        crawler = favorite_posts_content_craw()
        print("✅ 成功创建爬虫实例")
        
        # 测试URL（这是一个示例URL，你需要替换为实际的帖子URL）
        test_url = "https://m.newsmth.net/article/JobExpress/single/5b4b4b4b/0"
        
        print(f"🔗 测试URL: {test_url}")
        print("="*50)
        
        # 记录开始时间
        start_time = time.time()
        
        # 测试爬取功能
        result = crawler.fetch_content(test_url)
        
        # 记录结束时间
        end_time = time.time()
        elapsed_time = end_time - start_time
        
        if result:
            print("✅ 爬取成功！")
            print(f"⏱️  总耗时: {elapsed_time:.2f} 秒")
            print(f"📋 主题: {result.get('theme', 'N/A')}")
            print(f"📝 帖子数量: {len(result.get('posts', []))}")
            
            # 显示前几个帖子的信息
            for i, post in enumerate(result.get('posts', [])[:3]):
                print(f"\n📄 帖子 {i+1}:")
                print(f"   🏷️  类型: {post.get('type', 'N/A')}")
                print(f"   📌 标题: {post.get('title', 'N/A')}")
                print(f"   💬 内容长度: {len(post.get('content', ''))}")
                print(f"   🖼️  图片数量: {len(post.get('images', []))}")
                
                # 显示图片信息
                if post.get('images'):
                    for j, img in enumerate(post['images'][:2]):  # 只显示前2张图片
                        print(f"     🖼️  图片 {j+1}: {img.get('url', 'N/A')}")
                        print(f"        📊 数据大小: {len(img.get('data', b'')) if img.get('data') else 'None'} bytes")
        else:
            print("❌ 爬取失败")
            
    except Exception as e:
        print(f"❌ 测试过程中出错: {e}")
        import traceback
        traceback.print_exc()

def test_basic_functionality():
    """测试基本功能"""
    print("🧪 测试基本功能...")
    
    try:
        import requests
        from bs4 import BeautifulSoup
        
        # 测试网络连接
        url = "https://m.newsmth.net/"
        headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 Edg/138.0.0.0"
        }
        
        print(f"🌐 测试网络连接: {url}")
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            print(f"✅ 网络连接正常，状态码: {response.status_code}")
            print(f"📄 页面大小: {len(response.text)} 字符")
            
            # 解析页面
            soup = BeautifulSoup(response.text, "html.parser")
            title = soup.find("title")
            if title:
                print(f"📋 页面标题: {title.get_text(strip=True)}")
            
            # 查找页面信息元素
            page_info = soup.find("a", class_="plant")
            if page_info:
                print(f"📊 找到页面信息元素: {page_info.get_text(strip=True)}")
            else:
                print("⚠️  未找到页面信息元素")
                
        else:
            print(f"❌ 网络连接失败，状态码: {response.status_code}")
            
    except Exception as e:
        print(f"❌ 基本功能测试失败: {e}")

if __name__ == "__main__":
    print("🚀 开始测试修复后的爬虫代码")
    print("="*60)
    
    # 测试基本功能
    test_basic_functionality()
    
    print("\n" + "="*60)
    
    # 测试爬虫功能
    test_crawler()
    
    print("\n" + "="*60)
    print("🎯 测试完成！")

