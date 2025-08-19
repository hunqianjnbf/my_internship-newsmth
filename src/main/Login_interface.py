# -*- coding: utf-8 -*-
import sys
import json
from PyQt5.QtCore import QPoint,pyqtSignal,Qt
from PyQt5.QtGui import QMouseEvent, QCursor, QIcon, QImage, QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLineEdit, QTextBrowser, QMessageBox, \
    QHBoxLayout, QScrollArea, QLabel, QMainWindow, QAction, QMenu, qApp, QTextEdit, QToolBar, QDialog, QFrame, \
    QSpacerItem, QSizePolicy, QCheckBox
import requests,time
from PyQt5 import QtCore
from PyQt5.Qt import QThread


class LoginDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):

        self.setWindowTitle('登陆界面')
        self.setWindowIcon(QIcon("C:/Users/17256/PycharmProjects/pythonProject/picture/login.png"))
        self.resize(750, 490)
        self.setFixedSize(self.width(), self.height())
        self.setFixedSize(self.width(), self.height())
        self.setWindowFlags(Qt.Dialog | Qt.WindowCloseButtonHint)

        self.back_img = QLabel(self)  # 设置父控件为当前窗口
        self.back_img.resize(self.width(), self.height())
        self.back_img.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        pixmap = QPixmap("C:/Users/17256/PycharmProjects/pythonProject/picture/Login background.jpg")
        pixmap = pixmap.scaled(self.back_img.size(), Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
        self.back_img.setPixmap(pixmap)
        self.back_img.setScaledContents(True)
        self.back_img.setAlignment(Qt.AlignBottom | Qt.AlignRight)
        self.back_img.lower()  # 把图片放在最底层


        self.back_img.setPixmap(pixmap)
        self.back_img.setScaledContents(True)
        self.back_img.setAlignment(Qt.AlignBottom | Qt.AlignRight)

        self.login_container= QFrame(self)
        self.login_layout = QHBoxLayout(self.login_container) #确保整个控件水平居中

        self.content_layout = QVBoxLayout() #主存放内容区域为垂直布局
        self.content_layout.setContentsMargins(0,0,0,0)
        self.content_layout.addWidget(QLabel()) #创建一个空label作为顶部占位

        self.log_hlayout = QHBoxLayout() #头像+输入框水平布局

        #头像区域
        log_img = QLabel()
        log_img.resize(250,250)
        log_img.setStyleSheet("border:1px solid #aaa;")
        img = QImage()
        img.load("C:/Users/17256/PycharmProjects/pythonProject/picture/login.png")
        pic = QPixmap.fromImage(img.scaled(log_img.size(), Qt.IgnoreAspectRatio)) #缩放图片适应标签尺寸
        pic.scaled(log_img.size(), Qt.IgnoreAspectRatio)
        log_img.setPixmap(pic)
        self.log_hlayout.addWidget(log_img)

        #账号密码输入区域
        self.zhangmi_layout = QVBoxLayout()
        #账号
        self.shuru_hlay = QHBoxLayout()
        self.account = QLabel("账号：")
        self.account_lineEdit = QLineEdit()
        self.account_lineEdit.setPlaceholderText("请输入账号")
        self.hSpacer = QSpacerItem(10, 10, QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.shuru_hlay.addItem(self.hSpacer)
        self.shuru_hlay.addWidget(self.account)
        self.shuru_hlay.addWidget(self.account_lineEdit)
        #密码
        self.shuru_hlay1 = QHBoxLayout()
        self.password = QLabel("密码：")
        self.password_lineEdit = QLineEdit()
        self.password_lineEdit.setPlaceholderText("请输入密码")
        self.hSpacer = QSpacerItem(10, 10, QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.shuru_hlay1.addItem(self.hSpacer)
        self.shuru_hlay1.addWidget(self.password)
        self.shuru_hlay1.addWidget(self.password_lineEdit)

        #注册账号和找回密码区域
        self.btn_layout = QHBoxLayout()
        self.btn_layout.setContentsMargins(290,10,10,25)
        self.btn = QPushButton("注册账号")
        self.btn1 = QPushButton("找回密码")
        self.btn.setStyleSheet(self.btn_style())
        self.btn1.setStyleSheet(self.btn_style())

        self.btn_layout.addWidget(self.btn)
        self.btn_layout.addWidget(self.btn1)

        self.zhangmi_layout.addLayout(self.shuru_hlay)
        self.zhangmi_layout.addLayout(self.shuru_hlay1)

        self.log_hlayout.addLayout(self.zhangmi_layout)

        self.content_layout.addLayout(self.log_hlayout)
        self.content_layout.addLayout(self.btn_layout)

        #复选框区域
        self.choose_lay = QHBoxLayout()
        self.cb1 = QCheckBox("记住密码")
        self.cb2 = QCheckBox("自动登录")
        self.hSpacer = QSpacerItem(10, 10, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.choose_lay.addItem(self.hSpacer)
        self.choose_lay.addWidget(self.cb1)
        self.hSpacer = QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.choose_lay.addItem(self.hSpacer)
        self.choose_lay.addWidget(self.cb2)
        self.hSpacer = QSpacerItem(10, 10, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.choose_lay.addItem(self.hSpacer)

        self.content_layout.addLayout(self.choose_lay)
        #登录按钮
        self.s_hlay = QHBoxLayout()
        self.btn_enter = QPushButton()
        self.btn_enter.setText("登陆")
        self.btn_enter.setStyleSheet("background:#975;")
        self.btn_enter.clicked.connect(self.judge_login)
        hSpacer = QSpacerItem(10, 10, QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.s_hlay.addItem(hSpacer)
        self.s_hlay.addWidget(self.btn_enter)
        self.content_layout.addLayout(self.s_hlay)
        #两侧添加弹簧
        hSpacer = QSpacerItem(10, 10, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.login_layout.addItem(hSpacer)
        self.login_layout.addLayout(self.content_layout)
        hSpacer = QSpacerItem(10, 10, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.login_layout.addItem(hSpacer)

        self.setLayout(self.login_layout)
    def username(self):
        username1 = self.account_lineEdit.text()
    def password(self):
        password1 = self.password_lineEdit.text()
    def judge_login(self):
        username1 = self.account_lineEdit.text().strip()
        password1 = self.password_lineEdit.text().strip()

        if not username1:
            QMessageBox.warning(self, "输入错误", "账号不能为空")
            return
        if not password1:
            QMessageBox.warning(self, "输入错误", "密码不能为空")
            return

    def btn_style(self):

        self.btn_style1 = (
            """QPushButton{
        color:#333;
        font-family: 微软雅黑,宋体,Arial,Helvetica,Verdana,sans-serif;
        background-color: transparent;
        border:0px solid white;border-radius:10px;
    }
    QPushButton:hover{
        color:#333;
        font-family: 微软雅黑,宋体,Arial,Helvetica,Verdana,sans-serif;
        background-color: transparent;
        border:0px solid white;border-radius:10px;
    }

    QPushButton:pressed{
        color:#333;
        font-family: 微软雅黑,宋体,Arial,Helvetica,Verdana,sans-serif;
        background-color: transparent;
        border:0px solid white;border-radius:10px;
        padding-left:3px;
        padding-top:3px;
    }
"""
)
        return self.btn_style1


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = LoginDialog()
    w.show()
    app.exec()
