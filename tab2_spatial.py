from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QLabel, QPushButton
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from PIL import ImageFilter

class Tab2SpatialFilter:
    def __init__(self, main_window):
        self.main_window = main_window  # 关联主窗口
        self.init_ui()                  # 构建Tab2界面

    def init_ui(self):
        """构建Tab2布局"""
        self.layout = QVBoxLayout()
        # 图像显示+按钮布局
        self.image_layout = QHBoxLayout()
        # 原始图显示标签
        self.original_image_label_t2 = QLabel()
        self.original_image_label_t2.setText("原始图片会显示在这里")
        self.original_image_label_t2.setAlignment(Qt.AlignCenter)
        self.original_image_label_t2.setStyleSheet("border: 2px solid #B0B0B0; padding: 5px;")
        # 滤波按钮布局
        self.filter_selector = QVBoxLayout()
        self.create_filter_buttons()
        # 滤波结果显示标签
        self.filtered_image_label = QLabel()
        self.filtered_image_label.setText("滤波后的图像会显示在这里")
        self.filtered_image_label.setAlignment(Qt.AlignCenter)
        self.filtered_image_label.setStyleSheet("border: 2px solid #B0B0B0; padding: 5px;")
        # 组装布局
        self.image_layout.addWidget(self.original_image_label_t2)
        self.image_layout.addLayout(self.filter_selector)
        self.image_layout.addWidget(self.filtered_image_label)
        self.layout.addLayout(self.image_layout)

    def create_filter_buttons(self):
        """创建3个空间域滤波按钮"""
        self.mean_filter_button = QPushButton("均值滤波")
        self.gaussian_filter_button = QPushButton("高斯滤波")
        self.sharpen_filter_button = QPushButton("锐化滤波")
        # 设置按钮样式
        self.main_window.set_button_style(self.mean_filter_button)
        self.main_window.set_button_style(self.gaussian_filter_button)
        self.main_window.set_button_style(self.sharpen_filter_button)
        # 绑定点击事件
        self.mean_filter_button.clicked.connect(
            lambda: self.update_button_style(self.mean_filter_button)
        )
        self.gaussian_filter_button.clicked.connect(
            lambda: self.update_button_style(self.gaussian_filter_button)
        )
        self.sharpen_filter_button.clicked.connect(
            lambda: self.update_button_style(self.sharpen_filter_button)
        )
        # 添加到布局
        self.filter_selector.addWidget(self.mean_filter_button)
        self.filter_selector.addWidget(self.gaussian_filter_button)
        self.filter_selector.addWidget(self.sharpen_filter_button)

    def update_button_style(self, clicked_button):
        """更新按钮选中状态（橙色渐变）"""
        # 恢复所有按钮默认样式
        self.main_window.set_button_style(self.mean_filter_button)
        self.main_window.set_button_style(self.gaussian_filter_button)
        self.main_window.set_button_style(self.sharpen_filter_button)
        # 设置选中样式
        clicked_button.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                                           stop:0 #e67e22, stop:1 #f39c12);
                color: white;
                font-size: 14px;
                padding: 10px;
                max-width: 200px;
                border: none;
                border-radius: 6px;
                outline: none;
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                                           stop:0 #d35400, stop:1 #e67e22);
            }
        """)
        # 执行滤波
        self.apply_filter(clicked_button.text())

    def apply_filter(self, filter_type):
        """执行空间域滤波"""
        try:
            if not self.main_window.image:
                self.filtered_image_label.setText("请先加载图片！")
                return
            # 根据类型应用滤波
            if filter_type == "均值滤波":
                filtered_image = self.main_window.image.filter(ImageFilter.BoxBlur(5))
            elif filter_type == "高斯滤波":
                filtered_image = self.main_window.image.filter(ImageFilter.GaussianBlur(radius=2))
            elif filter_type == "锐化滤波":
                filtered_image = self.main_window.image.filter(ImageFilter.SHARPEN)
            # 显示结果
            q_image = self.main_window.pil_to_qimage(filtered_image)
            pixmap = QPixmap.fromImage(q_image)
            self.filtered_image_label.setPixmap(pixmap.scaled(800, 600, Qt.KeepAspectRatio))
        except Exception as e:
            self.filtered_image_label.setText(f"滤波出错：{str(e)}")

    def sync_original_image(self):
        """同步主窗口的原始图到Tab2"""
        if self.main_window.image:
            q_image = self.main_window.pil_to_qimage(self.main_window.image)
            pixmap = QPixmap.fromImage(q_image)
            self.original_image_label_t2.setPixmap(pixmap.scaled(800, 600, Qt.KeepAspectRatio))

    def get_layout(self):
        """返回Tab2布局（供主窗口调用）"""
        return self.layout