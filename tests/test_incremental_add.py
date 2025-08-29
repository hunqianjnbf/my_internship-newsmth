#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os

def test_incremental_add():
    """测试增量添加功能"""
    print("=== 测试增量添加功能 ===")
    
    # 模拟当前收藏文件内容
    current_favorites = {
        "收藏的版块": [
            "社区管理 - 版主申请",
            "国内院校 - 北京邮电大学"
        ],
        "收藏的版块详情": [
            {
                "name": "社区管理 - 版主申请",
                "url": "https://m.newsmth.net/board/BM_Apply"
            },
            {
                "name": "国内院校 - 北京邮电大学",
                "url": "https://m.newsmth.net/BUPT"
            }
        ]
    }
    
    print(f"当前收藏版面: {current_favorites['收藏的版块']}")
    print(f"当前版面详情数量: {len(current_favorites['收藏的版块详情'])}")
    
    # 模拟用户新选择的版面（包含重复）
    new_boards = ["休闲娱乐 - 电影", "国内院校 - 北京邮电大学", "体育健身 - 游泳"]
    print(f"新选择版面: {new_boards}")
    
    # 执行增量添加逻辑
    existing_boards = current_favorites["收藏的版块"]
    combined_boards = existing_boards.copy()
    
    for new_board in new_boards:
        if new_board not in combined_boards:
            combined_boards.append(new_board)
            print(f"新增版面: {new_board}")
        else:
            print(f"版面已存在，跳过: {new_board}")
    
    print(f"合并前版面数量: {len(existing_boards)}")
    print(f"新增版面数量: {len(new_boards)}")
    print(f"合并后版面数量: {len(combined_boards)}")
    print(f"最终版面列表: {combined_boards}")
    
    # 模拟保存操作（保留原有详情）
    updated_favorites = {
        "收藏的版块": combined_boards,
        "收藏的版块详情": current_favorites["收藏的版块详情"]  # 完全保留原有详情
    }
    
    print(f"保存后的版面详情数量: {len(updated_favorites['收藏的版块详情'])}")
    print(f"版面详情: {updated_favorites['收藏的版块详情']}")
    
    # 验证结果
    expected_boards = ["社区管理 - 版主申请", "国内院校 - 北京邮电大学", "休闲娱乐 - 电影", "体育健身 - 游泳"]
    print(f"期望版面列表: {expected_boards}")
    print(f"增量添加正确: {combined_boards == expected_boards}")
    
    return updated_favorites

if __name__ == "__main__":
    result = test_incremental_add()
    print("\n=== 测试完成 ===")
    print("现在可以运行 collection_dialog.py 来测试实际的增量添加功能")
