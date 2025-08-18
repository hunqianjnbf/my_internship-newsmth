#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
import os

# 读取README文件
def read_readme():
    with open('README.md', 'r', encoding='utf-8') as f:
        return f.read()

# 读取requirements文件
def read_requirements():
    with open('requirements.txt', 'r', encoding='utf-8') as f:
        return [line.strip() for line in f if line.strip() and not line.startswith('#')]

setup(
    name="web-scraping-toolkit",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="一个基于PyQt5的网络爬虫和自动登录工具集合",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/web-scraping-toolkit",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Internet :: WWW/HTTP :: Browsers",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.7",
    install_requires=read_requirements(),
    extras_require={
        "dev": [
            "pytest>=6.0.0",
            "black>=21.0.0",
            "flake8>=3.8.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "webscraper=main:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.json", "*.png", "*.jpg", "*.ico"],
    },
)

