#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试收藏夹对话框的自动刷新功能
"""

import sys
import os

# 添加项目路径
sys.path.append(os.path.join(os.path.dirname(__file__), 'src', 'main'))

from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QPushButton, QWidget, QLabel
from PyQt5.QtCore import Qt

from collection_dialog import CollectionDialog
from newsmth_GUI import window

class TestWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("测试收藏夹自动刷新功能")
        self.setGeometry(100, 100, 800, 600)
        
        # 创建主窗口实例
        self.main_window = window()
        
        # 创建测试界面
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout()
        
        # 说明标签
        info_label = QLabel("测试收藏夹对话框的自动刷新功能")
        info_label.setAlignment(Qt.AlignCenter)
        info_label.setStyleSheet("font-size: 18px; font-weight: bold; margin: 20px;")
        layout.addWidget(info_label)
        
        # 测试按钮
        test_btn = QPushButton("打开收藏夹对话框")
        test_btn.setStyleSheet("font-size: 16px; padding: 15px; margin: 10px;")
        test_btn.clicked.connect(self.test_collection_dialog)
        layout.addWidget(test_btn)
        
        # 显示主窗口按钮
        show_main_btn = QPushButton("显示主界面")
        show_main_btn.setStyleSheet("font-size: 16px; padding: 15px; margin: 10px;")
        show_main_btn.clicked.connect(self.show_main_window)
        layout.addWidget(show_main_btn)
        
        central_widget.setLayout(layout)
    
    def test_collection_dialog(self):
        """测试收藏夹对话框"""
        print("打开收藏夹对话框...")
        
        # 创建收藏夹对话框
        collection_dialog = CollectionDialog()
        
        # 连接退出信号到主窗口的刷新方法
        if hasattr(self.main_window, 'refresh_favorite_boards'):
            collection_dialog.dialog_closed.connect(self.main_window.refresh_favorite_boards)
            print("信号已连接到主窗口的刷新方法")
        else:
            print("警告：主窗口没有refresh_favorite_boards方法")
        
        # 显示对话框
        collection_dialog.exec_()
        print("收藏夹对话框已关闭")
    
    def show_main_window(self):
        """显示主界面"""
        print("显示主界面...")
        self.main_window.show()

def main():
    app = QApplication(sys.argv)
    
    # 创建测试窗口
    test_window = TestWindow()
    test_window.show()
    
    print("测试程序启动")
    print("1. 点击'显示主界面'按钮查看主界面")
    print("2. 点击'打开收藏夹对话框'按钮测试收藏夹功能")
    print("3. 在收藏夹中添加或删除版面后关闭对话框")
    print("4. 观察主界面是否自动刷新")
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
