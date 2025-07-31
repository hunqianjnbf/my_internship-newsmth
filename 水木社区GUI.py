import sys
from datetime import datetime

from PyQt5.QtCore import QPoint, pyqtSignal, Qt
from PyQt5.QtGui import QMouseEvent, QCursor, QIcon, QImage, QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLineEdit, QTextBrowser, QMessageBox, \
    QHBoxLayout, QScrollArea, QLabel, QMainWindow, QAction, QMenu, qApp, QTextEdit, QToolBar, QDialog, QFrame, \
    QSpacerItem, QSizePolicy, QCheckBox, QComboBox, QRadioButton, QListWidget, QListWidgetItem
from 水木社区爬取 import shuimu_craw
from PyQt5 import Qt, QtCore
from PyQt5.Qt import QThread
from 登录界面 import LoginDialog
from smth import NavigationWidget, BoardItem, AddBoardDialog, PostWidget


class window(QMainWindow):
    def __init__(self):
        super().__init__()

        self.init_styles()

        self.create_radioButton()
        self.create_cont()
        self.init_ui()
        self.current_board = None

        self.create_file()
        self.create_edit()
        self.create_view()
        self.create_go()
        self.create_feed()
        self.create_article()
        self.create_setting()
        self.create_tools()
        self.dragging = False
        self.drag_start_pos = None
        self.sort_by = "create_time"  # 初始化排序方式

    def create_file(self):

        menubar = self.menuBar()
        menubar.setStyleSheet("QMenuBar { background-color: #f8f9fa; border-bottom: 1px solid #dee2e6; }")
        menubar.setFixedHeight(50)
        menubar.setContentsMargins(30, 15, 15, 0)

        file_menu = menubar.addMenu("&文件")

        # 子菜单
        newMenu = QMenu("&新建", self)
        smail_file = QAction("&新建文件", self)
        smail_file1 = QAction("新建项目", self)
        newMenu.addAction(smail_file)
        newMenu.addAction(smail_file1)
        newMenu1 = QMenu("&打开", self)
        newMenu2 = QMenu("&保存", self)
        newMenu3 = QMenu("&另存为", self)

        file_menu.addMenu(newMenu)
        file_menu.addMenu(newMenu1)
        file_menu.addMenu(newMenu2)
        file_menu.addMenu(newMenu3)

    def create_edit(self):
        menubar = self.menuBar()
        edit_menu = menubar.addMenu("&编辑")

        smail_file = QMenu("&剪切", self)
        smail_file1 = QMenu("&复制", self)
        smail_file2 = QMenu("&粘贴", self)
        smail_file3 = QMenu("&删除", self)

        edit_menu.addMenu(smail_file)
        edit_menu.addMenu(smail_file1)
        edit_menu.addMenu(smail_file2)
        edit_menu.addMenu(smail_file3)

    def create_view(self):
        menubar = self.menuBar()
        view_menu = menubar.addMenu("&视图")

        small_menu = QMenu("&工具框", self)
        small_menu1 = QMenu("&外观", self)

        view_menu.addMenu(small_menu)
        view_menu.addMenu(small_menu1)

    def create_go(self):
        menubar = self.menuBar()
        go_menu = menubar.addMenu("&前往")

    def create_feed(self):
        menubar = self.menuBar()

        feed_menu = menubar.addMenu("&信息")

    def create_article(self):
        menubar = self.menuBar()
        article_menu = menubar.addMenu("&文章")

    def create_setting(self):
        menubar = self.menuBar()
        setting_menu = menubar.addMenu("&设置")

    def init_styles(self):
        self.btn_style = (
            """
            QPushButton {
                background-color: white;
                color: black;
                border: none;
                border-radius: 5px;  
                padding: 8px 14px;
                font-size: 28px;
            }
            QPushButton:hover {
                background-color: #D3D3D3;
            }
            """
        )

        self.title_btn_style = (
            """
            QPushButton {
                background-color: #ffffff;
                color: #333333;
                border: 2px solid #e0e0e0;
                border-radius: 8px;
                padding: 15px 20px;
                font-size: 28px;
                font-weight: 600;
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
        )
        
        self.tools_btn_style = (
            """
                    QPushButton {
                            font-size:37px;
                            font-weight:bold;
                            border: none;
                    }
    
                    QPushButton:hover {
                            text-decoration: underline;
                        }
                    QPushButton:pressed {
                            background-color:  #D3D3D3;  /* 灰黑色按下效果 */
                            text-decoration: underline;  /* 按下时保持下划线 */
                        }
                    """
        )
        self.border_style = (
            """ 
            border: 2px solid #e0e0e0;  
            border-radius: 10px;        
            background-color: white;    
            """
        )
        self.Font_style = (
            """
            font-size: 25px;
            font-weight:bold;
            border : None;
            
            """
        )

    def init_ui(self):

        container = QVBoxLayout()
        container.setContentsMargins(10, 0, 20, 20)
        container.setSpacing(20)
        self.setWindowTitle("水木社区")
        self.setWindowIcon(QIcon("bitbug_favicon.ico"))
        container.addLayout(self.create_core())

        self.textEdit = QTextEdit(self)
        central_widget = QWidget()
        central_widget.setLayout(container)
        self.setGeometry(700, 325, 2300, 1500)
        self.setStyleSheet("background-color:#f5f5f5")

        self.setCentralWidget(central_widget)

    def create_core(self):
        h_layout = QHBoxLayout()
        h_layout.setContentsMargins(20, 20, 20, 20)
        h_layout.setSpacing(20)

        h_layout.addWidget(self.create_left())
        h_layout.addWidget(self.create_right())

        return h_layout

    def create_right(self):
        container = QWidget()

        v_layout2 = QVBoxLayout()
        v_layout2.setContentsMargins(0, 5, 20, 5)
        v_layout2.setSpacing(5)
        v_layout2.addLayout(self.h1)
        v_layout2.addLayout(self.h2)
        v_layout2.addLayout(self.h3)
        v_layout2.addLayout(self.h4)
        v_layout2.addLayout(self.h5)
        v_layout2.addLayout(self.c_layout)

        container.setFixedWidth(490)
        container.setLayout(v_layout2)

        return container

    def create_cont(self):

        self.c_layout = QVBoxLayout()

        # 工具栏
        toolbar_layout = QHBoxLayout()
        toolbar_layout.setSpacing(0)

        self.board_label = QLabel("版块: 旅游")
        self.board_label.setStyleSheet("""
            font-weight: bold; 
            color: #2c3e50; 
            font-size: 20px;
            padding: 4px 8px;
            border: None;
            background-color: none
        """)
        # 设置尺寸策略，只占用需要的空间
        self.board_label.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)

        self.board_label.setMinimumWidth(130)
        self.board_label.setMaximumWidth(200)  # 限制最大宽度
        # 允许文字换行
        self.board_label.setWordWrap(True)

        self.sort_combo = QComboBox()
        self.sort_combo.addItems(["按创建时间排序", "按最后回复时间排序"])
        self.sort_combo.currentTextChanged.connect(self.on_sort_changed)
        # 设置排序下拉框为适中尺寸
        self.sort_combo.setMaximumWidth(180)
        self.sort_combo.setMinimumWidth(150)
        self.sort_combo.setStyleSheet("""
            QComboBox {
                font-size: 20px;
                padding: 6px 10px;
                border: 1px solid #ddd;
                border-radius: 5px;
                background-color: white;
                color: #333;
            }
            QComboBox:hover {
                border-color: #007bff;
            }
            QComboBox::drop-down {
                border: none;
                width: 25px;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 6px solid transparent;
                border-right: 6px solid transparent;
                border-top: 6px solid #666;
                margin-right: 8px;
            }
        """)

        self.refresh_btn = QPushButton("刷新")
        self.refresh_btn.clicked.connect(self.refresh_posts)
        # 设置刷新按钮为适中尺寸
        self.refresh_btn.setMaximumWidth(80)
        self.refresh_btn.setMinimumWidth(60)
        self.refresh_btn.setFixedHeight(40)
        self.refresh_btn.setStyleSheet("""
            QPushButton {
                font-size: 20px;
                font-weight: 500;
                padding: 6px 15px;
                border: 1px solid #ddd;
                border-radius: 5px;
                background-color: #f8f9fa;
                color: #333;
            }
            QPushButton:hover {
                background-color: #e9ecef;
                border-color: #007bff;
                color: #007bff;
            }
            QPushButton:pressed {
                background-color: #dee2e6;
                border-color: #0056b3;
                color: #0056b3;
            }
        """)

        # 直接添加版块标签到工具栏，不使用容器
        toolbar_layout.addWidget(self.board_label)
        toolbar_layout.addSpacing(5)  # 减少间距
        
        # 创建排序标签并设置样式
        sort_label = QLabel("排序:")
        sort_label.setStyleSheet("""
            font-size: 20px; 
            color: #555; 
            font-weight: bold;
            padding: 4px 6px;
        """)
        sort_label.setMaximumWidth(60)
        sort_label.setMinimumWidth(50)
        
        toolbar_layout.addWidget(sort_label)
        toolbar_layout.addWidget(self.sort_combo)
        toolbar_layout.addWidget(self.refresh_btn)
        
        # 添加版面选择按钮
        self.board_select_btn = QPushButton("选择版面")
        self.board_select_btn.setStyleSheet("""
            QPushButton {
                font-size: 16px;
                padding: 6px 12px;
                border: 1px solid #ddd;
                border-radius: 5px;
                background-color: #28a745;
                color: white;
            }
            QPushButton:hover {
                background-color: #218838;
                border-color: #1e7e34;
            }
            QPushButton:pressed {
                background-color: #1e7e34;
            }
        """)
        self.board_select_btn.clicked.connect(self.show_board_dialog)
        toolbar_layout.addWidget(self.board_select_btn)

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
        self.posts_scroll.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.posts_scroll.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
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

        self.c_layout.addLayout(toolbar_layout)
        self.c_layout.addWidget(self.posts_scroll)

    def on_sort_changed(self, text: str):
        if "创建时间" in text:
            self.sort_by = "create_time"
        else:
            self.sort_by = "last_reply_time"
        self.refresh_posts()

    def refresh_posts(self):
        if not self.current_board:
            return

            # 生成测试数据
            posts = []
            for i in range(20):
                posts.append({
                    "id": f"{self.current_board}_{i}",
                    "title": f"这是{self.current_board}版块的第{i + 1}个帖子标题，这是一个很长的标题用来测试显示效果",
                    "author": f"作者{i + 1}",
                    "create_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "last_reply_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "reply_count": i * 3 + 1,
                    "board": self.current_board
                })

            # 排序
            if hasattr(self, 'sort_by') and self.sort_by == "create_time":
                posts.sort(key=lambda x: x["create_time"], reverse=True)
            else:
                posts.sort(key=lambda x: x["last_reply_time"], reverse=True)

            try:
                for i in reversed(range(self.posts_layout.count())):
                    item = self.posts_layout.itemAt(i)
                    if item and item.widget():
                        item.widget().setParent(None)
            except Exception as e:
                print(f"清空帖子列表时出错: {e}")

        print(f"生成 {len(posts)} 个帖子")
        for i, post in enumerate(posts):
            post_widget = PostWidget(post, self.posts_widget)
            self.posts_layout.addWidget(post_widget)
            print(f"添加帖子 {i + 1}: {post['title'][:30]}...")

        self.posts_layout.addStretch()
        print(f"帖子列表布局完成，共 {self.posts_layout.count() - 1} 个帖子组件")


    def on_radio_button_clicked(self, button):
        try:
            if not button or not button.isChecked():
                return
                
            board_name = button.text()
            print(f"选择了板块: {board_name}")
            
            # 更新当前选中的板块
            self.current_board = board_name
            
            # 更新板块标签
            if hasattr(self, 'board_label') and self.board_label:
                self.board_label.setText(f"版块: {board_name}")
                # 确保标签能够显示完整文字
                self.board_label.adjustSize()
            
            # 安全地刷新帖子列表
            try:
                self.refresh_posts()
            except Exception as e:
                print(f"刷新帖子列表时出错: {e}")
            
            # 加载板块特定内容
            self.load_board_content(board_name)
            
        except Exception as e:
            print(f"处理QRadioButton点击事件时出错: {e}")
            import traceback
            traceback.print_exc()
    
    def load_board_content(self, board_name):
        """根据板块名称加载相应内容"""
        try:
            # 这里可以根据不同的板块加载不同的内容
            content_map = {
                "美食": "这里是美食板块的内容，包含各种美食分享、菜谱推荐等。",
                "家庭": "这里是家庭板块的内容，包含家庭生活、育儿经验等。",
                "电视": "这里是电视板块的内容，包含电视剧讨论、综艺节目等。",
                "汽车": "这里是汽车板块的内容，包含汽车评测、购车经验等。",
                "旅游": "这里是旅游板块的内容，包含旅游攻略、景点推荐等。",
                "高考-大学": "这里是高考-大学板块的内容，包含学习经验、院校信息等。",
                "股市": "这里是股市板块的内容，包含股票分析、投资建议等。",
                "二手房": "这里是二手房板块的内容，包含房产信息、交易经验等。",
                "电影生活": "这里是电影生活板块的内容，包含电影评论、观影体验等。",
                "幽默": "这里是幽默板块的内容，包含搞笑内容、段子分享等。"
            }
            
            content = content_map.get(board_name, f"这里是{board_name}板块的内容")
            print(f"加载{board_name}板块内容: {content}")
            
            # 可以在这里更新界面显示内容
            # 例如更新文本区域、加载特定数据等
            
        except Exception as e:
            print(f"加载板块内容时出错: {e}")
            import traceback
            traceback.print_exc()

    def show_board_dialog(self):
        """显示版面选择对话框"""
        try:
            # 创建爬虫实例并获取版面列表
            crawler = shuimu_craw()
            board_list = crawler.banmian
            
            if not board_list:
                QMessageBox.warning(self, "警告", "无法获取版面列表，请检查网络连接")
                return
            
            # 创建并显示版面对话框
            dialog = BoardDialog(board_list, self)
            result = dialog.exec_()
            
            if result == QDialog.Accepted and dialog.selected_board:
                # 更新当前选中的版面
                self.current_board = dialog.selected_board
                self.board_label.setText(f"版块: {dialog.selected_board}")
                print(f"选择了版面: {dialog.selected_board}")
                
                # 刷新帖子列表
                self.refresh_posts()
                
                # 加载版面内容
                self.load_board_content(dialog.selected_board)
                
        except Exception as e:
            print(f"显示版面对话框时出错: {e}")
            import traceback
            traceback.print_exc()
            QMessageBox.critical(self, "错误", f"无法显示版面选择对话框: {str(e)}")

    def create_tools(self):
        # 主工具栏
        self.toolbar = self.addToolBar('主工具栏')

        # 刷新按钮
        refresh_action = QAction('刷新', self)
        refresh_action.triggered.connect(self.refresh_all)
        self.toolbar.addAction(refresh_action)

        self.toolbar.addSeparator()

        # 首页按钮
        home_action = QAction('首页', self)
        home_action.triggered.connect(self.go_home)
        self.toolbar.addAction(home_action)

        # 登录按钮（保留原样）
        self.toolbar.addSeparator()
        self.Login_btn = QPushButton("登录")
        self.Login_btn.setMinimumSize(50, 50)
        self.Login_btn.setStyleSheet(self.tools_btn_style)
        self.Login_btn.setIcon(QIcon("登录.png"))
        self.Login_btn.clicked.connect(self.login_dialog)
        self.toolbar.addWidget(self.Login_btn)

    def refresh_all(self):
        if hasattr(self, 'create_left'):
            left_widget = self.create_left()
        # 刷新中间内容（如有）
        if hasattr(self, 'create_mid'):
            mid_widget = self.create_right()

    def go_home(self):
        # 清空中间内容（如有）
        if hasattr(self, 'scroll_layout'):
            for i in reversed(range(self.scroll_layout.count())):
                widget = self.scroll_layout.itemAt(i).widget()
                if widget:
                    widget.setParent(None)
        QMessageBox.information(self, "首页", "已返回首页（请根据实际需求完善首页逻辑）")

    def login_dialog(self):
        try:
            # 创建对话框时指定父窗口
            login_dialog = LoginDialog()

            # 显示对话框并获取结果
            result = login_dialog.exec_()

            if result == QDialog.Accepted:
                print("登录成功")
            else:
                print("登录取消")

        except Exception as e:
            print(f"登录对话框错误: {str(e)}")
            QMessageBox.critical(self, "错误", f"无法打开登录对话框: {str(e)}")

    def create_left(self):
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)

        self.scroll_container = QWidget()
        self.scroll_container.setStyleSheet(self.border_style)
        self.scroll_layout = QVBoxLayout()
        self.scroll_layout.setAlignment(QtCore.Qt.AlignTop)
        self.scroll_layout.setContentsMargins(20, 20, 20, 0)

        self.scroll_container.setLayout(self.scroll_layout)
        self.scroll_area.setWidget(self.scroll_container)

        return self.scroll_area


class BoardDialog(QDialog):
    def __init__(self, board_list, parent=None):
        super().__init__(parent)
        self.board_list = board_list
        self.selected_board = None
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle("水木社区版面列表")
        self.setFixedSize(600, 500)
        self.setStyleSheet("""
            QDialog {
                background-color: #f8f9fa;
            }
        """)
        
        layout = QVBoxLayout()
        
        # 标题
        title_label = QLabel("可用的版面列表")
        title_label.setStyleSheet("""
            font-size: 18px;
            font-weight: bold;
            color: #2c3e50;
            padding: 10px;
        """)
        title_label.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(title_label)
        
        # 搜索框
        search_layout = QHBoxLayout()
        self.search_edit = QLineEdit()
        self.search_edit.setPlaceholderText("搜索版面...")
        self.search_edit.setStyleSheet("""
            QLineEdit {
                font-size: 14px;
                padding: 8px 12px;
                border: 1px solid #ddd;
                border-radius: 5px;
                background-color: white;
            }
            QLineEdit:focus {
                border-color: #007bff;
            }
        """)
        self.search_edit.textChanged.connect(self.filter_boards)
        search_layout.addWidget(self.search_edit)
        layout.addLayout(search_layout)
        
        # 版面列表
        self.board_list_widget = QListWidget()
        self.board_list_widget.setStyleSheet("""
            QListWidget {
                font-size: 14px;
                border: 1px solid #ddd;
                border-radius: 5px;
                background-color: white;
                padding: 5px;
            }
            QListWidget::item {
                padding: 8px 12px;
                border-bottom: 1px solid #f0f0f0;
            }
            QListWidget::item:hover {
                background-color: #e9ecef;
            }
            QListWidget::item:selected {
                background-color: #007bff;
                color: white;
            }
        """)
        self.board_list_widget.itemDoubleClicked.connect(self.on_board_selected)
        layout.addWidget(self.board_list_widget)
        
        # 按钮
        button_layout = QHBoxLayout()
        self.select_btn = QPushButton("选择")
        self.cancel_btn = QPushButton("取消")
        
        for btn in [self.select_btn, self.cancel_btn]:
            btn.setStyleSheet("""
                QPushButton {
                    font-size: 14px;
                    padding: 8px 20px;
                    border: 1px solid #ddd;
                    border-radius: 5px;
                    background-color: #f8f9fa;
                    color: #333;
                }
                QPushButton:hover {
                    background-color: #e9ecef;
                    border-color: #007bff;
                }
                QPushButton:pressed {
                    background-color: #dee2e6;
                }
            """)
        
        self.select_btn.clicked.connect(self.on_select_clicked)
        self.cancel_btn.clicked.connect(self.reject)
        
        button_layout.addStretch()
        button_layout.addWidget(self.select_btn)
        button_layout.addWidget(self.cancel_btn)
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
        
        # 加载版面列表
        self.load_boards()
    
    def load_boards(self):
        """加载版面列表"""
        self.board_list_widget.clear()
        for board in self.board_list:
            item = QListWidgetItem(board)
            self.board_list_widget.addItem(item)
    
    def filter_boards(self):
        """根据搜索文本过滤版面"""
        search_text = self.search_edit.text().lower()
        for i in range(self.board_list_widget.count()):
            item = self.board_list_widget.item(i)
            item.setHidden(search_text not in item.text().lower())
    
    def on_board_selected(self, item):
        """双击选择版面"""
        self.selected_board = item.text()
        self.accept()
    
    def on_select_clicked(self):
        """点击选择按钮"""
        current_item = self.board_list_widget.currentItem()
        if current_item:
            self.selected_board = current_item.text()
            self.accept()
        else:
            QMessageBox.warning(self, "警告", "请先选择一个版面")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = window()
    w.show()
    app.exec()

