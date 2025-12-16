# qt_for_img

A desktop application for image processing with PyQt5

## 简介

qt_for_img 是一款基于 PyQt5 开发的桌面图像处理工具，集成了多种常用的图像处理功能，包括基础图像处理、空间域滤波、频域滤波、形态学处理和边缘检测等。该应用界面简洁直观，操作便捷，适合用于图像处理学习和日常使用。

## 功能特点

- **基础图像处理**：支持图像加载、灰度化转换、频域频谱显示
- **空间域滤波**：提供均值滤波、高斯滤波、锐化滤波等常用滤波功能
- **频域滤波**：支持频域内的各种滤波操作
- **形态学处理**：包含腐蚀、膨胀、开运算、闭运算等形态学操作，支持核大小调节
- **边缘检测**：实现多种边缘检测算法
- **图片导出**：支持单个页面或全部页面处理结果导出

## 技术栈

- 界面框架：PyQt5
- 图像处理：OpenCV、PIL (Pillow)
- 数据处理：NumPy
- 可视化：Matplotlib

## 安装与使用

### 前提条件
- Python 3.6+
- 所需依赖库：PyQt5、opencv-python、pillow、numpy、matplotlib

### 安装步骤
1. 克隆仓库
```bash
git clone https://github.com/johnsad-max/qt_for_img.git
cd qt_for_img
安装依赖
bash
运行
pip install PyQt5 opencv-python pillow numpy matplotlib
运行应用
bash
运行
python main.py
使用说明
加载图片：在 "图像处理" 标签页中点击 "加载图片" 按钮，选择本地图片文件
基础处理：可在 "图像处理" 标签页进行灰度化转换和频域频谱显示
空间域滤波：切换到 "空间域滤波" 标签页，选择所需滤波方式
频域滤波：在 "频域滤波" 标签页进行频域相关滤波操作
形态学处理：在 "形态学处理" 标签页选择相应操作，可通过滑块调节核大小
边缘检测：切换到 "边缘检测" 标签页，选择合适的检测算法
导出图片：点击窗口顶部的 "导出图片" 按钮，可选择导出当前页面结果或全部页面结果
界面预览
提示：请将应用界面截图保存到仓库的 screenshots/ 目录下，并替换以下示例路径

image

image

image
许可证
本项目采用 MIT 许可证，详情参见 LICENSE 文件。
作者信息
作者：周勇 (202321020629)
邮箱：johnsad@foxmail.com
日期：2025 年 12 月
免责声明
本软件仅用于学习交流，请勿用于商业用途。如有问题，欢迎提交 Issue 或邮件反馈。
