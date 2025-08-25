def show_top10_title(self):
    """��ʾtop10���������"""
    try:
        print("��ʼ��ʾtop10����...")

        # ������е�top10����
        for i in reversed(range(self.top10_layout.count())):
            item = self.top10_layout.itemAt(i)
            if item and item.widget():
                item.widget().setParent(None)

        # ���top10����
        top10_title = QLabel("? Top10 ���Ż���")
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

        # ��ȡtop10����
        m = top10_craw()
        top10_data = m.fetch_top10()

        if not top10_data or len(top10_data) == 0:
            print("δ��ȡ��top10����")
            # �����ʾ��ǩ
            no_data_label = QLabel("����top10����")
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

        print(f"�ɹ���ȡ�� {len(top10_data)} ��top10��Ŀ")

        # Ϊÿ��top10��Ŀ�������ⰴť
        for i, item in enumerate(top10_data, 1):
            title_button = self.create_top10_title_button(i, item)
            self.top10_layout.addWidget(title_button)

        print("top10������ʾ���")

    except Exception as e:
        print(f"��ʾtop10����ʧ��: {str(e)}")
        import traceback
        traceback.print_exc()


def create_top10_title_button(self, index, item):
    """����top10���ⰴť"""
    try:
        # ��������
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

        # ���ⰴť
        title_button = QPushButton(f"{index}. {item['����']}")
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

        # �󶨵���¼�
        url = item['��������']
        title_button.clicked.connect(lambda checked, u=url: self.show_top10_content("", u))

        layout.addWidget(title_button)
        container.setLayout(layout)

        return container

    except Exception as e:
        print(f"����top10���ⰴťʧ��: {str(e)}")
        # ����һ�������ǩ
        error_label = QLabel(f"������ťʧ��: {str(e)}")
        error_label.setStyleSheet("color: red; font-size: 12px;")
        return error_label