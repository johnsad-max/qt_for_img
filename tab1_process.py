import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFileDialog
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

class Tab1Processor:
    def __init__(self, main_window):
        self.main_window = main_window  # 关联主窗口
        self.init_ui()                  # 构建Tab1界面

    def init_ui(self):
        """构建Tab1布局"""
        self.layout = QVBoxLayout()
        # 图像显示布局（原始图+灰度图+频谱图）
        self.img_layout = QHBoxLayout()
        self.create_image_labels()
        # 按钮布局
        self.button_layout = QHBoxLayout()
        self.create_buttons()
        # 组装布局
        self.layout.addLayout(self.img_layout)
        self.layout.addLayout(self.button_layout)

    def create_image_labels(self):
        """创建3个图像显示标签"""
        # 原始图
        self.original_image_label = QLabel()
        self.original_image_label.setText("原始图片会显示在这里")
        self.original_image_label.setAlignment(Qt.AlignCenter)
        self.original_image_label.setStyleSheet("""
            border: 2px solid #B0B0B0; 
            padding: 5px; 
            
        """)
        # 灰度图
        self.gray_image_label = QLabel()
        self.gray_image_label.setText("灰度图会显示在这里")
        self.gray_image_label.setAlignment(Qt.AlignCenter)
        self.gray_image_label.setStyleSheet(self.original_image_label.styleSheet())
        # 频谱图
        self.frequency_image_label = QLabel()
        self.frequency_image_label.setText("频谱图会显示在这里")
        self.frequency_image_label.setAlignment(Qt.AlignCenter)
        self.frequency_image_label.setStyleSheet(self.original_image_label.styleSheet())
        # 添加到布局
        self.img_layout.addWidget(self.original_image_label)
        self.img_layout.addWidget(self.gray_image_label)
        self.img_layout.addWidget(self.frequency_image_label)

    def create_buttons(self):
        """创建功能按钮（复用全局样式）"""
        # 加载图片按钮
        self.load_button = QPushButton("加载图片")
        self.main_window.set_button_style(self.load_button)
        self.load_button.clicked.connect(self.load_image)
        # 转换灰度图按钮
        self.convert_button = QPushButton("转换为灰度图")
        self.main_window.set_button_style(self.convert_button)
        self.convert_button.clicked.connect(self.convert_to_grayscale)
        # 显示频谱按钮
        self.frequency_button = QPushButton("显示频域波形")
        self.main_window.set_button_style(self.frequency_button)
        self.frequency_button.clicked.connect(self.show_frequency_domain)
        # 添加到布局（居中显示）
        self.button_layout.addStretch()
        self.button_layout.addWidget(self.load_button)
        self.button_layout.addWidget(self.convert_button)
        self.button_layout.addWidget(self.frequency_button)
        self.button_layout.addStretch()

    def load_image(self):
        """加载图片并自动转为PNG（同步更新所有Tab）"""
        file_name, _ = QFileDialog.getOpenFileName(
            self.main_window, "选择图片", "", 
            "图片文件 (*.png *.jpg *.jpeg *.bmp *.gif *.tiff)"
        )
        if file_name:
            # 转为PNG并保存到临时路径
            original_image = Image.open(file_name)
            original_image.save(self.main_window.temp_png_path, format="PNG")
            # 更新全局属性
            self.main_window.image_path = self.main_window.temp_png_path
            self.main_window.image = Image.open(self.main_window.temp_png_path)
            # 显示原始图（Tab1）
            pixmap = QPixmap(self.main_window.temp_png_path)
            self.original_image_label.setPixmap(pixmap.scaled(800, 600, Qt.KeepAspectRatio))
            # 同步更新Tab2、Tab3的原始图
            self.main_window.tab2_filter.sync_original_image()
            self.main_window.tab3_filter.sync_original_image()
            self.main_window.tab4_filter.sync_original_image()  
            self.main_window.tab5_filter.sync_original_image()  

    def convert_to_grayscale(self):
        """转换为灰度图并显示"""
        try:
            if not self.main_window.image:
                self.gray_image_label.setText("请先加载图片！")
                return
            # 转换灰度图
            gray_image = self.main_window.image.convert("L")
            gray_image.save("gray_image.png", format="PNG")
            # 显示
            gray_pixmap = QPixmap("gray_image.png")
            self.gray_image_label.setPixmap(gray_pixmap.scaled(800, 600, Qt.KeepAspectRatio))
        except Exception as e:
            self.gray_image_label.setText(f"转换失败：{str(e)}")

    def show_frequency_domain(self):
        """显示频域频谱（matplotlib生成）"""
        try:
            if not self.main_window.image:
                self.frequency_image_label.setText("请先加载图片！")
                return
            # 转为灰度图计算频谱
            image = self.main_window.image.convert("L")
            image_array = np.array(image)
            # 傅里叶变换
            f_transform = np.fft.fft2(image_array)
            f_transform_shifted = np.fft.fftshift(f_transform)
            magnitude_spectrum = np.abs(f_transform_shifted)
            # 生成频谱图
            plt.figure(figsize=(6, 6))
            plt.imshow(np.log(magnitude_spectrum + 1), cmap='gray')
            plt.axis('off')
            plt.savefig("frequency_image.png", bbox_inches='tight', pad_inches=0)
            plt.close()
            # 显示
            freq_pixmap = QPixmap("frequency_image.png")
            self.frequency_image_label.setPixmap(freq_pixmap.scaled(800, 600, Qt.KeepAspectRatio))
        except Exception as e:
            self.frequency_image_label.setText(f"频谱显示失败：{str(e)}")

    def get_layout(self):
        """返回Tab1布局（供主窗口调用）"""
        return self.layout