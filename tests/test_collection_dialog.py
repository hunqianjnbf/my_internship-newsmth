#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试收藏夹对话框
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src', 'main'))

from PyQt5.QtWidgets import QApplication
from collection_dialog import CollectionDialog

def main():
    app = QApplication(sys.argv)
    
    # 创建收藏夹对话框
    dialog = CollectionDialog()
    dialog.show()
    
    print("收藏夹对话框已打开，请查看收藏版面的显示效果")
    print("收藏的版面将以QLineEdit的形式垂直排列在滚动区域中")
    
    # 运行应用程序
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
