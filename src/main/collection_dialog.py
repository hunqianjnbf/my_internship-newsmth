import sys
import json
from PyQt5.QtCore import QPoint,pyqtSignal,Qt
from PyQt5.QtGui import QMouseEvent, QCursor, QIcon, QImage, QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLineEdit, QTextBrowser, QMessageBox, \
    QHBoxLayout, QScrollArea, QLabel, QMainWindow, QAction, QMenu, qApp, QTextEdit, QToolBar, QDialog, QFrame, \
    QSpacerItem, QSizePolicy, QCheckBox

from choose_boardGUI import banmian

class CollectionDialog(QDialog):
    # 添加退出信号，用于通知主界面刷新
    dialog_closed = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.delete_mode = False  # 初始化删除模式
        self.favorite_board = []  # 初始化收藏版面列表
        self.btn_style()
        self.init_ui()
        self.load_favorites()  # 加载收藏数据

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
        
        # 新增收藏版面QLineEdit的样式
        self.favorite_board_edit_style = ("""
            QLineEdit {
                font-size: 18px;
                padding: 12px 16px;
                border: 2px solid #e9ecef;
                border-radius: 8px;
                background-color: #ffffff;
                color: #2c3e50;
                margin: 4px 8px;
                min-height: 25px;
                font-weight: 500;
            }
            QLineEdit:hover {
                border-color: #007bff;
                background-color: #f8f9fa;
                box-shadow: 0 2px 8px rgba(0, 123, 255, 0.1);
            }
            QLineEdit:focus {
                border-color: #007bff;
                background-color: #ffffff;
                box-shadow: 0 0 0 3px rgba(0, 123, 255, 0.1);
            }
        """)
        
        # 收藏版面容器样式
        self.favorite_container_style = ("""
            QWidget {
                background-color: #ffffff;
                border-radius: 8px;
                padding: 10px;
            }
        """)
        
        # 增强的底部按钮样式
        self.enhanced_button_style = ("""
            QPushButton {
                font-size: 16px;
                font-weight: bold;
                padding: 10px 20px;
                border: 2px solid #007bff;
                border-radius: 8px;
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #ffffff, stop:1 #f0f8ff);
                color: #007bff;
                min-width: 120px;
                min-height: 45px;
                max-height: 50px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #f0f8ff, stop:1 #e6f3ff);
                border-color: #0056b3;
                color: #0056b3;
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #e6f3ff, stop:1 #d1ecf1);
                border-color: #004085;
                color: #004085;
            }
        """)

    def init_ui(self):
        self.setWindowTitle('收藏夹')
        self.resize(1250, 990)
        self.setWindowIcon(QIcon("C:/Users/17256/PycharmProjects/pythonProject/picture/favorites.png"))

        self.setFixedSize(self.width(), self.height())
        self.setWindowFlags(Qt.Dialog | Qt.WindowCloseButtonHint)
        self.setStyleSheet("""
            QDialog {
                background-color: #f8f9fa;
            }
        """)
        whole_layout = QVBoxLayout()

        # 标题
        self.title_label = QLabel('已收藏的版面')
        self.title_label.setStyleSheet(self.title_label_style)
        self.title_label.setAlignment(Qt.AlignCenter)
        whole_layout.addWidget(self.title_label, 1)

        # 已收藏的版面滚动区域
        self.create_favorite_boards_scroll_area(whole_layout, 10)
        whole_layout.addSpacing(20)
        
        # 底部按钮区域
        self.create_bottom_buttons(whole_layout)

        self.setLayout(whole_layout)

    def create_favorite_boards_scroll_area(self, parent_layout, stretch_ratio=3):
        # 创建滚动区域
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet(self.favorite_scroll_style)
        # 根据拉伸比例调整滚动区域的高度
        if stretch_ratio >= 5:
            scroll_area.setMinimumHeight(800)
            scroll_area.setMaximumHeight(900)
        else:
            scroll_area.setMinimumHeight(600)
            scroll_area.setMaximumHeight(700)
        
        # 创建容器widget
        container = QWidget()
        container.setStyleSheet(self.favorite_container_style)
        container_layout = QVBoxLayout(container)
        
        try:
            # 读取收藏数据
            with open("favorites.json", "r", encoding="utf-8") as f:
                data = json.load(f)
            
            if isinstance(data, dict) and "收藏的版块" in data:
                board_data = data["收藏的版块"]
                
                if board_data:
                    # 为每个收藏的版面创建QLineEdit
                    for board_name in board_data:
                        board_edit = self.create_board_line_edit(board_name)
                        container_layout.addWidget(board_edit)
                    
                    # 添加弹性空间
                    container_layout.addStretch()
                else:
                    # 如果没有收藏的版面，显示提示信息
                    no_favorites_label = QLabel("暂无收藏的版面")
                    no_favorites_label.setStyleSheet("""
                        QLabel {
                            font-size: 18px;
                            color: #6c757d;
                            padding: 40px;
                            text-align: center;
                        }
                    """)
                    no_favorites_label.setAlignment(Qt.AlignCenter)
                    container_layout.addWidget(no_favorites_label)
                    container_layout.addStretch()
            else:
                # 数据格式错误时的提示
                error_label = QLabel("数据格式错误")
                error_label.setStyleSheet("""
                    QLabel {
                        font-size: 18px;
                        color: #dc3545;
                        padding: 40px;
                        text-align: center;
                    }
                """)
                error_label.setAlignment(Qt.AlignCenter)
                container_layout.addWidget(error_label)
                container_layout.addStretch()
                
        except FileNotFoundError:
            # 文件不存在时的提示
            no_file_label = QLabel("收藏文件不存在")
            no_file_label.setStyleSheet("""
                QLabel {
                    font-size: 18px;
                    color: #dc3545;
                    padding: 40px;
                    text-align: center;
                }
            """)
            no_file_label.setAlignment(Qt.AlignCenter)
            container_layout.addWidget(no_file_label)
            container_layout.addStretch()
        except Exception as e:
            # 其他错误时的提示
            error_label = QLabel(f"读取数据时出错: {str(e)}")
            error_label.setStyleSheet("""
                QLabel {
                    font-size: 18px;
                    color: #dc3545;
                    padding: 40px;
                    text-align: center;
                }
            """)
            error_label.setAlignment(Qt.AlignCenter)
            container_layout.addWidget(error_label)
            container_layout.addStretch()
        
        # 设置容器布局
        container.setLayout(container_layout)
        scroll_area.setWidget(container)
        
        # 将滚动区域添加到主布局，设置拉伸比例为3
        parent_layout.addWidget(scroll_area, stretch_ratio)

    def create_board_line_edit(self, board_name):
        """为单个版面创建QLineEdit"""
        board_edit = QLineEdit()
        board_edit.setText(board_name)
        board_edit.setReadOnly(True)  # 设置为只读
        board_edit.setStyleSheet(self.favorite_board_edit_style)
        
        # 设置工具提示
        if hasattr(self, 'delete_mode') and self.delete_mode:
            board_edit.setToolTip(f"点击删除版面: {board_name}")
            board_edit.setCursor(Qt.PointingHandCursor)
            # 为删除模式添加点击事件
            board_edit.mousePressEvent = lambda event: self.delete_board(board_name)
        else:
            board_edit.setToolTip(f"收藏的版面: {board_name}")
            board_edit.setCursor(Qt.ArrowCursor)
        
        return board_edit

    def create_bottom_buttons(self, parent_layout):
        """创建底部按钮区域"""
        button_layout = QHBoxLayout()
        button_layout.setSpacing(20)  # 按钮之间的间距
        
        # 添加收藏按钮
        self.add_btn = QPushButton("添加收藏")
        self.add_btn.setStyleSheet(self.enhanced_button_style)
        self.add_btn.setMinimumHeight(45)
        self.add_btn.setMinimumWidth(120)
        self.add_btn.setMaximumHeight(50)
        self.add_btn.setMaximumWidth(150)
        self.add_btn.clicked.connect(self.butn_clicked)
        
        # 删除版面按钮
        self.delete_btn = QPushButton("删除版面")
        self.delete_btn.setStyleSheet(self.enhanced_button_style)
        self.delete_btn.setMinimumHeight(45)
        self.delete_btn.setMinimumWidth(120)
        self.delete_btn.setMaximumHeight(50)
        self.delete_btn.setMaximumWidth(150)
        self.delete_btn.clicked.connect(self.butn1_clicked)
        
        # 添加弹性空间，让按钮居中
        button_layout.addStretch()
        button_layout.addWidget(self.add_btn)
        button_layout.addWidget(self.delete_btn)
        button_layout.addStretch()
        
        parent_layout.addLayout(button_layout)

    def load_favorites(self):
        """加载收藏数据"""
        try:
            with open("favorites.json", "r", encoding="utf-8") as f:
                favorites = json.load(f)
                return favorites.get("收藏的版块", [])
        except FileNotFoundError:
            print("没有找到文件")
            return []
        except json.JSONDecodeError:
            print("Json文件格式错误")
            return []
        except Exception as e:
            print(f"读取Json文件时发生错误{str(e)}")
            return []

    def butn_clicked(self):
        """添加收藏按钮点击事件"""
        try:
            # 创建版面选择对话框
            bm = banmian()
            result = bm.exec_()

            # 如果对话框被接受，处理选择的版块
            if result == QDialog.Accepted:
                # 从版面选择对话框获取选择的版块
                new_boards = bm.get_selected_boards()

                if new_boards:
                    # 获取现有的收藏版面
                    existing_boards = self.load_favorites()
                    
                    # 合并现有版面和新选择的版面，去重
                    combined_boards = self.merge_boards(existing_boards, new_boards)
                    
                    # 更新JSON文件，使用追加模式
                    self.save_favorites(combined_boards, append_mode=True)
                    print(f"已添加新收藏的版块: {new_boards}")
                    print(f"当前所有收藏版块: {combined_boards}")
                    
                    # 刷新界面显示新的收藏内容
                    self.refresh_ui()
                    
                    # 发送信号通知主界面刷新
                    self.dialog_closed.emit()
                else:
                    print("没有选择任何版块")
                    QMessageBox.information(self, "提示", "没有选择任何版块")
            else:
                print("用户取消了版块选择")

        except Exception as e:
            print(f"添加收藏时出错: {e}")
            QMessageBox.warning(self, "错误", f"添加收藏失败: {str(e)}")

    def replace_all_favorites(self):
        try:
            # 这个方法现在主要用于兼容性，实际功能已在butn_clicked中实现
            print("replace_all_favorites方法被调用，但主要功能已在butn_clicked中实现")
        except Exception as e:
            print(f"replace_all_favorites出错: {e}")

    def merge_boards(self, existing_boards, new_boards):
        """合并现有版面和新选择的版面，去重处理"""
        try:
            # 创建现有版面的集合，用于快速查找
            existing_set = set(existing_boards)
            
            # 合并版面列表
            combined_boards = existing_boards.copy()  # 复制现有版面
            
            # 添加新选择的版面，如果重复则覆盖（替换）
            for new_board in new_boards:
                if new_board in existing_set:
                    # 如果版面已存在，找到位置并替换
                    try:
                        index = combined_boards.index(new_board)
                        combined_boards[index] = new_board  # 实际上位置不变，但确保内容一致
                        print(f"版面 '{new_board}' 已存在，保持原位置")
                    except ValueError:
                        # 如果找不到索引，直接添加（这种情况理论上不会发生）
                        combined_boards.append(new_board)
                else:
                    # 如果版面不存在，添加到末尾
                    combined_boards.append(new_board)
                    print(f"新增版面: '{new_board}'")
            
            print(f"合并前版面数量: {len(existing_boards)}")
            print(f"新增版面数量: {len(new_boards)}")
            print(f"合并后版面数量: {len(combined_boards)}")
            
            return combined_boards
            
        except Exception as e:
            print(f"合并版面时出错: {e}")
            # 如果合并出错，返回现有版面
            return existing_boards

    def save_favorites(self, boards, append_mode=False):
        """
        保存收藏版块到JSON文件
        :param boards: 要保存的版块列表
        :param append_mode: 是否为追加模式，True为追加，False为替换
        """
        try:
            # 读取现有数据
            existing_data = {}
            try:
                with open("favorites.json", "r", encoding="utf-8") as f:
                    existing_data = json.load(f)
            except FileNotFoundError:
                existing_data = {"收藏的版块": [], "收藏的版块详情": []}
            except json.JSONDecodeError:
                existing_data = {"收藏的版块": [], "收藏的版块详情": []}

            if append_mode:
                # 追加模式：合并现有版块和新版块，去重
                existing_boards = existing_data.get("收藏的版块", [])
                existing_details = existing_data.get("收藏的版块详情", [])
                
                # 合并版块列表，去重
                combined_boards = existing_boards.copy()
                for board in boards:
                    if board not in combined_boards:
                        combined_boards.append(board)
                
                # 更新收藏的版块详情，保留现有的，添加新的
                updated_details = existing_details.copy()
                # 这里可以根据需要添加新的版块详情逻辑
                
                data = {
                    "收藏的版块": combined_boards,
                    "收藏的版块详情": updated_details
                }
                
                # 更新内部状态为合并后的结果
                self.favorite_board = combined_boards
            else:
                # 替换模式：完全替换现有数据
                data = {"收藏的版块": boards}

                # 如果有现有的收藏的版块详情，需要同步更新
                if "收藏的版块详情" in existing_data:
                    # 过滤掉已删除的版块详情
                    updated_details = []
                    for detail in existing_data["收藏的版块详情"]:
                        if detail["name"] in boards:
                            updated_details.append(detail)
                    data["收藏的版块详情"] = updated_details
                
                # 更新内部状态
                self.favorite_board = boards

            # 保存到文件
            with open("favorites.json", "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
                
        except Exception as e:
            print(f"保存收藏版块时出错: {e}")
            raise e

    def butn1_clicked(self):
        try:
            if hasattr(self, 'delete_mode') and self.delete_mode:
                # 退出删除模式
                self.delete_mode = False
                self.delete_btn.setText("删除版面")
                self.delete_btn.setStyleSheet(self.enhanced_button_style)
                self.refresh_ui()
            else:
                # 进入删除模式
                self.delete_mode = True
                self.delete_btn.setText("退出删除")
                self.delete_btn.setStyleSheet("""
                    QPushButton {
                        font-size: 16px;
                        font-weight: bold;
                        padding: 10px 20px;
                        border: 2px solid #dc3545;
                        border-radius: 8px;
                        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                            stop:0 #ff6b6b, stop:1 #dc3545);
                        color: white;
                        min-width: 120px;
                        min-height: 45px;
                        max-height: 50px;
                    }
                    QPushButton:hover {
                        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                            stop:0 #dc3545, stop:1 #c82333);
                        border-color: #c82333;
                    }
                    QPushButton:pressed {
                        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                            stop:0 #c82333, stop:1 #bd2130);
                        border-color: #bd2130;
                    }
                """)
                self.refresh_ui()
                QMessageBox.information(self, "提示", "已进入删除模式，点击版面可删除")
        except Exception as e:
            print(f"切换删除模式时出错: {e}")
            QMessageBox.warning(self, "错误", f"操作失败: {str(e)}")

    def delete_board(self, board_name):
        """删除指定版面"""
        try:
            # 确认删除
            reply = QMessageBox.question(self, "确认删除", 
                                       f"确定要删除版面 '{board_name}' 吗？",
                                       QMessageBox.Yes | QMessageBox.No, 
                                       QMessageBox.No)
            
            if reply == QMessageBox.Yes:
                # 从收藏列表中移除
                if board_name in self.favorite_board:
                    self.favorite_board.remove(board_name)

                    # 保存到JSON，使用替换模式（因为删除后需要更新整个列表）
                    self.save_favorites(self.favorite_board, append_mode=False)

                    # 刷新UI
                    self.refresh_ui()
                    
                    # 发送信号通知主界面刷新
                    self.dialog_closed.emit()

                    print(f"已删除版块: {board_name}")

        except Exception as e:
            print(f"删除版块时出错: {e}")
            import traceback
            traceback.print_exc()
            QMessageBox.warning(self, "错误", f"删除版块失败: {str(e)}")

    def refresh_ui(self):
        """刷新UI界面（只刷新收藏列表，不关闭对话框）"""
        try:
            # 重新加载数据
            self.favorite_board = self.load_favorites()
            
            # 只刷新收藏内容区域，不重新初始化整个UI
            self.refresh_favorite_content()
            
        except Exception as e:
            print(f"刷新UI时出错: {e}")
            QMessageBox.warning(self, "错误", f"刷新界面失败: {str(e)}")

    def refresh_favorite_content(self):
        try:
            # 找到滚动区域容器
            scroll_area = None
            container = None
            
            # 遍历主布局寻找滚动区域
            main_layout = self.layout()
            if main_layout:
                for i in range(main_layout.count()):
                    item = main_layout.itemAt(i)
                    if item and item.widget():
                        widget = item.widget()
                        if isinstance(widget, QScrollArea):
                            scroll_area = widget
                            container = scroll_area.widget()
                            break
            
            if scroll_area and container:
                # 清空现有的内容
                container_layout = container.layout()
                if container_layout:
                    for i in reversed(range(container_layout.count())):
                        item = container_layout.itemAt(i)
                        if item and item.widget():
                            item.widget().setParent(None)
                
                # 重新加载收藏数据并创建新的版面编辑框
                try:
                    with open("favorites.json", "r", encoding="utf-8") as f:
                        data = json.load(f)
                    
                    if isinstance(data, dict) and "收藏的版块" in data:
                        board_data = data["收藏的版块"]
                        
                        if board_data:
                            # 为每个收藏的版面创建QLineEdit
                            for board_name in board_data:
                                board_edit = self.create_board_line_edit(board_name)
                                container_layout.addWidget(board_edit)

                        else:
                            # 如果没有收藏的版面，显示提示信息
                            no_favorites_label = QLabel("暂无收藏的版面")
                            no_favorites_label.setStyleSheet("""
                                QLabel {
                                    font-size: 18px;
                                    color: #6c757d;
                                    padding: 40px;
                                    text-align: center;
                                }
                            """)
                            no_favorites_label.setAlignment(Qt.AlignCenter)
                            container_layout.addWidget(no_favorites_label)

                    else:
                        # 数据格式错误时的提示
                        error_label = QLabel("数据格式错误")
                        error_label.setStyleSheet("""
                            QLabel {
                                font-size: 18px;
                                color: #dc3545;
                                padding: 40px;
                                text-align: center;
                            }
                        """)
                        error_label.setAlignment(Qt.AlignCenter)
                        container_layout.addWidget(error_label)

                        
                except FileNotFoundError:
                    # 文件不存在时的提示
                    no_file_label = QLabel("收藏文件不存在")
                    no_file_label.setStyleSheet("""
                        QLabel {
                            font-size: 18px;
                            color: #dc3545;
                            padding: 40px;
                            text-align: center;
                        }
                    """)
                    no_file_label.setAlignment(Qt.AlignCenter)
                    container_layout.addWidget(no_file_label)

                except Exception as e:
                    # 其他错误时的提示
                    error_label = QLabel(f"读取数据时出错: {str(e)}")
                    error_label.setStyleSheet("""
                        QLabel {
                            font-size: 18px;
                            color: #dc3545;
                            padding: 40px;
                            text-align: center;
                        }
                    """)
                    error_label.setAlignment(Qt.AlignCenter)
                    container_layout.addWidget(error_label)
                
                print("收藏列表已刷新")
            else:
                print("未找到滚动区域，使用完整UI刷新")
                # 如果找不到滚动区域，作为后备方案重新初始化UI
                self.init_ui()
                
        except Exception as e:
            print(f"刷新收藏内容时出错: {e}")
            # 出错时作为后备方案重新初始化UI
            self.init_ui()

    def closeEvent(self, event):
        """重写关闭事件，发送退出信号"""
        try:
            print("收藏夹对话框即将关闭，发送退出信号")
            # 发送退出信号，通知主界面刷新
            self.dialog_closed.emit()
            # 接受关闭事件
            event.accept()
        except Exception as e:
            print(f"发送退出信号时出错: {e}")
            # 即使出错也要接受关闭事件
            event.accept()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = CollectionDialog()
    w.show()
    app.exec_()