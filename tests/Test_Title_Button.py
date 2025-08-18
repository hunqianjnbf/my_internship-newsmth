# -*- coding: utf-8 -*-
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QScrollArea, QLabel, QSpacerItem, QSizePolicy
from PyQt5.QtCore import Qt

class TitleButtonTest(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        self.setWindowTitle("标题按钮测试")
        self.setGeometry(100, 100, 800, 600)
        
        # 标题按钮样式
        self.title_btn_style = """
            QPushButton {
                background-color: #ffffff;
                color: #333333;
                border: 2px solid #e0e0e0;
                border-radius: 8px;
                padding: 15px 20px;
                font-size: 16px;
                font-weight: 500;
                text-align: left;
                margin: 5px 0px;
            }
            QPushButton:hover {
                background-color: #f8f9fa;
                border-color: #007bff;
                color: #007bff;
            }
            QPushButton:pressed {
                background-color: #e9ecef;
                border-color: #0056b3;
                color: #0056b3;
            }
        """
        
        # 创建中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 创建滚动区域
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        
        # 创建滚动容器
        scroll_container = QWidget()
        scroll_layout = QVBoxLayout(scroll_container)
        scroll_layout.setAlignment(Qt.AlignTop)
        scroll_layout.setContentsMargins(20, 20, 20, 20)
        scroll_layout.setSpacing(10)
        
        # 添加标题
        title_label = QLabel("测试标题按钮")
        title_label.setStyleSheet("""
            QLabel {
                font-size: 20px;
                font-weight: bold;
                color: #333333;
                padding: 10px 0px;
                border-bottom: 2px solid #e0e0e0;
                margin-bottom: 10px;
            }
        """)
        title_label.setAlignment(Qt.AlignCenter)
        scroll_layout.addWidget(title_label)
        
        # 创建示例标题按钮
        sample_titles = [
            "这是第一个标题按钮 - 点击查看详情",
            "第二个标题按钮 - 包含更多内容信息",
            "第三个标题按钮 - 这是一个很长的标题用来测试换行效果",
            "第四个标题按钮 - 测试按钮样式和交互效果",
            "第五个标题按钮 - 验证滚动区域的功能",
            "第六个标题按钮 - 测试按钮的悬停和点击效果",
            "第七个标题按钮 - 确保所有按钮都能正常工作",
            "第八个标题按钮 - 测试按钮的布局和间距",
            "第九个标题按钮 - 验证按钮的响应性",
            "第十个标题按钮 - 最后一个测试按钮"
        ]
        
        for i, title in enumerate(sample_titles, 1):
            btn = QPushButton(f"{i}. {title}")
            btn.setStyleSheet(self.title_btn_style)
            btn.setMinimumHeight(60)
            btn.setMaximumHeight(80)
            btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            btn.clicked.connect(lambda checked, t=title: self.on_title_clicked(t))
            scroll_layout.addWidget(btn)
            
            # 添加间距
            spacer = QSpacerItem(20, 5, QSizePolicy.Minimum, QSizePolicy.Fixed)
            scroll_layout.addItem(spacer)
        
        # 设置滚动区域
        scroll_area.setWidget(scroll_container)
        
        # 创建主布局
        main_layout = QVBoxLayout(central_widget)
        main_layout.addWidget(scroll_area)
        
    def on_title_clicked(self, title):
        """标题按钮点击事件"""
        print(f"点击了标题: {title}")
        # 这里可以添加点击标题后的处理逻辑

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = TitleButtonTest()
    window.show()
    sys.exit(app.exec_()) 