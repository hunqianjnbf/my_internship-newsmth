#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import json
import requests
from datetime import datetime
from typing import List, Dict, Optional
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QSplitter, QListWidget, QListWidgetItem, QTextEdit, QLabel,
    QMenuBar, QToolBar, QAction, QComboBox, QPushButton, QScrollArea,
    QFrame, QMessageBox, QInputDialog, QLineEdit, QDialog, QFormLayout,
    QDialogButtonBox, QTabWidget, QTableWidget, QTableWidgetItem,
    QHeaderView, QAbstractItemView, QSizePolicy
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QTimer, QSize
from PyQt5.QtGui import QFont, QIcon, QPixmap, QPalette, QColor

class SMTHThread(QThread):
    """水木清华API线程"""
    posts_loaded = pyqtSignal(list)
    thread_loaded = pyqtSignal(dict)
    error_occurred = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        self.base_url = "https://www.mysmth.net"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def get_boards(self) -> List[Dict]:
        """获取版块列表"""
        try:
            # 这里使用模拟数据，实际应用中需要调用真实API
            return [
                {"name": "JobExpress", "title": "求职招聘", "description": "求职招聘信息"},
                {"name": "RealEstate", "title": "房地产", "description": "房地产相关讨论"},
                {"name": "ITExpress", "title": "IT业界", "description": "IT行业新闻讨论"},
                {"name": "Stock", "title": "股票", "description": "股票投资讨论"},
                {"name": "AutoWorld", "title": "汽车世界", "description": "汽车相关讨论"},
                {"name": "Travel", "title": "旅游", "description": "旅游攻略分享"},
                {"name": "Food", "title": "美食", "description": "美食分享讨论"},
                {"name": "Movie", "title": "电影", "description": "电影评论讨论"},
            ]
        except Exception as e:
            self.error_occurred.emit(f"获取版块列表失败: {str(e)}")
            return []
    
    def get_posts(self, board: str, page: int = 1) -> List[Dict]:
        """获取版块帖子列表"""
        try:
            # 模拟数据
            posts = []
            for i in range(20):
                posts.append({
                    "id": f"{board}_{page}_{i}",
                    "title": f"这是{board}版块的第{page}页第{i+1}个帖子标题",
                    "author": f"作者{i+1}",
                    "create_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "last_reply_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "reply_count": i * 3 + 1,
                    "board": board
                })
            return posts
        except Exception as e:
            self.error_occurred.emit(f"获取帖子列表失败: {str(e)}")
            return []
    
    def get_thread(self, thread_id: str) -> Dict:
        """获取帖子详情"""
        try:
            # 模拟数据
            thread = {
                "id": thread_id,
                "title": f"帖子标题: {thread_id}",
                "author": "发帖人",
                "create_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "content": f"这是帖子{thread_id}的详细内容。\n\n这里可以包含很多内容，支持换行。\n\n这是一个模拟的帖子内容，实际应用中会从API获取真实数据。",
                "replies": []
            }
            
            # 添加回复
            for i in range(10):
                thread["replies"].append({
                    "id": f"{thread_id}_reply_{i}",
                    "author": f"回复者{i+1}",
                    "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "content": f"这是第{i+1}个回复的内容。\n\n回复内容可以很长，支持多行显示。"
                })
            
            return thread
        except Exception as e:
            self.error_occurred.emit(f"获取帖子详情失败: {str(e)}")
            return {}


class BoardItem(QListWidgetItem):
    """版块列表项"""
    def __init__(self, board_data: Dict):
        super().__init__()
        self.board_data = board_data
        self.setText(board_data["title"])
        # 安全地获取description，如果不存在则使用title
        description = board_data.get("description", board_data["title"])
        self.setToolTip(description)


class PostItem(QListWidgetItem):
    """帖子列表项"""
    def __init__(self, post_data: Dict):
        super().__init__()
        self.post_data = post_data
        self.setText(f"{post_data['title']}\n作者: {post_data['author']} | 回复: {post_data['reply_count']}")
        self.setToolTip(f"创建时间: {post_data['create_time']}\n最后回复: {post_data['last_reply_time']}")





class ThreadViewWidget(QWidget):
    """帖子详情视图"""
    def __init__(self):
        super().__init__()
        self.current_thread = None
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        
        # 帖子标题
        self.title_label = QLabel()
        self.title_label.setStyleSheet("""
            QLabel {
                font-size: 18px;
                font-weight: bold;
                color: #2c3e50;
                padding: 10px;
                background-color: #ecf0f1;
                border-radius: 5px;
            }
        """)
        
        # 帖子信息
        self.info_label = QLabel()
        self.info_label.setStyleSheet("""
            QLabel {
                color: #7f8c8d;
                font-size: 12px;
                padding: 5px 10px;
            }
        """)
        
        # 帖子内容滚动区域
        self.content_scroll = QScrollArea()
        self.content_widget = QWidget()
        self.content_layout = QVBoxLayout()
        self.content_widget.setLayout(self.content_layout)
        self.content_scroll.setWidget(self.content_widget)
        self.content_scroll.setWidgetResizable(True)
        self.content_scroll.setStyleSheet("""
            QScrollArea {
                border: 1px solid #bdc3c7;
                border-radius: 5px;
                background-color: white;
            }
        """)
        
        # 设置内容区域的背景为白色
        self.content_widget.setStyleSheet("""
            QWidget {
                background-color: white;
            }
        """)
        
        layout.addWidget(self.title_label)
        layout.addWidget(self.info_label)
        layout.addWidget(self.content_scroll)
        
        self.setLayout(layout)
    
    def load_thread(self, thread_data: Dict):
        """加载帖子详情"""
        self.current_thread = thread_data
        
        # 设置标题
        self.title_label.setText(thread_data.get('title', ''))
        
        # 设置信息
        info_text = f"作者: {thread_data.get('author', '')} | 发布时间: {thread_data.get('create_time', '')}"
        self.info_label.setText(info_text)
        
        # 清空内容区域
        for i in reversed(range(self.content_layout.count())):
            self.content_layout.itemAt(i).widget().setParent(None)
        
        # 添加主贴
        if thread_data.get('content'):
            main_post_widget = self.create_post_widget(
                thread_data.get('author', ''),
                thread_data.get('create_time', ''),
                thread_data.get('content', ''),
                is_main_post=True
            )
            self.content_layout.addWidget(main_post_widget)
        
        # 添加分隔线
        if thread_data.get('replies'):
            separator = QFrame()
            separator.setFrameShape(QFrame.HLine)
            separator.setStyleSheet("QFrame { background-color: #bdc3c7; margin: 10px 0px; }")
            self.content_layout.addWidget(separator)
        
        # 添加回复
        for i, reply in enumerate(thread_data.get('replies', [])):
            reply_widget = self.create_post_widget(
                reply.get('author', ''),
                reply.get('time', ''),
                reply.get('content', ''),
                is_main_post=False
            )
            self.content_layout.addWidget(reply_widget)
            
            # 在回复之间添加分隔线（除了最后一个）
            if i < len(thread_data.get('replies', [])) - 1:
                separator = QFrame()
                separator.setFrameShape(QFrame.HLine)
                separator.setStyleSheet("QFrame { background-color: #bdc3c7; margin: 10px 0px; }")
                self.content_layout.addWidget(separator)
        
        self.content_layout.addStretch()
    
    def create_post_widget(self, author: str, time: str, content: str, is_main_post: bool = False) -> QWidget:
        """创建帖子/回复组件"""
        widget = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(15, 10, 15, 10)
        
        # 头部信息
        header_layout = QHBoxLayout()
        author_label = QLabel(f"作者: {author}")
        author_label.setStyleSheet("font-weight: bold; color: #2c3e50;")
        
        time_label = QLabel(f"时间: {time}")
        time_label.setStyleSheet("color: #7f8c8d; font-size: 12px;")
        
        # 如果是主贴，添加标识
        if is_main_post:
            main_label = QLabel("[主贴]")
            main_label.setStyleSheet("color: #e74c3c; font-weight: bold; font-size: 12px;")
            header_layout.addWidget(main_label)
        
        header_layout.addWidget(author_label)
        header_layout.addStretch()
        header_layout.addWidget(time_label)
        
        # 内容
        content_text = QTextEdit()
        content_text.setPlainText(content)
        content_text.setReadOnly(True)
        # 根据内容自动调整高度
        content_text.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        content_text.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        content_text.setStyleSheet("""
            QTextEdit {
                border: 1px solid #ecf0f1;
                border-radius: 5px;
                background-color: white;
                padding: 10px;
                font-size: 14px;
                line-height: 1.5;
            }
        """)
        
        # 根据内容长度调整高度
        content_length = len(content)
        if content_length < 100:
            content_text.setMaximumHeight(80)
        elif content_length < 300:
            content_text.setMaximumHeight(120)
        elif content_length < 600:
            content_text.setMaximumHeight(180)
        else:
            content_text.setMaximumHeight(250)
        
        # 强制更新大小
        content_text.document().setTextWidth(content_text.viewport().width())
        content_text.setFixedHeight(content_text.document().size().height() + 20)
        
        layout.addLayout(header_layout)
        layout.addWidget(content_text)
        
        widget.setLayout(layout)
        return widget


class PostWidget(QWidget):
    """帖子小方块组件"""
    def __init__(self, post_data: Dict, parent=None):
        super().__init__(parent)
        self.post_data = post_data
        self.init_ui()
    
    def init_ui(self):
        self.setFixedHeight(80)  # 固定高度
        self.setMinimumWidth(200)  # 设置最小宽度
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.setStyleSheet("""
            QWidget {
                background-color: #f8f9fa;
                border: 1px solid #e9ecef;
                border-radius: 8px;
                margin: 5px;
            }
            QWidget:hover {
                background-color: #e9ecef;
                border-color: #3498db;
            }
        """)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 8, 10, 8)
        layout.setSpacing(5)
        
        # 标题
        title_label = QLabel(self.post_data["title"])
        title_label.setWordWrap(True)
        title_label.setStyleSheet("""
            QLabel {
                font-weight: bold;
                color: #2c3e50;
                font-size: 14px;
                line-height: 1.3;
            }
        """)
        
        # 作者和时间信息
        info_label = QLabel(f"作者: {self.post_data['author']} | 时间: {self.post_data['create_time']}")
        info_label.setStyleSheet("""
            QLabel {
                color: #7f8c8d;
                font-size: 12px;
            }
        """)
        
        layout.addWidget(title_label)
        layout.addWidget(info_label)
        
        self.setLayout(layout)
    
    def sizeHint(self):
        """返回建议的大小"""
        return QSize(300, 80)
    
    def mousePressEvent(self, event):
        """鼠标点击事件"""
        if event.button() == Qt.LeftButton:
            # 发送信号给主窗口
            main_window = self.window()
            if hasattr(main_window, 'on_post_selected'):
                main_window.on_post_selected(self.post_data)


class PostsListWidget(QWidget):
    """帖子列表组件"""
    def __init__(self):
        super().__init__()
        self.current_board = None
        self.sort_by = "create_time"  # create_time 或 last_reply_time
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        
        # 工具栏
        toolbar_layout = QHBoxLayout()
        
        self.board_label = QLabel("版块: 未选择")
        self.board_label.setStyleSheet("font-weight: bold; color: #2c3e50;")
        
        self.sort_combo = QComboBox()
        self.sort_combo.addItems(["按创建时间排序", "按最后回复时间排序"])
        self.sort_combo.currentTextChanged.connect(self.on_sort_changed)
        
        self.refresh_btn = QPushButton("刷新")
        self.refresh_btn.clicked.connect(self.refresh_posts)
        
        toolbar_layout.addWidget(self.board_label)
        toolbar_layout.addStretch()
        toolbar_layout.addWidget(QLabel("排序:"))
        toolbar_layout.addWidget(self.sort_combo)
        toolbar_layout.addWidget(self.refresh_btn)
        
        # 帖子列表滚动区域
        self.posts_scroll = QScrollArea()
        self.posts_widget = QWidget()
        self.posts_layout = QVBoxLayout()
        self.posts_layout.setContentsMargins(5, 5, 5, 5)
        self.posts_layout.setSpacing(5)
        self.posts_widget.setLayout(self.posts_layout)
        self.posts_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.posts_scroll.setWidget(self.posts_widget)
        self.posts_scroll.setWidgetResizable(True)
        self.posts_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.posts_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.posts_scroll.setStyleSheet("""
            QScrollArea {
                border: 1px solid #bdc3c7;
                border-radius: 5px;
                background-color: white;
            }
        """)
        
        # 设置帖子列表区域的背景为白色
        self.posts_widget.setStyleSheet("""
            QWidget {
                background-color: white;
            }
        """)
        
        layout.addLayout(toolbar_layout)
        layout.addWidget(self.posts_scroll)
        
        self.setLayout(layout)
    
    def set_board(self, board_name: str, board_title: str):
        """设置当前版块"""
        self.current_board = board_name
        self.board_label.setText(f"版块: {board_title}")
        self.refresh_posts()
    
    def on_sort_changed(self, text: str):
        """排序方式改变"""
        if "创建时间" in text:
            self.sort_by = "create_time"
        else:
            self.sort_by = "last_reply_time"
        self.refresh_posts()
    
    def refresh_posts(self):
        """刷新帖子列表"""
        if not self.current_board:
            return
        
        # 生成测试数据
        posts = []
        for i in range(20):
            posts.append({
                "id": f"{self.current_board}_{i}",
                "title": f"这是{self.current_board}版块的第{i+1}个帖子标题，这是一个很长的标题用来测试显示效果",
                "author": f"作者{i+1}",
                "create_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "last_reply_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "reply_count": i * 3 + 1,
                "board": self.current_board
            })
        
        # 排序
        if self.sort_by == "create_time":
            posts.sort(key=lambda x: x["create_time"], reverse=True)
        else:
            posts.sort(key=lambda x: x["last_reply_time"], reverse=True)
        
        # 清空并更新列表
        for i in reversed(range(self.posts_layout.count())):
            item = self.posts_layout.itemAt(i)
            if item and item.widget():
                item.widget().setParent(None)
        
        print(f"生成 {len(posts)} 个帖子")
        for i, post in enumerate(posts):
            post_widget = PostWidget(post, self.posts_widget)
            self.posts_layout.addWidget(post_widget)
            print(f"添加帖子 {i+1}: {post['title'][:30]}...")
        
        self.posts_layout.addStretch()
        print(f"帖子列表布局完成，共 {self.posts_layout.count()-1} 个帖子组件")


class NavigationWidget(QWidget):
    """左侧导航栏"""
    def __init__(self):
        super().__init__()
        self.favorite_boards = []
        self.init_ui()
        self.load_favorites()
    
    def init_ui(self):
        layout = QVBoxLayout()
        
        # 标题
        title_label = QLabel("收藏版块")
        title_label.setStyleSheet("""
            QLabel {
                font-size: 28px;
                font-weight: bold;
                color: #2c3e50;
                padding: 10px;
                background-color: #ecf0f1;
                border-radius: 5px;
            }
        """)
        
        # 版块列表
        self.boards_list = QListWidget()
        self.boards_list.itemClicked.connect(self.on_board_selected)
        self.boards_list.setStyleSheet("""
            QListWidget {
                border: 1px solid #bdc3c7;
                border-radius: 5px;
                background-color: white;
            }
            QListWidget::item {
                padding: 8px;
                border-bottom: 1px solid #ecf0f1;
            }
            QListWidget::item:selected {
                background-color: #3498db;
                color: white;
            }
            QListWidget::item:hover {
                background-color: #ecf0f1;
            }
        """)
        
        # 添加收藏按钮
        add_btn = QPushButton("添加收藏")
        add_btn.clicked.connect(self.add_favorite)
        add_btn.setStyleSheet("""
            QPushButton {
                background-color: #27ae60;
                color: white;
                border: none;
                padding: 8px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #229954;
            }
        """)
        
        layout.addWidget(title_label)
        layout.addWidget(self.boards_list)
        layout.addWidget(add_btn)
        
        self.setLayout(layout)
    
    def load_favorites(self):
        """加载收藏版块"""
        # 从配置文件加载收藏版块
        try:
            with open('favorite_boards.json', 'r', encoding='utf-8') as f:
                self.favorite_boards = json.load(f)
        except FileNotFoundError:
            # 默认收藏版块
            self.favorite_boards = [
                {"name": "JobExpress", "title": "求职招聘", "description": "求职招聘信息"},
                {"name": "RealEstate", "title": "房地产", "description": "房地产相关讨论"},
                {"name": "ITExpress", "title": "IT业界", "description": "IT行业新闻讨论"},
            ]
            self.save_favorites()
        
        self.update_boards_list()
    
    def save_favorites(self):
        """保存收藏版块"""
        with open('favorite_boards.json', 'w', encoding='utf-8') as f:
            json.dump(self.favorite_boards, f, ensure_ascii=False, indent=2)
    
    def update_boards_list(self):
        """更新版块列表"""
        self.boards_list.clear()
        for board in self.favorite_boards:
            item = BoardItem(board)
            self.boards_list.addItem(item)
        
        # 如果有版块，默认选择第一个
        if self.favorite_boards:
            self.boards_list.setCurrentRow(0)
            # 使用定时器延迟设置，确保主窗口完全初始化
            QTimer.singleShot(100, self.set_default_board)
    
    def set_default_board(self):
        """设置默认版块"""
        if self.favorite_boards:
            first_board = self.favorite_boards[0]
            main_window = self.window()
            if hasattr(main_window, 'posts_widget'):
                main_window.posts_widget.set_board(first_board["name"], first_board["title"])
    
    def add_favorite(self):
        """添加收藏版块"""
        dialog = AddBoardDialog()
        if dialog.exec_() == QDialog.Accepted:
            board_name = dialog.board_name_edit.text().strip()
            board_title = dialog.board_title_edit.text().strip()
            
            if board_name and board_title:
                new_board = {"name": board_name, "title": board_title}
                if new_board not in self.favorite_boards:
                    self.favorite_boards.append(new_board)
                    self.save_favorites()
                    self.update_boards_list()
    
    def on_board_selected(self, item: BoardItem):
        """版块被选中"""
        # 发送信号给主窗口
        board_data = item.board_data
        # 直接调用主窗口的方法
        main_window = self.window()
        if hasattr(main_window, 'on_board_selected'):
            main_window.on_board_selected(item)


class AddBoardDialog(QDialog):
    """添加版块对话框"""
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle("添加收藏版块")
        self.setModal(True)
        
        layout = QFormLayout()
        
        self.board_name_edit = QLineEdit()
        self.board_name_edit.setPlaceholderText("版块英文名，如: JobExpress")
        
        self.board_title_edit = QLineEdit()
        self.board_title_edit.setPlaceholderText("版块中文名，如: 求职招聘")
        
        layout.addRow("版块英文名:", self.board_name_edit)
        layout.addRow("版块中文名:", self.board_title_edit)
        
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        
        layout.addRow(buttons)
        
        self.setLayout(layout)


class SMTHMainWindow(QMainWindow):
    """水木清华主窗口"""
    def __init__(self):
        super().__init__()
        self.smth_thread = SMTHThread()
        self.init_ui()
        self.setup_connections()
    
    def init_ui(self):
        self.setWindowTitle("水木清华社区 - PC端")
        self.setGeometry(100, 100, 1200, 800)
        
        # 设置菜单栏
        self.setup_menu_bar()
        
        # 设置工具栏
        self.setup_tool_bar()
        
        # 创建中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 创建主布局
        main_layout = QHBoxLayout()
        
        # 创建分割器
        splitter = QSplitter(Qt.Horizontal)
        
        # 左侧导航栏
        self.nav_widget = NavigationWidget()
        self.nav_widget.boards_list.itemClicked.connect(self.on_board_selected)
        
        # 中部帖子详情
        self.thread_widget = ThreadViewWidget()
        
        # 右侧帖子列表
        self.posts_widget = PostsListWidget()
        
        # 添加到分割器
        splitter.addWidget(self.nav_widget)
        splitter.addWidget(self.thread_widget)
        splitter.addWidget(self.posts_widget)
        
        # 设置分割器比例
        splitter.setSizes([30, 400, 600])
        
        main_layout.addWidget(splitter)
        central_widget.setLayout(main_layout)
        
        # 设置样式
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f6fa;
            }
        """)
    
    def setup_menu_bar(self):
        """设置菜单栏"""
        menubar = self.menuBar()
        
        # 文件菜单
        file_menu = menubar.addMenu('文件')
        
        refresh_action = QAction('刷新', self)
        refresh_action.setShortcut('F5')
        refresh_action.triggered.connect(self.refresh_all)
        file_menu.addAction(refresh_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction('退出', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # 工具菜单
        tools_menu = menubar.addMenu('工具')
        
        settings_action = QAction('设置', self)
        settings_action.triggered.connect(self.show_settings)
        tools_menu.addAction(settings_action)
        
        # 帮助菜单
        help_menu = menubar.addMenu('帮助')
        
        about_action = QAction('关于', self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
    
    def setup_tool_bar(self):
        """设置工具栏"""
        toolbar = self.addToolBar('主工具栏')
        
        refresh_action = QAction('刷新', self)
        refresh_action.triggered.connect(self.refresh_all)
        toolbar.addAction(refresh_action)
        
        toolbar.addSeparator()
        
        home_action = QAction('首页', self)
        home_action.triggered.connect(self.go_home)
        toolbar.addAction(home_action)
    
    def setup_connections(self):
        """设置信号连接"""
        self.smth_thread.posts_loaded.connect(self.on_posts_loaded)
        self.smth_thread.thread_loaded.connect(self.on_thread_loaded)
        self.smth_thread.error_occurred.connect(self.on_error)
    
    def on_board_selected(self, item: BoardItem):
        """版块被选中"""
        board_data = item.board_data
        self.posts_widget.set_board(board_data["name"], board_data["title"])
    
    def on_post_selected(self, post_data: Dict):
        """帖子被选中"""
        # 生成测试帖子内容
        thread_data = {
            "id": post_data["id"],
            "title": post_data["title"],
            "author": post_data["author"],
            "create_time": post_data["create_time"],
            "content": f"""这是帖子{post_data['id']}的详细内容。

这是一个模拟的帖子内容，用来测试显示效果。这个帖子包含了丰富的内容，包括：

1. 多行文本内容
2. 各种格式的文本
3. 详细的描述信息

这个帖子来自{post_data['board']}版块，作者是{post_data['author']}，创建时间是{post_data['create_time']}。

这里可以包含很多内容，支持换行和格式化。在实际应用中，这些内容会从API获取真实数据。

希望这个测试内容能够很好地展示帖子的显示效果！""",
            "replies": []
        }
        
        # 生成测试回复
        for i in range(8):
            thread_data["replies"].append({
                "id": f"{post_data['id']}_reply_{i}",
                "author": f"回复者{i+1}",
                "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "content": f"""这是第{i+1}个回复的内容。

回复者{i+1}说：这个帖子很有意思，我也来回复一下。

这是一个测试回复，用来展示回复的显示效果。回复内容可以很长，支持多行显示和格式化。

回复时间：{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}"""
            })
        
        # 加载帖子详情
        self.on_thread_loaded(thread_data)
    
    def on_posts_loaded(self, posts: List[Dict]):
        """帖子列表加载完成"""
        pass
    
    def on_thread_loaded(self, thread_data: Dict):
        """帖子详情加载完成"""
        self.thread_widget.load_thread(thread_data)
    
    def on_error(self, error_msg: str):
        """错误处理"""
        QMessageBox.warning(self, "错误", error_msg)
    
    def refresh_all(self):
        """刷新所有数据"""
        self.posts_widget.refresh_posts()
    
    def go_home(self):
        """返回首页"""
        # 清空当前显示
        self.thread_widget.load_thread({})
        self.posts_widget.set_board("", "")
    
    def show_settings(self):
        """显示设置对话框"""
        QMessageBox.information(self, "设置", "设置功能开发中...")
    
    def show_about(self):
        """显示关于对话框"""
        QMessageBox.about(self, "关于", 
                         "水木清华社区PC端\n\n"
                         "版本: 1.0.0\n"
                         "基于PyQt5开发\n\n"
                         "功能特性:\n"
                         "- 浏览水木清华社区帖子\n"
                         "- 收藏常用版块\n"
                         "- 查看帖子详情和回复\n"
                         "- 支持按时间排序")


def main():
    """主函数"""
    app = QApplication(sys.argv)
    
    # 设置应用信息
    app.setApplicationName("水木清华社区")
    app.setApplicationVersion("1.0.0")
    app.setOrganizationName("SMTH")
    
    # 创建主窗口
    window = SMTHMainWindow()
    window.show()
    
    # 运行应用
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
