def show_top10_title(self):
    """显示top10标题和内容"""
    try:
        print("开始显示top10标题...")

        # 清空现有的top10内容
        for i in reversed(range(self.top10_layout.count())):
            item = self.top10_layout.itemAt(i)
            if item and item.widget():
                item.widget().setParent(None)

        # 添加top10标题
        top10_title = QLabel("? Top10 热门话题")
        top10_title.setStyleSheet("""
            QLabel {
                font-size: 24px;
                font-weight: bold;
                color: #1976D2;
                font-family: 'Segoe UI', Arial, sans-serif;
                padding: 10px 0px;
                border-bottom: 2px solid #E3F2FD;
                margin-bottom: 15px;
            }
        """)
        self.top10_layout.addWidget(top10_title)

        # 获取top10数据
        m = top10_craw()
        top10_data = m.fetch_top10()

        if not top10_data or len(top10_data) == 0:
            print("未获取到top10数据")
            # 添加提示标签
            no_data_label = QLabel("暂无top10数据")
            no_data_label.setStyleSheet("""
                QLabel {
                    color: #757575;
                    font-size: 16px;
                    font-style: italic;
                    padding: 20px;
                    text-align: center;
                }
            """)
            self.top10_layout.addWidget(no_data_label)
            return

        print(f"成功获取到 {len(top10_data)} 个top10项目")

        # 为每个top10项目创建标题按钮
        for i, item in enumerate(top10_data, 1):
            title_button = self.create_top10_title_button(i, item)
            self.top10_layout.addWidget(title_button)

        print("top10标题显示完成")

    except Exception as e:
        print(f"显示top10标题失败: {str(e)}")
        import traceback
        traceback.print_exc()


def create_top10_title_button(self, index, item):
    """创建top10标题按钮"""
    try:
        # 创建容器
        container = QWidget()
        container.setFixedHeight(80)
        container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        container.setStyleSheet("""
            QWidget {
                background: transparent;
                border: none;
                margin: 4px 0px;
                padding: 0px;
            }
            QWidget:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(33, 150, 243, 0.05), stop:1 rgba(33, 150, 243, 0.02));
                border-radius: 12px;
            }
        """)

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 8, 0, 8)
        layout.setSpacing(5)

        # 标题按钮
        title_button = QPushButton(f"{index}. {item['标题']}")
        title_button.setCursor(QtCore.Qt.PointingHandCursor)
        title_button.setStyleSheet("""
            QPushButton {
                font-weight: 700;
                color: #1a237e;
                font-size: 18px;
                font-family: 'Segoe UI', Arial, sans-serif;
                line-height: 1.3;
                padding: 8px 0px;
                margin: 0px;
                background: transparent;
                border: none;
                text-align: left;
                border-radius: 0px;
                min-height: 25px;
            }
            QPushButton:hover {
                color: #1565c0;
                background: transparent;
                text-decoration: underline;
            }
        """)

        # 绑定点击事件
        url = item['文章链接']
        title_button.clicked.connect(lambda checked, u=url: self.show_top10_content("", u))

        layout.addWidget(title_button)
        container.setLayout(layout)

        return container

    except Exception as e:
        print(f"创建top10标题按钮失败: {str(e)}")
        # 返回一个错误标签
        error_label = QLabel(f"创建按钮失败: {str(e)}")
        error_label.setStyleSheet("color: red; font-size: 12px;")
        return error_label