import cv2
import numpy as np
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QSlider, QWidget, QGroupBox, QSizePolicy
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt

class Tab5EdgeDetection:
    def __init__(self, main_window):
        self.main_window = main_window  # 关联主窗口
        self.selected_edge_op = None    # 选中的边缘检测类型
        # 初始化各算法参数（默认值）
        self.sobel_ksize = 3            # Sobel：孔径大小（3-7奇数可调）
        self.canny_low_thresh = 50       # Canny：低阈值（10-200可调）
        self.canny_high_thresh = 150     # Canny：高阈值（50-300可调）
        self.laplacian_ksize = 3         # Laplacian：孔径大小（3-7奇数可调）
        # 固定显示尺寸（与Tab2/Tab3/Tab4统一）
        self.IMAGE_DISPLAY_SIZE = (600, 400)
        self.init_ui()                  # 构建Tab5界面

    def init_ui(self):
        """构建Tab5布局（固定尺寸+统一结构）"""
        self.layout = QVBoxLayout()
        # 第一行：原始图 + 操作按钮 + 检测结果图
        self.image_layout = QHBoxLayout()
        self.create_image_labels()
        self.create_edge_buttons()
        # 第二行：参数调节区（按算法分组显示）
        self.param_layout = QHBoxLayout()
        self.create_param_sliders()
        self.param_layout.setContentsMargins(0, 10, 0, 10)
        # 组装布局（添加整体边距）
        self.layout.addLayout(self.image_layout)
        self.layout.addLayout(self.param_layout)
        self.layout.setContentsMargins(20, 20, 20, 20)

    def create_image_labels(self):
        """创建原始图和结果图标签（固定尺寸）"""
        # 原始图
        self.original_image_label_t5 = QLabel()
        self.original_image_label_t5.setText("原始图片会显示在这里")
        self.original_image_label_t5.setAlignment(Qt.AlignCenter)
        self.original_image_label_t5.setFixedSize(self.IMAGE_DISPLAY_SIZE[0], self.IMAGE_DISPLAY_SIZE[1])
        self.original_image_label_t5.setMinimumSize(self.IMAGE_DISPLAY_SIZE[0], self.IMAGE_DISPLAY_SIZE[1])
        self.original_image_label_t5.setMaximumSize(self.IMAGE_DISPLAY_SIZE[0], self.IMAGE_DISPLAY_SIZE[1])
        self.original_image_label_t5.setStyleSheet("""
            border: 2px solid #B0B0B0; 
            padding: 5px; 
            background: rgba(255, 255, 255, 0.7);
            font-size: 14px;
            color: #333333;
        """)
        # 检测结果图
        self.edge_result_label = QLabel()
        self.edge_result_label.setText("边缘检测结果会显示在这里")
        self.edge_result_label.setAlignment(Qt.AlignCenter)
        self.edge_result_label.setFixedSize(self.IMAGE_DISPLAY_SIZE[0], self.IMAGE_DISPLAY_SIZE[1])
        self.edge_result_label.setMinimumSize(self.IMAGE_DISPLAY_SIZE[0], self.IMAGE_DISPLAY_SIZE[1])
        self.edge_result_label.setMaximumSize(self.IMAGE_DISPLAY_SIZE[0], self.IMAGE_DISPLAY_SIZE[1])
        self.edge_result_label.setStyleSheet(self.original_image_label_t5.styleSheet())
        # 添加到布局（留间距）
        self.image_layout.addWidget(self.original_image_label_t5)
        self.image_layout.addSpacing(30)

    def create_edge_buttons(self):
        """创建4个边缘检测按钮（统一宽度）"""
        self.edge_selector = QVBoxLayout()
        self.sobel_x_button = QPushButton("Sobel 水平边缘")
        self.sobel_y_button = QPushButton("Sobel 垂直边缘")
        self.canny_button = QPushButton("Canny 边缘检测")
        self.laplacian_button = QPushButton("Laplacian 边缘")
        # 设置按钮样式（统一最大宽度）
        self.main_window.set_button_style(self.sobel_x_button)
        self.main_window.set_button_style(self.sobel_y_button)
        self.main_window.set_button_style(self.canny_button)
        self.main_window.set_button_style(self.laplacian_button)
        for btn in [self.sobel_x_button, self.sobel_y_button, self.canny_button, self.laplacian_button]:
            btn.setMaximumWidth(180)
        # 绑定点击事件
        self.sobel_x_button.clicked.connect(lambda: self.update_button_style(self.sobel_x_button))
        self.sobel_y_button.clicked.connect(lambda: self.update_button_style(self.sobel_y_button))
        self.canny_button.clicked.connect(lambda: self.update_button_style(self.canny_button))
        self.laplacian_button.clicked.connect(lambda: self.update_button_style(self.laplacian_button))
        # 添加到布局（按钮间距均匀）
        self.edge_selector.addStretch()
        self.edge_selector.addWidget(self.sobel_x_button)
        self.edge_selector.addSpacing(15)
        self.edge_selector.addWidget(self.sobel_y_button)
        self.edge_selector.addSpacing(15)
        self.edge_selector.addWidget(self.canny_button)
        self.edge_selector.addSpacing(15)
        self.edge_selector.addWidget(self.laplacian_button)
        self.edge_selector.addStretch()
        self.image_layout.addLayout(self.edge_selector)
        self.image_layout.addSpacing(30)
        self.image_layout.addWidget(self.edge_result_label)

    def create_param_sliders(self):
        """创建参数滑块（按算法分组，固定宽度）"""
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
                text-align: center;
            }
            QGroupBox {
                border: 1px solid #B0B0B0;
                border-radius: 6px;
                padding: 10px;
                margin: 5px;
                font-size: 14px;
                color: #333333;
                background: rgba(255, 255, 255, 0.5);
            }
        """

        # 1. Sobel参数组（水平+垂直共用）
        self.sobel_param_group = QGroupBox("Sobel 参数")
        self.sobel_param_group.setFixedHeight(160)
        self.sobel_param_layout = QVBoxLayout(self.sobel_param_group)
        self.sobel_param_layout.addStretch()
        self.sobel_ksize_label = QLabel(f"孔径大小：{self.sobel_ksize}x{self.sobel_ksize}（奇数）")
        self.sobel_ksize_slider = QSlider(Qt.Horizontal)
        self.sobel_ksize_slider.setRange(3, 7)
        self.sobel_ksize_slider.setSingleStep(2)
        self.sobel_ksize_slider.setValue(self.sobel_ksize)
        self.sobel_ksize_slider.setStyleSheet(slider_style)
        self.sobel_ksize_slider.setFixedWidth(400)
        # self.sobel_ksize_slider.valueChanged.connect(self.update_sobel_param)
        self.sobel_ksize_slider.valueChanged.connect(self.update_sobel_param_with_fix)
        
        self.sobel_param_layout.addWidget(self.sobel_ksize_label)
        self.sobel_param_layout.addWidget(self.sobel_ksize_slider)
        
        self.sobel_param_group.setVisible(True)

        # 2. Canny参数组（低阈值+高阈值）
        self.canny_param_group = QGroupBox("Canny 参数")
        self.canny_param_group.setFixedHeight(160)
        self.canny_param_layout = QVBoxLayout(self.canny_param_group)
        self.canny_param_layout.addStretch()

        self.canny_low_label = QLabel(f"低阈值：{self.canny_low_thresh}")
        self.canny_low_slider = QSlider(Qt.Horizontal)
        self.canny_low_slider.setRange(10, 200)
        self.canny_low_slider.setValue(self.canny_low_thresh)
        self.canny_low_slider.setStyleSheet(slider_style)
        self.canny_low_slider.setFixedWidth(400)
        self.canny_low_slider.valueChanged.connect(self.update_canny_low_param)

        self.canny_high_label = QLabel(f"高阈值：{self.canny_high_thresh}")
        self.canny_high_slider = QSlider(Qt.Horizontal)
        self.canny_high_slider.setRange(50, 300)
        self.canny_high_slider.setValue(self.canny_high_thresh)
        self.canny_high_slider.setStyleSheet(slider_style)
        self.canny_high_slider.setFixedWidth(400)
        self.canny_high_slider.valueChanged.connect(self.update_canny_high_param)

        self.canny_param_layout.addWidget(self.canny_low_label)
        self.canny_param_layout.addWidget(self.canny_low_slider)
        self.canny_param_layout.addSpacing(10)
        self.canny_param_layout.addWidget(self.canny_high_label)
        self.canny_param_layout.addWidget(self.canny_high_slider)
        self.canny_param_group.setVisible(False)

        # 3. Laplacian参数组
        self.laplacian_param_group = QGroupBox("Laplacian 参数")
        self.laplacian_param_group.setFixedHeight(160)
        self.laplacian_param_layout = QVBoxLayout(self.laplacian_param_group)
        self.laplacian_param_layout.addStretch()
        self.laplacian_ksize_label = QLabel(f"孔径大小：{self.laplacian_ksize}x{self.laplacian_ksize}（奇数）")
        self.laplacian_ksize_slider = QSlider(Qt.Horizontal)
        self.laplacian_ksize_slider.setRange(3, 7)
        self.laplacian_ksize_slider.setSingleStep(2)
        self.laplacian_ksize_slider.setValue(self.laplacian_ksize)
        self.laplacian_ksize_slider.setStyleSheet(slider_style)
        self.laplacian_ksize_slider.setFixedWidth(400)
        self.laplacian_ksize_slider.valueChanged.connect(self.update_laplacian_param)
        self.laplacian_param_layout.addWidget(self.laplacian_ksize_label)
        self.laplacian_param_layout.addWidget(self.laplacian_ksize_slider)
        self.laplacian_param_group.setVisible(False)

        # 总参数布局（居中，分组间距均匀）
        self.param_layout.addStretch()
        self.param_layout.addWidget(self.sobel_param_group)
        # self.param_layout.addSpacing(40)
        self.param_layout.addWidget(self.canny_param_group)
        # self.param_layout.addSpacing(40)
        self.param_layout.addWidget(self.laplacian_param_group)
        self.param_layout.addStretch()

    def update_button_style(self, clicked_button):
        """更新按钮选中状态+显示对应参数组"""
        # 1. 恢复所有按钮默认样式
        for btn in [self.sobel_x_button, self.sobel_y_button, self.canny_button, self.laplacian_button]:
            self.main_window.set_button_style(btn)
        # 2. 隐藏所有参数组
        self.sobel_param_group.setVisible(False)
        self.canny_param_group.setVisible(False)
        self.laplacian_param_group.setVisible(False)
        # 3. 设置选中按钮样式
        clicked_button.setStyleSheet(f"""
            QPushButton {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                                           stop:0 #e67e22, stop:1 #f39c12);
                color: white;
                font-size: 14px;
                padding: 10px;
                max-width: 180px;
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
        # 4. 显示对应参数组+记录选中操作
        self.selected_edge_op = clicked_button.text()
        if "Sobel" in self.selected_edge_op:
            self.sobel_param_group.setVisible(True)
        elif self.selected_edge_op == "Canny 边缘检测":
            self.canny_param_group.setVisible(True)
        elif self.selected_edge_op == "Laplacian 边缘":
            self.laplacian_param_group.setVisible(True)
        # 5. 执行边缘检测（已含图片校验，无需额外修改）
        self.apply_edge_detection()

    # -------------------------- 参数更新方法（新增图片校验） --------------------------
    def update_sobel_param(self, value):
        """更新Sobel孔径大小（新增图片校验）"""
        # 保险措施：判断图片是否存在
        if not self.main_window.image:
            self.edge_result_label.setText("请先加载图片再调整参数！")
            return
        self.sobel_ksize = value
        self.sobel_ksize_label.setText(f"孔径大小：{self.sobel_ksize}x{self.sobel_ksize}（奇数）")
        if "Sobel" in self.selected_edge_op:
            self.apply_edge_detection()

    def update_canny_low_param(self, value):
        """更新Canny低阈值（新增图片校验）"""
        # 保险措施：判断图片是否存在
        if not self.main_window.image:
            self.edge_result_label.setText("请先加载图片再调整参数！")
            return
        self.canny_low_thresh = value
        self.canny_low_label.setText(f"低阈值：{self.canny_low_thresh}")
        if self.selected_edge_op == "Canny 边缘检测":
            self.apply_edge_detection()

    def update_canny_high_param(self, value):
        """更新Canny高阈值（新增图片校验）"""
        # 保险措施：判断图片是否存在
        if not self.main_window.image:
            self.edge_result_label.setText("请先加载图片再调整参数！")
            return
        self.canny_high_thresh = value
        self.canny_high_label.setText(f"高阈值：{self.canny_high_thresh}")
        if self.selected_edge_op == "Canny 边缘检测":
            self.apply_edge_detection()

    def update_laplacian_param(self, value):
        """更新Laplacian孔径大小（新增图片校验）"""
        # 保险措施：判断图片是否存在
        if not self.main_window.image:
            self.edge_result_label.setText("请先加载图片再调整参数！")
            return
        self.laplacian_ksize = value
        self.laplacian_ksize_label.setText(f"孔径大小：{self.laplacian_ksize}x{self.laplacian_ksize}（奇数）")
        if self.selected_edge_op == "Laplacian 边缘":
            self.apply_edge_detection()

    # -------------------------- 边缘检测核心逻辑（保留原有校验，优化提示） --------------------------
    def apply_edge_detection(self):
        """执行边缘检测（固定尺寸显示）"""
        # 保险措施：判断图片是否存在（核心校验，防止后续处理报错）
        if not self.main_window.image:
            self.edge_result_label.setText("请先加载图片再执行检测！")
            return

        try:
            # 图像格式转换（PIL→OpenCV灰度图）
            cv_image = cv2.cvtColor(np.array(self.main_window.image), cv2.COLOR_RGB2BGR)
            gray_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
            # 高斯模糊降噪（所有算法共用，提升检测效果）
            blur_image = cv2.GaussianBlur(gray_image, (3, 3), 0)

            # 按选中算法执行检测
            if self.selected_edge_op == "Sobel 水平边缘":
                edge = cv2.Sobel(blur_image, cv2.CV_64F, dx=1, dy=0, ksize=self.sobel_ksize)
            elif self.selected_edge_op == "Sobel 垂直边缘":
                edge = cv2.Sobel(blur_image, cv2.CV_64F, dx=0, dy=1, ksize=self.sobel_ksize)
            elif self.selected_edge_op == "Canny 边缘检测":
                edge = cv2.Canny(blur_image, self.canny_low_thresh, self.canny_high_thresh)
            elif self.selected_edge_op == "Laplacian 边缘":
                edge = cv2.Laplacian(blur_image, cv2.CV_64F, ksize=self.laplacian_ksize)

            # 处理Sobel/Laplacian的负值（转为uint8）
            if "Sobel" in self.selected_edge_op or "Laplacian" in self.selected_edge_op:
                edge = cv2.convertScaleAbs(edge)  # 取绝对值并转为8位

            # 格式转回QImage并固定尺寸显示
            from PIL import Image
            pil_result = Image.fromarray(edge)
            q_image = self.main_window.pil_to_qimage(pil_result)
            self.edge_result_label.setPixmap(
                QPixmap.fromImage(q_image).scaled(
                    self.IMAGE_DISPLAY_SIZE[0], self.IMAGE_DISPLAY_SIZE[1],
                    Qt.KeepAspectRatio, Qt.SmoothTransformation
                )
            )

        except Exception as e:
            self.edge_result_label.setText(f"检测出错：{str(e)}")

    def sync_original_image(self):
        """同步主窗口原始图到Tab5（固定尺寸）"""
        # 保险措施：判断图片是否存在
        if not self.main_window.image:
            self.original_image_label_t5.setText("请先加载图片！")
            return
        q_image = self.main_window.pil_to_qimage(self.main_window.image)
        self.original_image_label_t5.setPixmap(
            QPixmap.fromImage(q_image).scaled(
                self.IMAGE_DISPLAY_SIZE[0], self.IMAGE_DISPLAY_SIZE[1],
                Qt.KeepAspectRatio, Qt.SmoothTransformation
            )
        )

    def update_sobel_param_with_fix(self, value):
        """修正滑块值，确保只能取3、5、7（步长2的奇数）（新增图片校验）"""
        # 保险措施：判断图片是否存在
        if not self.main_window.image:
            self.edge_result_label.setText("请先加载图片再调整参数！")
            return
        # 1. 计算最近的符合步长的数值（以3为起点，步长2）
        # 公式：修正值 = 起点 + 步长 * 整数倍（确保在3-7范围内）
        base = 3  # 起始值
        step = 2  # 步长
        # 计算与当前值最接近的目标值
        offset = (value - base) // step
        fixed_value = base + offset * step
        # 2. 确保修正值不超出滑块范围（3-7）
        fixed_value = max(base, min(fixed_value, 7))
        # 3. 更新滑块值（避免死循环，先断开信号再设置）
        self.sobel_ksize_slider.valueChanged.disconnect(self.update_sobel_param_with_fix)
        self.sobel_ksize_slider.setValue(fixed_value)
        self.sobel_ksize_slider.valueChanged.connect(self.update_sobel_param_with_fix)
        # 4. 执行原有的参数更新和边缘检测
        self.sobel_ksize = fixed_value
        self.sobel_ksize_label.setText(f"孔径大小：{self.sobel_ksize}x{self.sobel_ksize}（奇数）")
        if "Sobel" in self.selected_edge_op:
            self.apply_edge_detection()

    def get_layout(self):
        """返回Tab5布局（供主窗口调用）"""
        return self.layout