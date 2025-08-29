# 水木社区客户端

一个基于PyQt5客户端界面设计以及网络爬虫,通过PYQT5设计出简单的客户端界面再通过

## 功能特性

-  **PyQt5 GUI界面** - 现代化的用户界面
-  **网络爬虫** - 支持多线程爬取
-  **自动登录** - 目前还未实现
-  **多平台支持** - 支持newsmth阅读帖子
-  **自定义主题** - 支持背景图片和图标

## 项目结构

```
pythonProject/
├── src/                    # 源代码目录
│   ├── gui/               # GUI相关代码
│   ├── scrapers/          # 爬虫模块
│   └── login/             # 登录模块(还未完善)
│   
├── examples/               # 示例代码
├── docs/                  # 文档
├── tests/                 # 测试代码
├── requirements.txt       # 依赖包
└──setup.py              # 安装配置
```

## 安装依赖

```bash
pip install -r requirements.txt
```

## 支持的平台

- 水木社区 (newsmth)

## 许可证

GPL License
