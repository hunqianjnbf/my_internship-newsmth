#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试收藏追加功能的脚本
"""

import json
import os

def test_append_functionality():
    """测试收藏追加功能"""
    
    # 测试文件路径
    test_file = "test_favorites.json"
    
    # 清理之前的测试文件
    if os.path.exists(test_file):
        os.remove(test_file)
    
    print("=== 测试收藏追加功能 ===\n")
    
    # 第一次收藏
    print("1. 第一次收藏：")
    first_favorites = {
        "收藏的版块": ["社区管理 - 会议室管理"],
        "收藏的版块详情": [
            {
                "name": "社区管理 - 会议室管理",
                "url": "https://m.newsmth.net/board/RoomManager"
            }
        ]
    }
    
    with open(test_file, 'w', encoding='utf-8') as f:
        json.dump(first_favorites, f, ensure_ascii=False, indent=2)
    
    print(f"   保存内容: {first_favorites['收藏的版块']}")
    
    # 第二次收藏（追加）
    print("\n2. 第二次收藏（追加）：")
    try:
        # 读取现有数据
        with open(test_file, 'r', encoding='utf-8') as f:
            existing_data = json.load(f)
        
        # 新的收藏内容
        new_boards = ["技术讨论 - Python编程", "生活休闲 - 美食天地"]
        new_details = [
            {
                "name": "技术讨论 - Python编程",
                "url": "https://m.newsmth.net/board/Python"
            },
            {
                "name": "生活休闲 - 美食天地",
                "url": "https://m.newsmth.net/board/Food"
            }
        ]
        
        # 合并现有数据和新数据
        existing_boards = existing_data.get("收藏的版块", [])
        existing_details = existing_data.get("收藏的版块详情", [])
        
        # 避免重复
        for board in new_boards:
            if board not in existing_boards:
                existing_boards.append(board)
        
        for detail in new_details:
            if detail not in existing_details:
                existing_details.append(detail)
        
        # 保存合并后的数据
        final_data = {
            "收藏的版块": existing_boards,
            "收藏的版块详情": existing_details
        }
        
        with open(test_file, 'w', encoding='utf-8') as f:
            json.dump(final_data, f, ensure_ascii=False, indent=2)
        
        print(f"   新增内容: {new_boards}")
        print(f"   最终内容: {existing_boards}")
        
    except Exception as e:
        print(f"   追加失败: {e}")
    
    # 第三次收藏（再次追加）
    print("\n3. 第三次收藏（再次追加）：")
    try:
        # 读取现有数据
        with open(test_file, 'r', encoding='utf-8') as f:
            existing_data = json.load(f)
        
        # 新的收藏内容
        new_boards = ["技术讨论 - 机器学习", "社区管理 - 会议室管理"]  # 第二个是重复的
        new_details = [
            {
                "name": "技术讨论 - 机器学习",
                "url": "https://m.newsmth.net/board/ML"
            },
            {
                "name": "社区管理 - 会议室管理",  # 重复的
                "url": "https://m.newsmth.net/board/RoomManager"
            }
        ]
        
        # 合并现有数据和新数据
        existing_boards = existing_data.get("收藏的版块", [])
        existing_details = existing_data.get("收藏的版块详情", [])
        
        # 避免重复
        for board in new_boards:
            if board not in existing_boards:
                existing_boards.append(board)
                print(f"   新增版面: {board}")
            else:
                print(f"   跳过重复版面: {board}")
        
        for detail in new_details:
            if detail not in existing_details:
                existing_details.append(detail)
                print(f"   新增详情: {detail['name']}")
            else:
                print(f"   跳过重复详情: {detail['name']}")
        
        # 保存合并后的数据
        final_data = {
            "收藏的版块": existing_boards,
            "收藏的版块详情": existing_details
        }
        
        with open(test_file, 'w', encoding='utf-8') as f:
            json.dump(final_data, f, ensure_ascii=False, indent=2)
        
        print(f"   最终内容: {existing_boards}")
        
    except Exception as e:
        print(f"   追加失败: {e}")
    
    # 显示最终结果
    print("\n4. 最终结果：")
    try:
        with open(test_file, 'r', encoding='utf-8') as f:
            final_data = json.load(f)
        
        print(f"   收藏的版块数量: {len(final_data['收藏的版块'])}")
        print(f"   收藏的版块详情数量: {len(final_data['收藏的版块详情'])}")
        print(f"   所有版块: {final_data['收藏的版块']}")
        
    except Exception as e:
        print(f"   读取最终结果失败: {e}")
    
    # 清理测试文件
    if os.path.exists(test_file):
        os.remove(test_file)
        print(f"\n已清理测试文件: {test_file}")
    
    print("\n=== 测试完成 ===")

if __name__ == "__main__":
    test_append_functionality()
