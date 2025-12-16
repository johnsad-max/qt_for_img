qt_for_img

基于 PyQt5 + OpenCV + Pillow + NumPy + Matplotlib 构建的图像处理桌面应用程序。
提供空间域滤波、频域滤波、边缘检测、形态学处理等常见图像处理功能，适用于图像处理学习、演示和实验。

✨ 功能特点

图像加载与灰度化

频域显示与频域滤波

空间域滤波（均值、高斯、锐化等）

图像形态学操作（腐蚀、膨胀、开/闭运算）

常用边缘检测算法

处理后图像支持导出

多标签界面，结构清晰

基于 MIT License 可自由使用与扩展

🛠 技术栈
技术	用途
Python	主程序语言
PyQt5	图形用户界面
OpenCV	图像处理算法
Pillow	图片读写
NumPy	数值计算
Matplotlib	频谱显示等绘图
📦 安装方法
1. 克隆仓库
git clone https://github.com/johnsad-max/qt_for_img.git
cd qt_for_img

2. 安装依赖

建议使用虚拟环境：

python -m venv venv
source venv/bin/activate       # macOS / Linux
venv\Scripts\activate          # Windows


如果仓库有 requirements.txt：

pip install -r requirements.txt


如果没有，可手动安装：

pip install PyQt5 opencv-python pillow numpy matplotlib

▶️ 运行方式
python main.py

📘 使用说明
1. 加载图片

在“图像处理”页面点击 加载图片 选择本地文件。

2. 可用处理功能
标签页	功能说明
图像处理	加载图像、灰度化、频域显示
空间域滤波	模糊、锐化、降噪等滤波机制
频域滤波	高频 / 低频等频域操作
形态学处理	腐蚀、膨胀、开/闭运算
边缘检测	多种边缘检测算法
3. 导出图像

顶部工具栏可导出当前处理后的图像或批量导出全部结果。

🖼 示例截图（可选）

如果你加入截图，可以按以下结构放：

screenshots/
├─ main_window.png
├─ spatial_filter.png
├─ frequency_filter.png


Markdown 示例：

![Main Window](screenshots/main_window.png)

📄 License

本项目使用 MIT License。
你可以自由用于学习、研究或扩展。

👨‍💻 作者

周勇
邮箱：johnsad@foxmail.com

创建日期：2025-12

欢迎提交 Issue 或 PR 来完善本项目。
