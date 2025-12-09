from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QTextBrowser
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QDesktopServices

class Tab7About(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        """构建关于页面布局"""
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(40, 30, 40, 30)
        self.layout.setSpacing(25)
        
        # 1. 标题区
        title_label = QLabel("关于 图像处理工具")
        title_label.setStyleSheet("""
            font-size: 20px;
            font-weight: bold;
            color: #222222;
        """)
        title_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(title_label)
        
        # 2. 核心信息区（使用QTextBrowser支持换行和链接）
        info_browser = QTextBrowser()
        info_browser.setStyleSheet("""
            font-size: 20px;
            color: #333333;
            background: transparent;
            border: none;
            line-height: 1.8;
        """)
        # 设置不可编辑，仅展示
        info_browser.setReadOnly(True)
        
        # 告诉控件：外部链接直接用系统浏览器打开，不要自己加载
        info_browser.setOpenExternalLinks(True)
        
        # 内容（支持HTML格式，可添加链接）
        info_content = """
        <p><strong>📌 软件简介</strong><br>
        一款集成多种图像处理功能的桌面应用，支持空间域滤波、频域滤波、形态学处理、边缘检测等核心功能。</p>
        
        <p><strong>👨‍💻 作者信息</strong><br>
        作者：周勇(202321020629)<br>
        邮箱：johnsad@foxmail.com<br>
        日期：2025年12月</p>
        
        <p><strong>🔧 核心功能</strong><br>
        • 基础图像处理：灰度化、频谱图生成<br>
        • 滤波处理：空间域滤波、频域滤波<br>
        • 形态学处理：腐蚀、膨胀、开运算、闭运算<br>
        • 边缘检测：Sobel、Canny等算法<br>
        • 图片导出：支持单个/全部页面处理结果导出</p>
        
        <p><strong>🖥️ 技术栈</strong><br>
        • 界面框架：PyQt5<br>
        • 图像处理：OpenCV、PIL<br>
        • 数据处理：NumPy</p>
        
        <p><strong>🌐 开源地址</strong><br>
        <a href="https://github.com/johnsad-max/qt_for_img.git">https://github.com/johnsad-max/qt_for_img.git</a>
        </p>
        
        <p><strong>📄 免责声明</strong><br>
        本软件仅用于学习交流，请勿用于商业用途。如有问题，欢迎反馈交流。</p>
        """
        info_browser.setHtml(info_content)
        self.layout.addWidget(info_browser)
        
        # 3. 底部按钮区
        btn_layout = QHBoxLayout()
        repo_btn = QPushButton("访问开源仓库")
        repo_btn.setStyleSheet("""
            QPushButton {
                background: #4299e1;
                color: white;
                font-size: 14px;
                padding: 8px 20px;
                border: none;
                border-radius: 6px;
            }
            QPushButton:hover {
                background: #3182ce;
            }
        """)
        # 绑定按钮事件（打开开源地址）
        repo_btn.clicked.connect(lambda: QDesktopServices.openUrl(QUrl("https://github.com/johnsad-max/qt_for_img.git")))
        btn_layout.addWidget(repo_btn, alignment=Qt.AlignCenter)
        self.layout.addLayout(btn_layout)

    def get_layout(self):
        """返回布局（供主窗口调用）"""
        return self.layout