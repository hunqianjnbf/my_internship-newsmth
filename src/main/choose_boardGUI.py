import sys
import json
import os

from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QApplication, QDialog, QLabel, QPushButton, 
                             QVBoxLayout, QHBoxLayout, QLineEdit, QScrollArea, 
                             QWidget, QCheckBox, QFrame, QMessageBox, QGroupBox)

class banmian(QDialog):
    # 添加信号，用于通知主界面刷新
    favorites_updated = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.selected_items = set()  # 存储用户选择的项目
        self.board_data = {}  # 存储版块数据
        self.btn_style()
        self.init_ui()
        self.load_board_data()
        self.btn_style()
        self.update_favorite_list()

    def btn_style(self):
        self.btn_style1 = ("""
            QPushButton {
                font-size: 22px;
                padding: 8px 20px;
                border: 1px solid #ddd;
                border-radius: 5px;
                background-color: #f8f9fa;
                color: #333;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #e9ecef;
                border-color: #007bff;
            }
            QPushButton:pressed {
                background-color: #dee2e6;
            }
        """)

        self.confirm_btn_style = ("""
            QPushButton {
                font-size: 14px;
                padding: 8px 20px;
                border: 1px solid #007bff;
                border-radius: 5px;
                background-color: #007bff;
                color: white;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #0056b3;
                border-color: #004085;
            }
            QPushButton:pressed {
                background-color: #004085;
            }
        
        """)
        self.title_label_style = ("""
                    font-size: 24px;
                    font-weight: bold;
                    color: #2c3e50;
                    padding: 20px;
                    background-color: #e9ecef;
                    border-radius: 8px;
                    margin: 10px;
                """)
        self.search_edit_style = ("""
                    QLineEdit {
                        font-size: 22px;
                        padding: 8px 12px;
                        border: 1px solid #ddd;
                        border-radius: 5px;
                        background-color: white;
                        min-height: 20px;
                    }
                    QLineEdit:focus {
                        border-color: #007bff;
                    }
                """)
        self.board_scroll_style = ("""
                    QScrollArea {
                        border: 1px solid #ddd;
                        border-radius: 5px;
                        background-color: white;
                    }
                """)
        self.favorite_label_style = ("""
                    font-size: 22px;
                    font-weight: bold;
                    color: #2c3e50;
                    padding: 8px;
                    background-color: #d4edda;
                    border-radius: 5px;
                """)
        self.favorite_scroll_style = ("""
                    QScrollArea {
                        border: 1px solid #ddd;
                        border-radius: 5px;
                        background-color: white;
                    }
                """)
        self.add_favorite_btn_style = ("""
                    QPushButton {
                        background-color: #d4edda;
                        color: black;
                        border: black;
                        border-radius: 5px;  
                        padding: 8px 14px;
                        font-size: 28px;
                    }
                    QPushButton:hover {
                        background-color: #D3D3D3;
                    }
                    }
                """)
        self.title_label1_style = ("""
                        QLabel {
                            font-size: 22px;
                            font-weight: bold;
                            color: #2c3e50;
                            padding: 10px 15px;
                            background-color: #e9ecef;
                            border-radius: 8px;
                            margin: 5px 0px;
                            border: 1px solid #dee2e6;
                        }
                    """)
        self.checkbox_style = ("""
                            QCheckBox {
                                font-size: 22px;
                                color: #495057;
                                padding: 8px 10px;
                                border-radius: 6px;
                                margin: 3px;
                                min-width: 110px;
                                max-width: 130px;
                                background-color: #ffffff;
                                border: 1px solid #e9ecef;
                            }
                            QCheckBox:hover {
                                background-color: #f8f9fa;
                                border: 1px solid #007bff;
                                color: #007bff;
                            }
                            QCheckBox:checked {
                                background-color: #e3f2fd;
                                border: 1px solid #2196f3;
                                color: #1976d2;
                                font-weight: bold;
                            }
                        """)
        self.content_scroll_style = ("""
                        QScrollArea {
                            border: 1px solid #dee2e6;
                            border-radius: 5px;
                            background-color: white;
                            margin: 5px 0px;
                        }
                    """)

    def init_ui(self):
        self.setWindowTitle('水木社区版面选择')
        self.setWindowIcon(QIcon('C:/Users/17256/PycharmProjects/pythonProject/picture/logo.ico'))
        self.setFixedSize(1600, 1090)
        self.setStyleSheet("""
            QDialog {
                background-color: #f8f9fa;
            }
        """)
        
        layout = QVBoxLayout()

        # 标题
        self.title_label = QLabel("版面收藏选择")
        self.title_label.setStyleSheet(self.title_label_style)
        self.title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.title_label)

        # 主内容区域
        main_layout = QHBoxLayout()

        # 左侧：版块选择区域
        left_widget = QWidget()
        left_layout = QVBoxLayout()

        # 搜索框
        search_layout = QHBoxLayout()
        search_label = QLabel("搜索版面:")
        search_label.setStyleSheet("font-size: 18px; color: #555; font-weight: bold;")
        
        self.search_edit = QLineEdit()
        self.search_edit.setPlaceholderText("输入关键词搜索版面...")
        self.search_edit.setStyleSheet(self.search_edit_style)

        self.search_edit.textChanged.connect(self.filter_boards)
        
        search_layout.addWidget(search_label)
        search_layout.addWidget(self.search_edit)
        left_layout.addLayout(search_layout)
        
        # 版块滚动区域
        self.board_scroll = QScrollArea()
        self.board_scroll.setWidgetResizable(True)
        self.board_scroll.setStyleSheet(self.board_scroll_style)

        
        self.board_container = QWidget()
        self.board_layout = QVBoxLayout()
        self.board_container.setLayout(self.board_layout)
        self.board_scroll.setWidget(self.board_container)
        left_layout.addWidget(self.board_scroll)
        
        left_widget.setLayout(left_layout)
        main_layout.addWidget(left_widget,2)  # 占2份空间

        # 右侧：收藏区域
        right_widget = QWidget()
        right_layout = QVBoxLayout()

        # 收藏区域标题
        self.favorite_label = QLabel("已选择的版面")
        self.favorite_label.setStyleSheet(self.favorite_label_style)
        self.favorite_label.setAlignment(Qt.AlignCenter)
        right_layout.addWidget(self.favorite_label)

        # 收藏滚动区域 - 设置固定高度确保布局稳定
        self.favorite_scroll = QScrollArea()
        self.favorite_scroll.setWidgetResizable(True)
        self.favorite_scroll.setStyleSheet(self.favorite_scroll_style)

        
        self.favorite_container = QWidget()
        self.favorite_layout = QVBoxLayout()
        self.favorite_layout.setSpacing(3)  # 减小间距
        self.favorite_layout.setContentsMargins(10, 10, 10, 10)  # 设置边距
        self.favorite_layout.setAlignment(Qt.AlignTop)  # 确保内容从顶部开始排列
        self.favorite_container.setLayout(self.favorite_layout)
        self.favorite_scroll.setWidget(self.favorite_container)
        right_layout.addWidget(self.favorite_scroll)
        
        # 添加收藏按钮
        self.add_favorite_btn = QPushButton("添加收藏")
        self.add_favorite_btn.setStyleSheet(self.add_favorite_btn_style)

        self.add_favorite_btn.clicked.connect(self.save_favorites_to_json)
        right_layout.addWidget(self.add_favorite_btn)
        
        right_widget.setLayout(right_layout)
        main_layout.addWidget(right_widget, 1)  # 占1份空间
        
        layout.addLayout(main_layout)
        # 底部按钮
        button_layout = QHBoxLayout()
        
        self.refresh_btn = QPushButton("刷新")
        self.refresh_btn.setStyleSheet(self.btn_style1)
        self.cancel_btn = QPushButton("取消")
        self.cancel_btn.setStyleSheet(self.btn_style1)

        self.refresh_btn.clicked.connect(self.refresh_data)
        self.cancel_btn.clicked.connect(self.reject)
        
        button_layout.addStretch()
        button_layout.addWidget(self.refresh_btn)

        button_layout.addWidget(self.cancel_btn)
        layout.addLayout(button_layout)
        
        self.setLayout(layout)

    def load_board_data(self):
        try:
            import os
            current_dir = os.path.dirname(os.path.abspath(__file__))
            data_path = os.path.join(current_dir, 'bk_content1.json')
            
            with open(data_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            # 处理新的数据结构（包含URL信息）
            if isinstance(data, dict) and "版面数据" in data:
                self.board_data = data["版面数据"]
                self.board_urls = data.get("版面URL", {})
            else:
                # 旧格式：只有版面数据
                self.board_data = data
                self.board_urls = {}
            
            print(f"成功加载 {len(self.board_data)} 个版块:")
            for board, contents in self.board_data.items():
                print(f"版块: {board} - {len(contents)} 个内容")
            
            self.create_board_widgets()
            
        except Exception as e:
            print(f"加载版块数据失败: {e}")
            QMessageBox.critical(self, "错误", f"无法加载版块数据: {str(e)}")

    def create_board_widgets(self):

        for board_title, contents in self.board_data.items():
            # 创建版块标题标签
            self.title_label1 = QLabel(board_title)
            self.title_label1.setStyleSheet(self.title_label1_style)
            self.title_label1.setAlignment(Qt.AlignCenter)
            self.board_layout.addWidget(self.title_label1)
            
            # 创建版块内容的滚动区域
            content_scroll = QScrollArea()
            content_scroll.setWidgetResizable(True)
            content_scroll.setFixedHeight(300)
            content_scroll.setStyleSheet(self.content_scroll_style)
            
            # 创建内容容器
            content_widget = QWidget()
            content_layout = QVBoxLayout()
            content_layout.setSpacing(5)
            content_layout.setContentsMargins(10, 10, 10, 10)
            
            # 添加复选框 - 横向排列，一行5个
            row_layout = None
            for i, content in enumerate(contents):
                # 每5个复选框创建一行
                if i % 5 == 0:
                    row_layout = QHBoxLayout()
                    row_layout.setSpacing(10)
                    content_layout.addLayout(row_layout)
                
                self.checkbox = QCheckBox(content)
                self.checkbox.setStyleSheet(self.checkbox_style)
                self.checkbox.stateChanged.connect(self.on_checkbox_changed)
                # 存储版面URL信息到复选框的属性中
                if hasattr(self, 'board_urls') and content in self.board_urls:
                    self.checkbox.setProperty("board_url", self.board_urls[content])
                row_layout.addWidget(self.checkbox)
            
            # 如果最后一行不满5个，添加弹性空间
            if row_layout and len(contents) % 5 != 0:
                row_layout.addStretch()
            
            content_widget.setLayout(content_layout)
            content_scroll.setWidget(content_widget)
            
            self.board_layout.addWidget(content_scroll)
            
            # 添加分隔线（除了最后一个版块）
            if board_title != list(self.board_data.keys())[-1]:
                separator = QFrame()
                separator.setFrameShape(QFrame.HLine)
                separator.setStyleSheet("background-color: #dee2e6; margin: 10px 0px; height: 1px;")
                self.board_layout.addWidget(separator)

    def on_checkbox_changed(self, state):
        # 直接更新收藏列表，不需要取消其他复选框的选中状态
        self.update_favorite_list()

    def update_favorite_list(self):
        # 清空现有收藏列表
        self.selected_items = []
        self.selected_items_with_urls = []  # 存储带URL的收藏项目
        for i in reversed(range(self.favorite_layout.count())):
            item = self.favorite_layout.itemAt(i)
            if item.widget():
                item.widget().setParent(None)

        
        # 遍历所有版块，按照它们在界面中的顺序
        current_board_title = None  # 初始化变量
        for i in range(self.board_layout.count()):
            widget = self.board_layout.itemAt(i).widget()
            
            # 检查是否是版块标题标签
            if isinstance(widget, QLabel) and widget.styleSheet().find("font-size: 22px") != -1:
                current_board_title = widget.text()
                continue
            
            # 检查是否是滚动区域（包含复选框）
            if isinstance(widget, QScrollArea):
                content_widget = widget.widget()
                content_layout = content_widget.layout()
                
                # 遍历每一行
                for j in range(content_layout.count()):
                    item = content_layout.itemAt(j)
                    if item.layout():  # 如果是行布局
                        row_layout = item.layout()
                        # 遍历行中的每个复选框
                        for k in range(row_layout.count()):
                            checkbox = row_layout.itemAt(k).widget()
                            if isinstance(checkbox, QCheckBox) and checkbox.isChecked():
                                if current_board_title:  # 确保有版块标题
                                    board_name = checkbox.text()
                                    full_name = f"{current_board_title} - {board_name}"
                                    self.selected_items.append(full_name)
                                    
                                    # 收集URL信息
                                    board_url = checkbox.property("board_url")
                                    if board_url:
                                        self.selected_items_with_urls.append({
                                            "name": full_name,
                                            "url": board_url
                                        })
                                    else:
                                        self.selected_items_with_urls.append({
                                            "name": full_name,
                                            "url": ""
                                        })
        
        self.shoucang = {
            "收藏的版块": self.selected_items,
            "收藏的版块详情": self.selected_items_with_urls
        }
        print(self.shoucang)
        # 创建固定的容器来保持布局稳定
        if self.selected_items:
            for item in self.selected_items:
                label = QLabel(f" {item}")
                label.setStyleSheet("""
                    font-size: 22px;
                    color: #28a745;
                    padding: 8px 12px;
                    background-color: #d4edda;
                    border-radius: 5px;
                    margin: 3px 0px;
                    border: 1px solid #c3e6cb;
                """)
                label.setFixedHeight(50)
                self.favorite_layout.addWidget(label)
        else:
            no_selection_label = QLabel("暂无选中的版面")
            no_selection_label.setStyleSheet("""
                font-size: 20px;
                color: #6c757d;
                padding: 20px;
                text-align: center;
            """)
            no_selection_label.setAlignment(Qt.AlignCenter)
            self.favorite_layout.addWidget(no_selection_label)

    def filter_boards(self):
        search_text = self.search_edit.text().lower()
        
        current_title_label = None
        current_content_scroll = None
        
        for i in range(self.board_layout.count()):
            widget = self.board_layout.itemAt(i).widget()
            
            # 检查是否是版块标题标签
            if isinstance(widget, QLabel) and widget.styleSheet().find("font-size: 22px") != -1:
                current_title_label = widget
                continue
            
            # 检查是否是滚动区域（包含复选框）
            if isinstance(widget, QScrollArea):
                current_content_scroll = widget
                content_widget = widget.widget()
                content_layout = content_widget.layout()
                
                # 检查版块标题是否匹配
                title_match = search_text in current_title_label.text().lower() if current_title_label else False
                
                # 检查内容是否匹配
                content_match = False
                for j in range(content_layout.count()):
                    item = content_layout.itemAt(j)
                    if item.layout():  # 如果是行布局
                        row_layout = item.layout()
                        for k in range(row_layout.count()):
                            checkbox = row_layout.itemAt(k).widget()
                            if isinstance(checkbox, QCheckBox):
                                if search_text in checkbox.text().lower():
                                    content_match = True
                                    checkbox.setVisible(True)
                                else:
                                    checkbox.setVisible(False)
                
                # 显示或隐藏整个版块组
                if current_title_label and current_content_scroll:
                    should_show = title_match or content_match
                    current_title_label.setVisible(should_show)
                    current_content_scroll.setVisible(should_show)
            
            # 检查是否是分隔线
            elif isinstance(widget, QFrame):
                # 分隔线的显示逻辑需要根据前后组件来决定
                pass

    def save_favorites_to_json(self, checked=False, filename="favorites.json"):
        self.update_favorite_list() # 确保是最新的
        if self.selected_items:
            try:
                reply = QMessageBox.question(self, "提示", "您确定收藏这些版面吗",QMessageBox.Yes | QMessageBox.No)
                if reply == QMessageBox.Yes:
                    # 读取现有的收藏数据
                    existing_data = {}
                    try:
                        with open(filename, 'r', encoding="utf-8") as f:
                            existing_data = json.load(f)
                    except FileNotFoundError:
                        # 如果文件不存在，创建新的数据结构
                        existing_data = {"收藏的版块": [], "收藏的版块详情": []}
                    except json.JSONDecodeError:
                        # 如果JSON格式错误，创建新的数据结构
                        existing_data = {"收藏的版块": [], "收藏的版块详情": []}
                    
                    # 获取现有的收藏版块和详情
                    existing_boards = existing_data.get("收藏的版块", [])
                    existing_details = existing_data.get("收藏的版块详情", [])
                    
                    # 合并新的收藏内容，避免重复
                    new_boards = []
                    new_details = []
                    
                    for board in self.selected_items:
                        if board not in existing_boards:
                            new_boards.append(board)
                    
                    for detail in self.selected_items_with_urls:
                        if detail not in existing_details:
                            new_details.append(detail)
                    
                    # 合并现有数据和新数据
                    combined_boards = existing_boards + new_boards
                    combined_details = existing_details + new_details
                    
                    # 创建最终的收藏数据
                    final_data = {
                        "收藏的版块": combined_boards,
                        "收藏的版块详情": combined_details
                    }
                    
                    # 保存合并后的数据
                    with open(filename, 'w', encoding="utf-8") as f:
                        json.dump(final_data, f, ensure_ascii=False, indent=4)
                    
                    QMessageBox.information(self, "成功", f"版面收藏成功！新增 {len(new_boards)} 个版面")
                    # 发送信号通知主界面刷新
                    self.favorites_updated.emit()
                    # 设置对话框结果为接受，并保存选择的版块
                    self.selected_boards = list(self.selected_items)
                    self.accept()
                    return True
            except Exception as e:
                print(f"收藏失败: {e}")
                return False
        else:
            reply1 = QMessageBox.information(self, "提示", "您并没有选择任何版面")
            return False

    def get_selected_boards(self):
        return getattr(self, 'selected_boards', [])

    def refresh_data(self):
        self.load_board_data()
        self.search_edit.clear()
        QMessageBox.information(self, "刷新完成", "版面数据已刷新")





if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = banmian()
    win.show()
    app.exec_()


