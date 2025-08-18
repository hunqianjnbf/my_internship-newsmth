import sys
import json
from datetime import datetime
import requests
from bs4 import BeautifulSoup
from PyQt5.QtCore import QPoint, pyqtSignal, Qt, QSize
from PyQt5.QtGui import QMouseEvent, QCursor, QIcon, QImage, QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLineEdit, QTextBrowser, QMessageBox, \
    QHBoxLayout, QScrollArea, QLabel, QMainWindow, QAction, QMenu, qApp, QTextEdit, QToolBar, QDialog, QFrame, \
    QSpacerItem, QSizePolicy, QCheckBox, QComboBox, QRadioButton
from PyQt5 import Qt, QtCore
from PyQt5.Qt import QThread
from Login_interface import LoginDialog
from smth import NavigationWidget, BoardItem, AddBoardDialog, PostWidget
from choose_boardGUI import banmian


class window(QMainWindow):
    def __init__(self):
        super().__init__()

        self.init_styles()

        self.create_favorite_board()
        self.create_cont()
        self.init_ui()
        self.current_board = None

        # 初始化爬虫实例，用于获取帖子内容
        self.crawler = shuimu_craw()
        self.posts_data = []  # 存储当前版块的帖子数据

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
        self.sort_by = "last_reply_time"  # 初始化排序方式，默认按最近时间排序
        self.delete_mode = False  # 初始化删除模式

    def process_time_for_sorting(self, time_str):
        if not time_str:
            return time_str
        
        try:
            # 去除可能的空格和开头的|符号
            time_str = time_str.strip()
            if time_str.startswith('|'):
                time_str = time_str[1:]  # 去掉开头的|符号
            
            print(f"处理时间字符串: '{time_str}'")

            # 如果时间格式是 HH:MM:SS 格式（只有时分秒）
            if ':' in time_str and len(time_str.split(':')) == 3:
                parts = time_str.split(':')
                if (len(parts[0]) == 2 and len(parts[1]) == 2 and len(parts[2]) == 2 and
                    parts[0].isdigit() and parts[1].isdigit() and parts[2].isdigit()):

                    current_year = datetime.now().year
                    today = datetime.now().strftime("%m-%d")
                    processed_time = f"{current_year}-{today} {time_str}"
                    print(f"时间只有时分秒，添加当前年份: '{time_str}' -> '{processed_time}'")
                    return processed_time

            elif '-' in time_str and ':' in time_str:
                parts = time_str.split(' ')
                if len(parts) == 2:
                    date_part = parts[0]  # MM-DD
                    time_part = parts[1]  # HH:MM:SS

                    if '-' in date_part and len(date_part.split('-')) == 2:
                        month_day = date_part.split('-')
                        if (len(month_day[0]) <= 2 and len(month_day[1]) <= 2 and
                            month_day[0].isdigit() and month_day[1].isdigit() and
                            int(month_day[0]) <= 12 and int(month_day[1]) <= 31):

                            current_year = datetime.now().year
                            processed_time = f"{current_year}-{date_part} {time_part}"
                            print(f"时间有月日时分秒，添加当前年份: '{time_str}' -> '{processed_time}'")
                            return processed_time
            
            # 如果已经是完整的时间格式，直接返回
            print(f"时间格式完整，无需处理: '{time_str}'")
            return time_str
            
        except Exception as e:
            print(f"处理时间字符串时出错: {e}")
            return time_str

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
        self.label2_style = ("""
                        color: black;
                        font-size: 24px;
                        padding: 20px;
                        text-align: center;
                    """)
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
        self.label1_style = (
            """
            font-size: 25px;
            font-weight:bold;
            """
        )
        self.container_scroll_style = (
            """
                        QScrollArea {
                            border: 1px solid #e0e0e0;
                            border-radius: 8px;
                            background-color: white;
                        }
                        QScrollBar:vertical {
                            background: #f0f0f0;
                            width: 12px;
                            border-radius: 6px;
                        }
                        QScrollBar::handle:vertical {
                            background: #c0c0c0;
                            border-radius: 6px;
                            min-height: 20px;
                        }
                        QScrollBar::handle:vertical:hover {
                            background: #a0a0a0;
                        }
                    """
        )
        self.board_button_style = ("""
                    QPushButton {
                        background-color: #ffffff;
                        color: #333333;
                        border: 2px solid #e0e0e0;
                        border-radius: 10px;
                        padding: 15px 20px;
                        font-size: 16px;
                        font-weight: 500;
                        text-align: left;
                        margin: 5px 0px;
                        min-height: 50px;
                        min-width: 400px;
                        max-width: 450px;
                    }
                    QPushButton:hover {
                        background-color: #f8f9fa;
                        border-color: #007bff;
                        color: #007bff;
                    }
                    QPushButton:checked {
                        background-color: #e3f2fd;
                        border-color: #2196f3;
                        color: #1976d2;
                        font-weight: 600;
                    }
                    QPushButton:pressed {
                        background-color: #e9ecef;
                        border-color: #0056b3;
                        color: #0056b3;
                    }
                """)

        self.board_button_style_delete_mode = ("""
                    QPushButton {
                        background-color: #ffffff;
                        color: #333333;
                        border: 2px solid #e0e0e0;
                        border-radius: 10px;
                        padding: 15px 20px;
                        font-size: 16px;
                        font-weight: 500;
                        text-align: left;
                        margin: 5px 0px;
                        min-height: 50px;
                        min-width: 350px;
                        max-width: 400px;
                    }
                    QPushButton:hover {
                        background-color: #f8f9fa;
                        border-color: #007bff;
                        color: #007bff;
                    }
                    QPushButton:checked {
                        background-color: #e3f2fd;
                        border-color: #2196f3;
                        color: #1976d2;
                        font-weight: 600;
                    }
                    QPushButton:pressed {
                        background-color: #e9ecef;
                        border-color: #0056b3;
                        color: #0056b3;
                    }
                """)

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
        self.setGeometry(300, 125, 2300, 1500)
        self.setStyleSheet("background-color:#f5f5f5")

        self.setCentralWidget(central_widget)

    def create_core(self):
        h_layout = QHBoxLayout()
        h_layout.setContentsMargins(20, 20, 20, 20)
        h_layout.setSpacing(20)

        h_layout.addWidget(self.create_left(), 3)  # 左边占3/5
        h_layout.addWidget(self.create_right(), 2)  # 右边占2/5

        return h_layout

    def create_right(self):
        container = QWidget()

        v_layout2 = QVBoxLayout()

        v_layout2.setContentsMargins(0, 5, 20, 5)
        v_layout2.setSpacing(5)
        h_lay = QHBoxLayout()
        self.label1 = QLabel("已收藏的版块")
        self.label1.setStyleSheet(self.label1_style)
        self.butn = QPushButton("添加收藏")
        self.butn.clicked.connect(self.butn_clicked)
        self.butn.setStyleSheet(self.btn_style)
        self.butn1 = QPushButton("删除收藏")
        self.butn1.clicked.connect(self.butn1_clicked)
        self.butn1.setStyleSheet(self.btn_style)
        h_lay.addWidget(self.label1)
        h_lay.addWidget(self.butn)
        h_lay.addWidget(self.butn1)

        v_layout2.addLayout(h_lay)
        v_layout2.addWidget(self.container_scroll,1)
        v_layout2.addLayout(self.c_layout,2)

        container.setFixedWidth(490)
        container.setLayout(v_layout2)

        return container

    def create_favorite_board(self):
        self.radioButton_container = QWidget()
        self.container_scroll = QScrollArea()
        self.container_layout = QVBoxLayout()
        self.container_scroll.setStyleSheet(self.container_scroll_style)

        self.favorite_board = self.load_favorites()
        for board_name in self.favorite_board:
            board_name1 = self.create_board_button(board_name)
            self.container_layout.addWidget(board_name1)
        if not self.favorite_board:
            self.label2 = QLabel("暂无收藏的版块")
            self.label2.setStyleSheet(self.label2_style)
            self.label2.setAlignment(QtCore.Qt.AlignCenter)
            self.container_layout.addWidget(self.label2)

        self.container_layout.addStretch(1)
        self.radioButton_container.setLayout(self.container_layout)
        self.container_scroll.setWidgetResizable(True)  #滚动区域自适应
        self.container_scroll.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded) #用于设置控件垂直滚动条显示策略的方法
        self.container_scroll.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)#用于设置控件水平滚动条显示策略的方法
        self.container_scroll.setWidget(self.radioButton_container)

    def load_favorites(self):
        try:
            with open("favorites.json","r",encoding="utf-8") as f:
                self.favorites = json.load(f)
                return self.favorites.get("收藏的版块",[])
        except FileNotFoundError:
            print("没有找到文件")
            return []
        except json.JSONDecodeError:
            print("Json文件格式错误")
            return []
        except Exception as e:
            print(f"读取Json文件时发生错误{str(e)}")
            return []

    def create_board_button(self,board_name):
        # 创建容器来放置按钮和删除按钮
        container = QWidget()
        container_layout = QHBoxLayout()
        container_layout.setContentsMargins(0, 0, 0, 0)
        container_layout.setSpacing(5)
        container_layout.setAlignment(QtCore.Qt.AlignCenter)  # 居中对齐

        # 创建版块按钮
        button = QPushButton(board_name)
        button.setCheckable(True)  # 设置为可选中状态

        # 根据删除模式设置不同的样式
        if hasattr(self, 'delete_mode') and self.delete_mode:
            button.setStyleSheet(self.board_button_style_delete_mode)
        else:
            button.setStyleSheet(self.board_button_style)

        button.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)  # 根据内容调整，垂直固定

        button.clicked.connect(lambda checked, btn=button: self.board_btn_clicked(btn))

        delete_btn = QPushButton("×")
        delete_btn.setFixedSize(35, 35)
        delete_btn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)  # 固定大小
        delete_btn.setStyleSheet("""
            QPushButton {
                background-color: #dc3545;
                color: white;
                border: 2px solid #dc3545;
                border-radius: 17px;
                font-size: 20px;
                font-weight: bold;
                min-width: 35px;
                min-height: 35px;
                margin: 0px 5px;
            }
            QPushButton:hover {
                background-color: #c82333;
                border-color: #c82333;
            }
        """)
        delete_btn.clicked.connect(lambda: self.delete_board(board_name))
        delete_btn.hide()

        container_layout.addWidget(button)
        container_layout.addWidget(delete_btn)

        container.setLayout(container_layout)

        container.delete_btn = delete_btn

        return container

    def board_btn_clicked(self, button):
        try:
            # 取消其他按钮的选中状态
            for i in range(self.container_layout.count()):
                item = self.container_layout.itemAt(i)
                if item and item.widget():
                    # 获取容器中的按钮
                    container = item.widget()
                    if hasattr(container, 'layout'):
                        container_layout = container.layout()
                        for j in range(container_layout.count()):
                            container_item = container_layout.itemAt(j)
                            if container_item and container_item.widget() and isinstance(container_item.widget(), QPushButton):
                                other_button = container_item.widget()
                                # 跳过删除按钮
                                if other_button.text() != "×" and other_button != button:
                                    other_button.setChecked(False)

            # 确保当前按钮被选中
            button.setChecked(True)

            # 调用原有的on_radio_button_clicked方法
            self.on_radio_button_clicked(button)

        except Exception as e:
            print(f"处理版块按钮点击事件时出错: {e}")
            import traceback
            traceback.print_exc()

    def butn_clicked(self):
        bm = banmian()
        result = bm.exec_()

        # 如果对话框被接受，替换所有收藏
        if result == QDialog.Accepted:
            self.replace_all_favorites()
            # 立即刷新显示
            self.refresh_favorite_boards()

    def replace_all_favorites(self):
        try:
            # 获取新选择的版块
            bm = banmian()
            result = bm.exec_()

            if result == QDialog.Accepted:
                # 从版面选择对话框获取选择的版块
                new_boards = bm.get_selected_boards()

                if new_boards:
                    # 更新JSON文件
                    self.save_favorites(new_boards)

                    print(f"已替换所有收藏的版块: {new_boards}")
                else:
                    print("没有选择任何版块")
            else:
                print("用户取消了版块选择")

        except Exception as e:
            print(f"替换收藏版块时出错: {e}")
            import traceback
            traceback.print_exc()

    def save_favorites(self, boards):
        try:
            # 读取
            existing_data = {}
            try:
                with open("favorites.json", "r", encoding="utf-8") as f:
                    existing_data = json.load(f)
            except FileNotFoundError:
                pass

            # 更新收藏的版块
            data = {"收藏的版块": boards}

            # 如果有现有的收藏的版块详情，需要同步更新
            if "收藏的版块详情" in existing_data:
                # 过滤掉已删除的版块详情
                updated_details = []
                for detail in existing_data["收藏的版块详情"]:
                    if detail["name"] in boards:
                        updated_details.append(detail)
                data["收藏的版块详情"] = updated_details

            with open("favorites.json", "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存收藏版块时出错: {e}")

    def delete_board(self, board_name):
        try:
            # 从收藏列表中移除
            if board_name in self.favorite_board:
                self.favorite_board.remove(board_name)

                # 保存到JSON
                self.save_favorites(self.favorite_board)

                # 刷新
                self.refresh_favorite_boards()

                print(f"已删除版块: {board_name}")

        except Exception as e:
            print(f"删除版块时出错: {e}")
            import traceback
            traceback.print_exc()

    def butn1_clicked(self):
        if hasattr(self, 'delete_mode') and self.delete_mode: #判断当前对象是否具有deletemode的属性且为真执行
            # 退出删除
            self.delete_mode = False
            self.butn1.setText("删除收藏")
            self.butn1.setStyleSheet(self.btn_style)
            self.refresh_favorite_boards()
        else:
            # 进入删除
            self.delete_mode = True
            self.butn1.setText("退出删除")
            self.butn1.setStyleSheet("""
                QPushButton {
                    background-color: #dc3545;
                    color: white;
                    border: none;
                    border-radius: 5px;  
                    padding: 8px 14px;
                    font-size: 28px;
                }
                QPushButton:hover {
                    background-color: #c82333;
                }
            """)
            self.refresh_favorite_boards()

    def refresh_favorite_boards(self):
        try:
            # 保存
            current_selected_board = None
            for i in range(self.container_layout.count()):
                item = self.container_layout.itemAt(i)
                if item and item.widget():
                    container = item.widget()
                    if hasattr(container, 'layout'):
                        container_layout = container.layout()
                        for j in range(container_layout.count()):
                            container_item = container_layout.itemAt(j)
                            if container_item and container_item.widget() and isinstance(container_item.widget(), QPushButton):
                                button = container_item.widget()
                                if button.text() != "×" and button.isChecked():
                                    current_selected_board = button.text()
                                    break

            # 清空按钮
            for i in reversed(range(self.container_layout.count())):
                item = self.container_layout.itemAt(i)
                if item and item.widget():
                    item.widget().setParent(None)

            # 重新加载收藏的版块
            self.favorite_board = self.load_favorites()

            # 重新创建按钮
            for board_name in self.favorite_board:
                board_container = self.create_board_button(board_name)
                self.container_layout.addWidget(board_container)

                if hasattr(self, 'delete_mode') and self.delete_mode:
                    if hasattr(board_container, 'delete_btn'):
                        board_container.delete_btn.show()
                        board_container.delete_btn.setVisible(True)
                        board_container.delete_btn.raise_()  # 确保按钮在最前面
                    else:
                        print(f"容器没有delete_btn属性: {board_name}")

                    for i in range(board_container.layout().count()):
                        item = board_container.layout().itemAt(i)
                        if item and item.widget() and isinstance(item.widget(), QPushButton) and item.widget() != board_container.delete_btn:
                            item.widget().setStyleSheet(self.board_button_style_delete_mode)
                else:
                    if hasattr(board_container, 'delete_btn'):
                        board_container.delete_btn.hide()
                        board_container.delete_btn.setVisible(False)
                    else:
                        print(f"容器没有delete_btn属性: {board_name}")

                    # 恢复版块按钮样式为正常模式
                    for i in range(board_container.layout().count()):
                        item = board_container.layout().itemAt(i)
                        if item and item.widget() and isinstance(item.widget(), QPushButton) and item.widget() != board_container.delete_btn:
                            item.widget().setStyleSheet(self.board_button_style)

            # 恢复选中状态
            if current_selected_board:
                for i in range(self.container_layout.count()):
                    item = self.container_layout.itemAt(i)
                    if item and item.widget():
                        container = item.widget()
                        if hasattr(container, 'layout'):
                            container_layout = container.layout()
                            for j in range(container_layout.count()):
                                container_item = container_layout.itemAt(j)
                                if container_item and container_item.widget() and isinstance(container_item.widget(), QPushButton):
                                    button = container_item.widget()
                                    if button.text() == current_selected_board:
                                        button.setChecked(True)
                                        break

            # 如果没有收藏的版块，显示提示信息
            if not self.favorite_board:
                self.label2 = QLabel("暂无收藏的版块")
                self.label2.setStyleSheet(self.label2_style)
                self.label2.setAlignment(QtCore.Qt.AlignCenter)
                self.container_layout.addWidget(self.label2)

            self.container_layout.addStretch()  # 添加弹性空间

        except Exception as e:
            print(f"刷新收藏版块列表时出错: {e}")
            import traceback
            traceback.print_exc()

    def create_cont(self):

        self.c_layout = QVBoxLayout()

        # 工具栏
        toolbar_layout = QHBoxLayout()
        toolbar_layout.setSpacing(0)


        self.sort_combo = QComboBox()
        self.sort_combo.addItems(["按创建时间排序", "按最近回复时间排序"])
        self.sort_combo.setCurrentText("按最近回复时间排序")  # 默认选择按最近时间排序
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
        """排序方式改变时的处理"""
        if "创建时间" in text:
            self.sort_by = "create_time"
            print(f"排序方式已更改为: 按创建时间排序")
        elif "最近回复时间" in text:
            self.sort_by = "last_reply_time"
            print(f"排序方式已更改为: 按最近回复时间排序")
        else:
            # 默认按最近回复时间排序
            self.sort_by = "last_reply_time"
            print(f"排序方式设置为默认: 按最近回复时间排序")
        self.refresh_posts()

    def refresh_posts(self):
        if not self.current_board:
            print("没有选择版块，无法刷新帖子")
            return

        print(f"开始刷新帖子列表，当前版块: {self.current_board}")

        # 直接复制标题作者和时间.py中的爬取逻辑
        posts_data = []

        # 从favorites.json获取当前版块的URL
        with open("favorites.json", "r", encoding="utf-8") as f:
            data = json.load(f)

        board_detail = data.get("收藏的版块详情", [])
        target_board = None

        for item in board_detail:
            if item.get("name") == self.current_board:
                target_board = item
                break

        if target_board:
            url = target_board.get("url")
            if url:


                r = requests.get(url)
                if r:
                    soup = BeautifulSoup(r.text, "html.parser")
                    ul_elements = soup.find_all("ul", class_="list sec")
                    for ul in ul_elements:
                        li_elements = ul.find_all("li")
                        if li_elements:
                            for li in li_elements:
                                div_elements = li.find_all("div")
                                if div_elements:
                                    title_div = div_elements[0]
                                    text0 = title_div.find("a")
                                    title = text0.get_text(strip=True) if text0 else ""
                                    if title == "版面积分变更记录":
                                        continue
                                    info_div = div_elements[1]
                                    self.authors = []
                                    self.times = []
                                    for child in info_div.children:
                                        if child.name == "a":
                                            text1 = child.get_text(strip=True)
                                            self.authors.append(text1)
                                        elif child.name:  # 其他标签节点
                                            text = child.get_text(strip=True).replace("&nbsp;"," ")
                                            if text.strip():
                                                self.times.append(text.strip())
                                        else:  # 文本节点
                                            text = child.get_text(strip=True).replace("&nbsp;"," ")
                                            if text.strip():
                                                self.times.append(text.strip())


                                    post_time = self.times[0] if len(self.times) >= 1 else ""
                                    author = self.authors[0] if len(self.authors) >= 1 else ""
                                    last_reply_time = self.times[1] if len(self.times) >= 2 else (self.times[0] if self.times else "")
                                    reply_count = self.authors[1] if len(self.authors) >= 2 else ""
                                    # 获取帖子的具体URL
                                    post_url = ""
                                    if text0 and text0.has_attr('href'):
                                        post_url = text0['href']
                                        post_url = "https://m.newsmth.net/" + post_url

                                    posts_data.append({
                                        "版面": self.current_board,
                                        "标题": title,
                                        "作者": author,
                                        "时间": post_time,
                                        "最近回复的时间": last_reply_time,
                                        "reply_count": reply_count,
                                        "url": post_url
                                    })
                                    

            posts = []
            for post_data in posts_data:
                posts.append({
                    "id": f"{post_data['版面']}_{len(posts)}",
                    "title": post_data['标题'],
                    "author": post_data['作者'],
                    "create_time": post_data['时间'],
                    "last_reply_time": post_data['最近回复的时间'],
                    "reply_count": post_data['reply_count'],
                    "url": post_data.get('url', '')
                })

            # 按时间排序（默认按最近时间排序）
            if hasattr(self, 'sort_by') and self.sort_by == "create_time":
                print(f"按创建时间排序，共 {len(posts)} 个帖子")
                # 处理时间字符串，确保排序正确
                for i, post in enumerate(posts):
                    print(f"帖子 {i+1} 原始创建时间: {post['create_time']}")
                    post["create_time"] = self.process_time_for_sorting(post["create_time"])
                    print(f"帖子 {i+1} 处理后创建时间: {post['create_time']}")
                posts.sort(key=lambda x: x["create_time"], reverse=True)
            else:
                print(f"按最近回复时间排序，共 {len(posts)} 个帖子")
                # 处理时间字符串，确保排序正确
                for i, post in enumerate(posts):
                    print(f"帖子 {i+1} 原始回复时间: {post['last_reply_time']}")
                    post["last_reply_time"] = self.process_time_for_sorting(post["last_reply_time"])
                    print(f"帖子 {i+1} 处理后回复时间: {post['last_reply_time']}")
                posts.sort(key=lambda x: x["last_reply_time"], reverse=True)

            try:
                for i in reversed(range(self.posts_layout.count())):
                    item = self.posts_layout.itemAt(i)
                    if item and item.widget():
                        item.widget().setParent(None)
            except Exception as e:
                print(f"清空帖子列表时出错: {e}")

            for i, post in enumerate(posts):
                post_widget = PostManager.PostWidget(post, self.posts_widget)
                self.posts_layout.addWidget(post_widget)

            self.posts_layout.addStretch()

    def on_radio_button_clicked(self, button):
        try:
            if not button or not button.isChecked():
                return

            board_name = button.text()

            self.current_board = board_name

            # 安全地刷新帖子列表
            try:
                self.refresh_posts()
            except Exception as e:
                print(f"刷新帖子列表时出错: {e}")
                return False

        except Exception as e:
            print(f"处理QRadioButton点击事件时出错: {e}")
            return False

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
        # 创建左侧区域
        left_widget = QWidget()
        left_layout = QHBoxLayout()
        
        # 创建滚动区域来容纳所有内容
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        
        # 设置滚动条样式
        scroll_area.setStyleSheet("""
            QScrollBar:vertical {
                background-color: #f0f0f0;
                width: 12px;
                border-radius: 6px;
            }
            QScrollBar::handle:vertical {
                background-color: #c0c0c0;
                border-radius: 6px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: #a0a0a0;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
        """)
        
        # 创建内容容器
        content_container = QWidget()
        content_layout = QVBoxLayout()
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)
        
        # 楼主内容区域
        self.louzhu_container = QWidget()
        self.louzhu_layout = QVBoxLayout()
        self.louzhu_layout.setContentsMargins(20, 20, 20, 20)
        self.louzhu_layout.setSpacing(15)
        self.louzhu_container.setLayout(self.louzhu_layout)
        
        # 跟帖滚动区域
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.scroll_area.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        
        # 设置跟帖滚动区域样式
        self.scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: transparent;
            }
            QScrollBar:vertical {
                background-color: #f0f0f0;
                width: 10px;
                border-radius: 5px;
            }
            QScrollBar::handle:vertical {
                background-color: #c0c0c0;
                border-radius: 5px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: #a0a0a0;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
        """)
        
        # 跟帖内容容器
        self.scroll_widget = QWidget()
        self.scroll_layout = QVBoxLayout()
        self.scroll_layout.setContentsMargins(20, 20, 20, 20)
        self.scroll_layout.setSpacing(15)
        self.scroll_layout.setAlignment(QtCore.Qt.AlignTop)
        self.scroll_widget.setLayout(self.scroll_layout)
        self.scroll_area.setWidget(self.scroll_widget)
        
        # 将楼主区域和跟帖区域添加到内容布局中
        content_layout.addWidget(self.louzhu_container)
        content_layout.addWidget(self.scroll_area)
        
        # 设置内容容器
        content_container.setLayout(content_layout)
        
        # 将内容容器添加到滚动区域
        scroll_area.setWidget(content_container)
        
        # 将滚动区域添加到左侧布局
        left_layout.addWidget(scroll_area)
        left_widget.setLayout(left_layout)
        
        return left_widget

    def show_post_content(self, title, url=None):
        try:
            if url:
                posts_data = self.crawler.fetch_content(url)
                if not posts_data:
                    print("获取失败")
                    return
            else:
                print("没有URL信息，无法获取")
                return
            
            # 清空楼主内容区域
            for i in reversed(range(self.louzhu_layout.count())):
                item = self.louzhu_layout.itemAt(i)
                if item and item.widget():
                    item.widget().setParent(None)
            
            # 清空跟帖滚动区域
            for i in reversed(range(self.scroll_layout.count())):
                item = self.scroll_layout.itemAt(i)
                if item and item.widget():
                    item.widget().setParent(None)
            
            # 显示爬取到的内容
            if posts_data and "posts" in posts_data:
                theme = posts_data.get("theme", "")
                all_posts = posts_data.get("posts", [])
                
                # 创建滚动区域容器
                scroll_container = QWidget()
                scroll_layout = QVBoxLayout()
                scroll_layout.setContentsMargins(10, 10, 10, 10)
                scroll_layout.setSpacing(15)
                scroll_layout.setAlignment(QtCore.Qt.AlignTop)
                
                # 为每个帖子创建独立容器
                for post_info in all_posts:
                    # 创建帖子容器
                    post_container = QWidget()
                    
                    # 根据帖子类型设置不同的样式
                    if post_info["type"] == "楼主":
                        post_container.setStyleSheet("""
                            QWidget {
                                background-color: #f8f9fa;
                                border-radius: 15px;
                                border: 2px solid #e9ecef;
                                margin: 5px 0px;
                            }
                            QWidget:hover {
                                border-color: #007bff;
                            }
                        """)
                    else:
                        post_container.setStyleSheet("""
                            QWidget {
                                background-color: white;
                                border-radius: 12px;
                                border: 1px solid #e9ecef;
                                margin: 5px 0px;
                            }
                            QWidget:hover {
                                border-color: #007bff;
                            }
                        """)
                    
                    # 帖子内容布局
                    post_layout = QVBoxLayout()
                    post_layout.setContentsMargins(20, 20, 20, 20)
                    post_layout.setSpacing(15)
                    
                    # 帖子头部信息
                    if post_info["type"] == "楼主":
                        # 楼主主题
                        if theme:
                            theme_label = QLabel(f"📋 {theme}")
                            theme_label.setStyleSheet("""
                                QLabel {
                                    font-size: 28px; 
                                    font-weight: bold; 
                                    color: #2c3e50;
                                    padding: 15px 0px;
                                    border-bottom: 2px solid #e9ecef;
                                    margin-bottom: 15px;
                                }
                            """)
                            post_layout.addWidget(theme_label)
                        
                        # 楼主信息
                        if post_info["title"]:
                            author_label = QLabel(f"👤 楼主: {post_info['title']}")
                            author_label.setStyleSheet("""
                                QLabel {
                                    font-size: 22px; 
                                    color: #6c757d;
                                    padding: 10px 0px;
                                    background-color: #e9ecef;
                                    border-radius: 8px;
                                    padding: 12px 16px;
                                }
                            """)
                            post_layout.addWidget(author_label)
                    else:
                        # 跟帖楼层信息
                        floor_label = QLabel(f"#{post_info['floor']}楼 | 👤 {post_info['title']}")
                        floor_label.setStyleSheet("""
                            QLabel {
                                font-size: 20px; 
                                color: #6c757d;
                                padding: 8px 12px;
                                background-color: #f8f9fa;
                                border-radius: 6px;
                                font-weight: 500;
                            }
                        """)
                        post_layout.addWidget(floor_label)
                    
                    # 帖子文字内容
                    if post_info["content"]:
                        content_label = QLabel(f"💬 {post_info['content']}")
                        content_label.setStyleSheet("""
                            QLabel {
                                font-size: 22px; 
                                color: #495057;
                                padding: 20px;
                                background-color: white;
                                border-radius: 10px;
                                border-left: 4px solid #007bff;
                                line-height: 1.6;
                            }
                        """)
                        content_label.setWordWrap(True)
                        post_layout.addWidget(content_label)
                    
                    # 显示帖子图片（如果有的话）
                    if post_info["images"]:
                        for img_info in post_info["images"]:
                            self.add_image_to_layout(post_layout, img_info, post_info["type"])
                    
                    post_container.setLayout(post_layout)
                    scroll_layout.addWidget(post_container)
                
                # 添加弹性空间
                scroll_layout.addStretch()
                
                # 设置滚动容器
                scroll_container.setLayout(scroll_layout)
                
                # 将滚动容器添加到楼主区域
                self.louzhu_layout.addWidget(scroll_container)
            
            print(f"成功显示帖子内容: {title}")
            
        except Exception as e:
            print(f"显示帖子内容时出错: {e}")
            import traceback
            traceback.print_exc()
    
    def add_image_to_layout(self, layout, img_info, post_type):
        """向布局中添加图片"""
        try:
            # 创建图片容器
            image_container = QWidget()
            
            # 根据帖子类型设置不同的样式
            if post_type == "楼主":
                image_container.setStyleSheet("""
                    QWidget {
                        background-color: white;
                        border-radius: 10px;
                        padding: 15px;
                        margin: 10px 0px;
                    }
                """)
                image_size = (400, 300)
                font_size = "16px"
            else:
                image_container.setStyleSheet("""
                    QWidget {
                        background-color: #f8f9fa;
                        border-radius: 8px;
                        padding: 12px;
                        margin: 8px 0px;
                    }
                """)
                image_size = (350, 250)
                font_size = "14px"
            
            image_layout = QVBoxLayout()
            image_layout.setContentsMargins(10, 10, 10, 10)
            image_layout.setSpacing(8)
            
            # 创建图片标签
            image_label = QLabel()
            image_label.setAlignment(QtCore.Qt.AlignCenter)
            
            # 将二进制数据转换为QPixmap
            image = QImage()
            image.loadFromData(img_info["data"])
            pixmap = QPixmap.fromImage(image)
            
            # 调整图片大小，保持比例
            scaled_pixmap = pixmap.scaled(image_size[0], image_size[1], QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
            image_label.setPixmap(scaled_pixmap)
            
            # 设置图片标签样式
            image_label.setStyleSheet("""
                QLabel {
                    border: 2px solid #e9ecef;
                    border-radius: 8px;
                    padding: 5px;
                }
                QLabel:hover {
                    border-color: #007bff;
                    background-color: #f8f9fa;
                }
            """)
            
            # 设置工具提示
            image_label.setToolTip("点击以查看原图")
            
            # 设置鼠标样式
            image_label.setCursor(QtCore.Qt.PointingHandCursor)
            
            # 添加点击事件
            image_label.mousePressEvent = lambda event, url=img_info["url"]: self.open_image_url(url)
            
            # 添加图片描述
            if img_info.get("text"):
                desc_label = QLabel(img_info["text"])
                desc_label.setStyleSheet(f"""
                    QLabel {{
                        font-size: {font_size};
                        color: #6c757d;
                        text-align: center;
                        padding: 5px;
                    }}
                """)
                desc_label.setAlignment(QtCore.Qt.AlignCenter)
                image_layout.addWidget(desc_label)
            
            image_layout.addWidget(image_label)
            image_container.setLayout(image_layout)
            layout.addWidget(image_container)
            
        except Exception as e:
            print(f"添加图片到布局时出错: {e}")
            error_label = QLabel("图片加载失败")
            error_label.setStyleSheet("color: red; font-size: 16px;")
            layout.addWidget(error_label)
    
    def open_image_url(self, url):
        try:
            import webbrowser
            print(f"正在打开图片URL: {url}")
            webbrowser.open(url)
        except Exception as e:
            print(f"打开图片URL失败: {e}")
            QMessageBox.warning(self, "错误", f"无法打开图片链接: {url}")

class shuimu_craw:
    def __init__(self):
        self.dit = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 Edg/138.0.0.0"
        }
    
    def get_image_data(self, image_url):
        try:
            response = requests.get(image_url, headers=self.dit)
            if response.status_code == 200:
                return response.content
            else:
                print(f"获取图片失败: {image_url}, 状态码: {response.status_code}")
                return None
        except Exception as e:
            print(f"获取图片时出错: {e}")
            return None
    
    def fetch_content(self, url):
        try:
            r = requests.get(url, headers=self.dit)
            content = r.text
            soup = BeautifulSoup(content, "html.parser")

            ul_element = soup.find("ul", class_="list sec")
            # 存储帖子内容
            posts = []
            if ul_element:
                # 主题
                theme_element = ul_element.find("li",class_= "f")
                theme = theme_element.get_text(strip=True)
                #内容
                content_element = ul_element.find_all("div", class_="sp")
                title_element = ul_element.find_all("div", class_="nav hl")
                # 处理每个帖子同级标签
                for i,(content_element,title_element) in enumerate(zip(content_element,title_element)):
                    post_data = {
                        "type": "楼主" if i == 0 else f"跟帖#{i}",
                        "title": title_element.get_text(strip=True) if title_element else "",
                        "content": content_element.get_text(strip=True) if content_element else "",
                        "images": [],
                        "floor": i
                    }

                    img_links = content_element.find_all("a",href=True)

                    for i in img_links:
                        link = i.get("href")
                        if link:
                            # 检查是否是图片链接
                            if any(ext in link.lower() for ext in ['.jpg', '.jpeg', '.png', '.gif']) or 'static.mysmth.net' in link.lower():
                                if link.startswith("http"):
                                    full_img_link = link
                                elif link.startswith("//"):
                                    full_img_link = "https:"+link
                                elif link.startswith("/"):
                                    full_img_link = "https://m.newsmth.net"+link
                                else:
                                    full_img_link = "https://m.newsmth.net/"+link
                                
                                print(f"检测到图片链接: {link} -> {full_img_link}")
                                
                                # 获取图片数据
                                img_data = self.get_image_data(full_img_link)
                                if img_data:
                                    post_data["images"].append({
                                        "url": full_img_link,
                                        "data": img_data,
                                        "text": i.get_text(strip=True) or "图片"
                                    })
                                    print(f"成功爬取图片: {full_img_link}")
                                else:
                                    print(f"图片获取失败: {full_img_link}")
                                    # 不返回False，继续处理其他图片
                            else:
                                print(f"跳过非图片链接: {link}")
                    posts.append(post_data)
                #整体结构
                result = {
                    "theme":theme,
                    "posts":posts
                }
                return result
            else:
                print("ul_element不存在,失败")
                return False
        except Exception as e:
            print(f"抓取失败{str(e)}")
            return False

class PostManager:
    class PostWidget(QWidget):
        def __init__(self, post_data, parent=None):
            super().__init__(parent)
            self.post_data = post_data
            self.init_ui()
        
        def init_ui(self):
            self.setFixedHeight(140)  # 增加高度以容纳两行信息
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
            layout.setContentsMargins(12, 10, 12, 10)
            layout.setSpacing(6)
            
            # 标题 - 改为按钮
            title_button = QPushButton(self.post_data["title"])
            title_button.setCursor(QtCore.Qt.PointingHandCursor)  # 鼠标悬停时显示手型光标
            title_button.setStyleSheet("""
                QPushButton {
                    font-weight: bold;
                    color: #2c3e50;
                    font-size: 18px;
                    line-height: 1.4;
                    padding: 3px 0px;
                    margin-bottom: 4px;
                    background: transparent;
                    border: none;
                    text-align: left;
                }
                QPushButton:hover {
                    color: #3498db;
                }
            """)
            
            # 添加点击事件
            title_button.clicked.connect(self.on_title_clicked)
            
            # 第一行：作者 与 时间
            author_text = self.post_data.get('author', '')
            create_time_text = self.post_data.get('create_time', '')
            info_label = QLabel(f"作者: {author_text} | 时间: {create_time_text}")
            info_label.setStyleSheet("""
                QLabel {
                    color: #7f8c8d;
                    font-size: 16px;
                    padding: 3px 0px;
                    margin-top: 2px;
                }
            """)
            
            # 第二行：最近回复时间 与 回复账户
            last_reply_time_text = self.post_data.get('last_reply_time', '')
            reply_user_text = self.post_data.get('reply_count', '')
            second_line = []
            if last_reply_time_text:
                second_line.append(f"最近回复: {last_reply_time_text}")
            if reply_user_text:
                second_line.append(f"回复账户: {reply_user_text}")
            second_info_label = QLabel(" | ".join(second_line)) if second_line else QLabel("")
            second_info_label.setStyleSheet("""
                QLabel {
                    color: #7f8c8d;
                    font-size: 16px;
                    padding: 0px 0px 3px 0px;
                }
            """)
            
            layout.addWidget(title_button)
            layout.addWidget(info_label)
            layout.addWidget(second_info_label)
            
            self.setLayout(layout)
        
        def sizeHint(self):
            """返回建议的大小"""
            return QSize(300, 120)
        
        def mousePressEvent(self, event):
            """鼠标点击事件"""
            if event.button() == QtCore.Qt.LeftButton:
                # 发送信号给主窗口
                main_window = self.window()
                if hasattr(main_window, 'on_post_selected'):
                    main_window.on_post_selected(self.post_data)

        def on_title_clicked(self):
            try:
                main_window = self.window()
                if hasattr(main_window, 'show_post_content'):
                    # 获取帖子的URL和标题
                    title = self.post_data.get("title", "")
                    url = self.post_data.get("url", "")
                    
                    if url:
                        main_window.show_post_content(title, url)
                    else:
                        main_window.show_post_content(title)
                else:
                    print("主窗口没有show_post_content方法")
            except Exception as e:
                print(f"处理标题点击事件时出错: {e}")
                import traceback
                traceback.print_exc()
    
    class PostsListWidget(QWidget):
        def __init__(self, parent=None):
            super().__init__(parent)
            self.current_board = None
            self.sort_by = "create_time"  # create_time 或 last_reply_time
            self.posts_layout = None  # 将在外部设置
            self.init_ui()
        
        def init_ui(self):
            layout = QVBoxLayout()
            
            # 工具栏
            toolbar_layout = QHBoxLayout()
            
            self.board_label = QLabel("版块: 未选择")
            self.board_label.setStyleSheet("font-weight: bold; color: #2c3e50;")
            
            self.sort_combo = QComboBox()
            self.sort_combo.addItems(["按创建时间排序", "按最近回复时间排序"])
            self.sort_combo.currentTextChanged.connect(self.on_sort_changed)
            
            self.refresh_btn = QPushButton("刷新")
            self.refresh_btn.clicked.connect(self.refresh_posts)
            
            toolbar_layout.addWidget(self.board_label)
            toolbar_layout.addStretch()
            toolbar_layout.addWidget(QLabel("排序:"))
            toolbar_layout.addWidget(self.sort_combo)
            toolbar_layout.addWidget(self.refresh_btn)
            
            layout.addLayout(toolbar_layout)
            
            # 帖子列表区域将在外部设置
            self.setLayout(layout)
        
        def set_board(self, board_name: str, board_title: str):
            self.current_board = board_name
            self.board_label.setText(f"版块: {board_title}")
            self.refresh_posts()
        
        def set_posts_layout(self, posts_layout):
            self.posts_layout = posts_layout
        
        def on_sort_changed(self, text: str):
            if "创建时间" in text:
                self.sort_by = "create_time"
            else:
                self.sort_by = "最近回复时间"
            self.refresh_posts()
        
        def refresh_posts(self):
            """刷新帖子列表"""
            if not self.current_board or not self.posts_layout:
                return
            
            # 通知主窗口刷新帖子
            main_window = self.window()
            if hasattr(main_window, 'refresh_posts'):
                main_window.refresh_posts()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = window()
    w.show()
    app.exec()

