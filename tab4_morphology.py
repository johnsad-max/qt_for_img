import cv2
import numpy as np
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QSlider, QWidget
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt

class Tab4Morphology:
    def __init__(self, main_window):
        self.main_window = main_window  # 关联主窗口
        self.selected_morph_op = None   # 选中的形态学操作类型
        self.kernel_size = 5            # 形态学核大小（默认5x5，3-21奇数可调）
        self.init_ui()                  # 构建Tab4界面

    def init_ui(self):
        """构建Tab4布局（原始图+按钮+结果图+核大小滑块）"""
        self.layout = QVBoxLayout()
        # 第一行：原始图 + 操作按钮 + 处理结果图
        self.image_layout = QHBoxLayout()
        self.create_image_labels()
        self.create_morph_buttons()
        # 第二行：核大小调节滑块（所有操作共用一个核大小）
        self.param_layout = QHBoxLayout()
        self.create_kernel_slider()
        # 组装布局
        self.layout.addLayout(self.image_layout)
        self.layout.addLayout(self.param_layout)

    def create_image_labels(self):
        """创建原始图和处理结果图标签"""
        # 原始图
        self.original_image_label_t4 = QLabel()
        self.original_image_label_t4.setText("原始图片会显示在这里")
        self.original_image_label_t4.setAlignment(Qt.AlignCenter)
        self.original_image_label_t4.setStyleSheet("""
            border: 2px solid #B0B0B0; 
            padding: 5px; 
            background: rgba(255, 255, 255, 0.7);
        """)
        # 处理结果图
        self.morph_result_label = QLabel()
        self.morph_result_label.setText("形态学处理结果会显示在这里")
        self.morph_result_label.setAlignment(Qt.AlignCenter)
        self.morph_result_label.setStyleSheet(self.original_image_label_t4.styleSheet())
        # 添加到布局
        self.image_layout.addWidget(self.original_image_label_t4)

    def create_morph_buttons(self):
        """创建4个形态学操作按钮"""
        self.morph_selector = QVBoxLayout()
        self.erode_button = QPushButton("腐蚀")
        self.dilate_button = QPushButton("膨胀")
        self.open_button = QPushButton("开运算（先腐蚀后膨胀）")
        self.close_button = QPushButton("闭运算（先膨胀后腐蚀）")
        # 设置按钮样式（复用全局样式，长按钮调整最大宽度）
        self.main_window.set_button_style(self.erode_button)
        self.main_window.set_button_style(self.dilate_button)
        self.main_window.set_button_style(self.open_button)
        self.main_window.set_button_style(self.close_button)
        self.open_button.setStyleSheet(self.open_button.styleSheet() + "max-width: 180px;")
        self.close_button.setStyleSheet(self.close_button.styleSheet() + "max-width: 180px;")
        # 绑定点击事件
        self.erode_button.clicked.connect(lambda: self.update_button_style(self.erode_button))
        self.dilate_button.clicked.connect(lambda: self.update_button_style(self.dilate_button))
        self.open_button.clicked.connect(lambda: self.update_button_style(self.open_button))
        self.close_button.clicked.connect(lambda: self.update_button_style(self.close_button))
        # 添加到布局（居中）
        self.morph_selector.addStretch()
        self.morph_selector.addWidget(self.erode_button)
        self.morph_selector.addWidget(self.dilate_button)
        self.morph_selector.addWidget(self.open_button)
        self.morph_selector.addWidget(self.close_button)
        self.morph_selector.addStretch()
        self.image_layout.addLayout(self.morph_selector)
        self.image_layout.addWidget(self.morph_result_label)

    def create_kernel_slider(self):
        """创建核大小调节滑块（3-21奇数，保证形态学操作对称性）"""
        slider_style = """
            QSlider::groove:horizontal {
                border: 1px solid #B0B0B0;
                background: white;
                height: 8px;
                border-radius: 4px;
            }
            QSlider::handle:horizontal {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                                           stop:0 #e67e22, stop:1 #f39c12);
                border: none;
                width: 20px;
                margin: -6px 0;
                border-radius: 10px;
            }
            QLabel {
                font-size: 13px;
                color: #222222;
                margin-bottom: 5px;
            }
        """
        # 核大小参数容器
        self.kernel_param_widget = QWidget()
        self.kernel_param_layout = QVBoxLayout(self.kernel_param_widget)
        self.kernel_label = QLabel(f"形态学核大小：{self.kernel_size}x{self.kernel_size}（奇数）")
        self.kernel_slider = QSlider(Qt.Horizontal)
        self.kernel_slider.setRange(3, 21)  # 核大小范围：3-21
        self.kernel_slider.setSingleStep(2)  # 步长2，保证奇数
        self.kernel_slider.setValue(self.kernel_size)
        self.kernel_slider.setStyleSheet(slider_style)
        self.kernel_slider.valueChanged.connect(self.update_kernel_size)
        # 添加到布局
        self.kernel_param_layout.addWidget(self.kernel_label)
        self.kernel_param_layout.addWidget(self.kernel_slider)
        self.kernel_param_widget.setVisible(True)  # 未选操作时隐藏
        # 总参数布局（居中）
        self.param_layout.addStretch()
        self.param_layout.addWidget(self.kernel_param_widget)
        self.param_layout.addStretch()

    def update_button_style(self, clicked_button):
        """更新按钮选中状态（橙色渐变）+ 显示滑块"""
        # 1. 恢复所有按钮默认样式
        self.main_window.set_button_style(self.erode_button)
        self.main_window.set_button_style(self.dilate_button)
        self.main_window.set_button_style(self.open_button)
        self.main_window.set_button_style(self.close_button)
        # 2. 显示核大小滑块
        self.kernel_param_widget.setVisible(True)
        # 3. 设置选中按钮样式（适配长按钮）
        max_width = "200px"
        clicked_button.setStyleSheet(f"""
            QPushButton {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                                           stop:0 #e67e22, stop:1 #f39c12);
                color: white;
                font-size: 14px;
                padding: 10px;
                max-width: {max_width};
                border: none;
                border-radius: 6px;
                outline: none;
                font-weight: 500;
            }}
            QPushButton:pressed {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                                           stop:0 #d35400, stop:1 #e67e22);
            }}
        """)
        # 4. 记录选中操作并执行
        self.selected_morph_op = clicked_button.text()
        self.apply_morph_operation()

    def update_kernel_size(self, value):
        """更新核大小（强制奇数）并实时刷新效果"""
        self.kernel_size = value
        self.kernel_label.setText(f"形态学核大小：{self.kernel_size}x{self.kernel_size}（奇数）")
        if self.selected_morph_op:  # 选中操作后才刷新
            self.apply_morph_operation()

    def apply_morph_operation(self):
        """执行形态学操作（基于OpenCV）"""
        if not self.main_window.image:
            self.morph_result_label.setText("请先加载图片！")
            return

        try:
            # 1. 图像格式转换（PIL→OpenCV）
            cv_image = cv2.cvtColor(np.array(self.main_window.image), cv2.COLOR_RGB2BGR)
            gray_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)  # 形态学操作基于灰度图

            # 2. 创建形态学核（正方形结构元素）
            kernel = np.ones((self.kernel_size, self.kernel_size), np.uint8)

            # 3. 根据选中操作执行形态学处理
            if self.selected_morph_op == "腐蚀":
                result = cv2.erode(gray_image, kernel, iterations=1)
            elif self.selected_morph_op == "膨胀":
                result = cv2.dilate(gray_image, kernel, iterations=1)
            elif self.selected_morph_op == "开运算（先腐蚀后膨胀）":
                result = cv2.morphologyEx(gray_image, cv2.MORPH_OPEN, kernel)
            elif self.selected_morph_op == "闭运算（先膨胀后腐蚀）":
                result = cv2.morphologyEx(gray_image, cv2.MORPH_CLOSE, kernel)

            # 4. 格式转回QImage并显示
            from PIL import Image
            pil_result = Image.fromarray(result)
            q_image = self.main_window.pil_to_qimage(pil_result)
            self.morph_result_label.setPixmap(
                QPixmap.fromImage(q_image).scaled(800, 600, Qt.KeepAspectRatio)
            )

        except Exception as e:
            self.morph_result_label.setText(f"处理出错：{str(e)}")

    def sync_original_image(self):
        """同步主窗口的原始图到Tab4"""
        if self.main_window.image:
            q_image = self.main_window.pil_to_qimage(self.main_window.image)
            self.original_image_label_t4.setPixmap(
                QPixmap.fromImage(q_image).scaled(800, 600, Qt.KeepAspectRatio)
            )

    def get_layout(self):
        """返回Tab4布局（供主窗口调用）"""
        return self.layout