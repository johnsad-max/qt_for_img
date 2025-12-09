import numpy as np
import cv2
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QSlider, QWidget
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt

class Tab3FrequencyFilter:
    def __init__(self, main_window):
        self.main_window = main_window  # 关联主窗口
        self.selected_freq_filter = None  # 选中的频域滤波类型
        # 初始化各滤波参数（默认值）
        self.lpf_cutoff = 30        # 高斯低通：截止频率（10-100可调）
        self.hpf_cutoff = 30        # 高斯高通：截止频率（10-100可调）
        self.br_center_freq = 50     # 带阻滤波：中心频率（20-80可调）
        self.br_bandwidth = 10      # 带阻滤波：带宽（5-30可调）
        # 固定图像显示尺寸（所有Tab统一，避免切换缩放）
        self.IMAGE_DISPLAY_SIZE = (600, 400)  # 原始图/结果图尺寸（宽x高）
        self.SPECTRUM_DISPLAY_SIZE = (500, 350)  # 频谱图尺寸（宽x高）
        self.init_ui()              # 构建Tab3界面

    def init_ui(self):
        """构建Tab3布局（固定尺寸+统一结构）"""
        self.layout = QVBoxLayout()
        # 第一行：原始图 + 按钮 + 滤波结果图（固定尺寸，居中对齐）
        self.image_layout = QHBoxLayout()
        self.create_image_labels()
        self.create_freq_filter_buttons()
        # 第二行：参数调节区（固定高度，居中显示）
        self.param_layout = QHBoxLayout()
        self.create_param_sliders()
        self.param_layout.setContentsMargins(0, 10, 0, 10)  # 上下留空，避免拥挤
        # 第三行：原始频谱 + 滤波后频谱（固定尺寸）
        self.spectrum_layout = QHBoxLayout()
        self.create_spectrum_labels()
        # 组装布局（添加整体边距，避免贴边）
        self.layout.addLayout(self.image_layout)
        self.layout.addLayout(self.param_layout)
        self.layout.addLayout(self.spectrum_layout)
        self.layout.setContentsMargins(20, 20, 20, 20)

    def create_image_labels(self):
        """创建原始图和滤波结果图标签（固定尺寸，背景半透白）"""
        # 原始图
        self.original_image_label_t3 = QLabel()
        self.original_image_label_t3.setText("原始图片会显示在这里")
        self.original_image_label_t3.setAlignment(Qt.AlignCenter)
        # 固定标签尺寸，设置最小/最大尺寸避免缩放
        self.original_image_label_t3.setFixedSize(self.IMAGE_DISPLAY_SIZE[0], self.IMAGE_DISPLAY_SIZE[1])
        self.original_image_label_t3.setMinimumSize(self.IMAGE_DISPLAY_SIZE[0], self.IMAGE_DISPLAY_SIZE[1])
        self.original_image_label_t3.setMaximumSize(self.IMAGE_DISPLAY_SIZE[0], self.IMAGE_DISPLAY_SIZE[1])
        self.original_image_label_t3.setStyleSheet("""
            border: 2px solid #B0B0B0; 
            padding: 5px; 
            
            font-size: 14px;
            color: #333333;
        """)
        # 滤波结果图（与原始图尺寸完全一致）
        self.freq_filtered_image_label = QLabel()
        self.freq_filtered_image_label.setText("滤波后的图像会显示在这里")
        self.freq_filtered_image_label.setAlignment(Qt.AlignCenter)
        self.freq_filtered_image_label.setFixedSize(self.IMAGE_DISPLAY_SIZE[0], self.IMAGE_DISPLAY_SIZE[1])
        self.freq_filtered_image_label.setMinimumSize(self.IMAGE_DISPLAY_SIZE[0], self.IMAGE_DISPLAY_SIZE[1])
        self.freq_filtered_image_label.setMaximumSize(self.IMAGE_DISPLAY_SIZE[0], self.IMAGE_DISPLAY_SIZE[1])
        self.freq_filtered_image_label.setStyleSheet(self.original_image_label_t3.styleSheet())
        # 添加到布局（标签之间留间距）
        self.image_layout.addWidget(self.original_image_label_t3)
        self.image_layout.addSpacing(30)  # 原始图与按钮区间距

    def create_freq_filter_buttons(self):
        """创建3个频域滤波按钮（固定按钮宽度，避免布局偏移）"""
        self.freq_filter_selector = QVBoxLayout()
        self.gaussian_lpf_button = QPushButton("高斯低通滤波")
        self.gaussian_hpf_button = QPushButton("高斯高通滤波")
        self.band_reject_button = QPushButton("带阻滤波（去周期噪声）")
        # 设置按钮样式（统一固定宽度，与Tab2/Tab4一致）
        self.main_window.set_button_style(self.gaussian_lpf_button)
        self.main_window.set_button_style(self.gaussian_hpf_button)
        self.main_window.set_button_style(self.band_reject_button)
        # 统一按钮最大宽度，避免长文本导致布局拉伸
        self.gaussian_lpf_button.setMaximumWidth(180)
        self.gaussian_hpf_button.setMaximumWidth(180)
        self.band_reject_button.setMaximumWidth(180)
        # 绑定点击事件
        self.gaussian_lpf_button.clicked.connect(
            lambda: self.update_freq_button_style(self.gaussian_lpf_button)
        )
        self.gaussian_hpf_button.clicked.connect(
            lambda: self.update_freq_button_style(self.gaussian_hpf_button)
        )
        self.band_reject_button.clicked.connect(
            lambda: self.update_freq_button_style(self.band_reject_button)
        )
        # 添加到布局（按钮之间留间距，居中显示）
        self.freq_filter_selector.addStretch()
        self.freq_filter_selector.addWidget(self.gaussian_lpf_button)
        self.freq_filter_selector.addSpacing(15)
        self.freq_filter_selector.addWidget(self.gaussian_hpf_button)
        self.freq_filter_selector.addSpacing(15)
        self.freq_filter_selector.addWidget(self.band_reject_button)
        self.freq_filter_selector.addStretch()
        self.image_layout.addLayout(self.freq_filter_selector)
        self.image_layout.addSpacing(30)  # 按钮区与结果图间距
        self.image_layout.addWidget(self.freq_filtered_image_label)

    def create_param_sliders(self):
        """创建参数调节滑块（固定滑块宽度，避免布局晃动）"""
        # 滑块通用样式（固定滑块长度）
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
        """

        # 1. 高斯低通滤波参数（截止频率）
        self.lpf_param_widget = QWidget()
        self.lpf_param_layout = QHBoxLayout(self.lpf_param_widget)
        self.lpf_label = QLabel(f"高斯低通 - 截止频率：{self.lpf_cutoff}")
        self.lpf_slider = QSlider(Qt.Horizontal)
        self.lpf_slider.setRange(10, 100)
        self.lpf_slider.setValue(self.lpf_cutoff)
        self.lpf_slider.setStyleSheet(slider_style)
        self.lpf_slider.setFixedWidth(300)  # 固定滑块宽度
        self.lpf_slider.valueChanged.connect(self.update_lpf_param)
        self.lpf_param_layout.addWidget(self.lpf_label)
        self.lpf_param_layout.addWidget(self.lpf_slider)
        self.lpf_param_widget.setVisible(True)

        # 2. 高斯高通滤波参数（截止频率）
        self.hpf_param_widget = QWidget()
        self.hpf_param_layout = QHBoxLayout(self.hpf_param_widget)
        self.hpf_label = QLabel(f"高斯高通 - 截止频率：{self.hpf_cutoff}")
        self.hpf_slider = QSlider(Qt.Horizontal)
        self.hpf_slider.setRange(10, 100)
        self.hpf_slider.setValue(self.hpf_cutoff)
        self.hpf_slider.setStyleSheet(slider_style)
        self.hpf_slider.setFixedWidth(300)  # 固定滑块宽度
        self.hpf_slider.valueChanged.connect(self.update_hpf_param)
        self.hpf_param_layout.addWidget(self.hpf_label)
        self.hpf_param_layout.addWidget(self.hpf_slider)
        self.hpf_param_widget.setVisible(False)

        # 3. 带阻滤波参数（中心频率 + 带宽）
        self.br_param_widget = QWidget()
        self.br_param_layout = QHBoxLayout(self.br_param_widget)
        self.br_center_label = QLabel(f"中心频率：{self.br_center_freq}")
        self.br_center_slider = QSlider(Qt.Horizontal)
        self.br_center_slider.setRange(20, 80)
        self.br_center_slider.setValue(self.br_center_freq)
        self.br_center_slider.setStyleSheet(slider_style)
        self.br_center_slider.setFixedWidth(300)  # 固定滑块宽度
        self.br_center_slider.valueChanged.connect(self.update_br_center_param)

        self.br_bandwidth_label = QLabel(f"带宽：{self.br_bandwidth}")
        self.br_bandwidth_slider = QSlider(Qt.Horizontal)
        self.br_bandwidth_slider.setRange(5, 30)
        self.br_bandwidth_slider.setValue(self.br_bandwidth)
        self.br_bandwidth_slider.setStyleSheet(slider_style)
        self.br_bandwidth_slider.setFixedWidth(300)  # 固定滑块宽度
        self.br_bandwidth_slider.valueChanged.connect(self.update_br_bandwidth_param)

        self.br_param_layout.addWidget(QLabel("带阻滤波参数"))  # 分组标题
        self.br_param_layout.addWidget(self.br_center_label)
        self.br_param_layout.addWidget(self.br_center_slider)
        self.br_param_layout.addSpacing(10)
        self.br_param_layout.addWidget(self.br_bandwidth_label)
        self.br_param_layout.addWidget(self.br_bandwidth_slider)
        self.br_param_widget.setVisible(False)

        # 将所有参数Widget添加到总参数布局（居中，间距均匀）
        self.param_layout.addStretch()
        self.param_layout.addWidget(self.lpf_param_widget)
        # self.param_layout.addSpacing(50)
        self.param_layout.addWidget(self.hpf_param_widget)
        # self.param_layout.addSpacing(50)
        self.param_layout.addWidget(self.br_param_widget)
        self.param_layout.addStretch()

    def create_spectrum_labels(self):
        """创建频谱显示标签（固定尺寸，与图像区协调）"""
        # 原始频谱
        self.original_spectrum_label = QLabel()
        self.original_spectrum_label.setText("原始频域频谱")
        self.original_spectrum_label.setAlignment(Qt.AlignCenter)
        # 固定频谱标签尺寸
        self.original_spectrum_label.setFixedSize(self.SPECTRUM_DISPLAY_SIZE[0], self.SPECTRUM_DISPLAY_SIZE[1])
        self.original_spectrum_label.setMinimumSize(self.SPECTRUM_DISPLAY_SIZE[0], self.SPECTRUM_DISPLAY_SIZE[1])
        self.original_spectrum_label.setMaximumSize(self.SPECTRUM_DISPLAY_SIZE[0], self.SPECTRUM_DISPLAY_SIZE[1])
        self.original_spectrum_label.setStyleSheet("""
            border: 2px solid #B0B0B0; 
            padding: 5px; 
            font-size: 14px;
            color: #333333;
        """)
        # 滤波后频谱（与原始频谱尺寸一致）
        self.filtered_spectrum_label = QLabel()
        self.filtered_spectrum_label.setText("滤波后频域频谱")
        self.filtered_spectrum_label.setAlignment(Qt.AlignCenter)
        self.filtered_spectrum_label.setFixedSize(self.SPECTRUM_DISPLAY_SIZE[0], self.SPECTRUM_DISPLAY_SIZE[1])
        self.filtered_spectrum_label.setMinimumSize(self.SPECTRUM_DISPLAY_SIZE[0], self.SPECTRUM_DISPLAY_SIZE[1])
        self.filtered_spectrum_label.setMaximumSize(self.SPECTRUM_DISPLAY_SIZE[0], self.SPECTRUM_DISPLAY_SIZE[1])
        self.filtered_spectrum_label.setStyleSheet(self.original_spectrum_label.styleSheet())
        # 添加到布局（频谱之间留间距，整体居中）
        self.spectrum_layout.addStretch()
        self.spectrum_layout.addWidget(self.original_spectrum_label)
        self.spectrum_layout.addSpacing(50)
        self.spectrum_layout.addWidget(self.filtered_spectrum_label)
        self.spectrum_layout.addStretch()

    def update_freq_button_style(self, clicked_button):
        """更新频域滤波按钮选中状态 + 显示对应参数滑块"""
        # 1. 恢复所有按钮默认样式
        self.main_window.set_button_style(self.gaussian_lpf_button)
        self.main_window.set_button_style(self.gaussian_hpf_button)
        self.main_window.set_button_style(self.band_reject_button)
        # 2. 隐藏所有参数Widget
        self.lpf_param_widget.setVisible(False)
        self.hpf_param_widget.setVisible(False)
        self.br_param_widget.setVisible(False)
        # 3. 设置当前按钮选中样式（统一宽度）
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
        # 4. 显示对应参数Widget + 记录选中的滤波类型
        self.selected_freq_filter = clicked_button.text()
        if self.selected_freq_filter == "高斯低通滤波":
            self.lpf_param_widget.setVisible(True)
        elif self.selected_freq_filter == "高斯高通滤波":
            self.hpf_param_widget.setVisible(True)
        elif self.selected_freq_filter == "带阻滤波（去周期噪声）":
            self.br_param_widget.setVisible(True)
        # 5. 执行滤波（初始参数）
        self.apply_freq_filter()

    # -------------------------- 滑块参数更新方法（新增图片校验） --------------------------
    def update_lpf_param(self, value):
        """更新高斯低通滤波参数（新增图片校验）"""
        # 保险措施：判断图片是否存在
        if not self.main_window.image:
            self.freq_filtered_image_label.setText("请先加载图片再调整参数！")
            self.filtered_spectrum_label.setText("请先加载图片再调整参数！")
            return
        self.lpf_cutoff = value
        self.lpf_label.setText(f"高斯低通 - 截止频率：{self.lpf_cutoff}")
        if self.selected_freq_filter == "高斯低通滤波":
            self.apply_freq_filter()

    def update_hpf_param(self, value):
        """更新高斯高通滤波参数（新增图片校验）"""
        # 保险措施：判断图片是否存在
        if not self.main_window.image:
            self.freq_filtered_image_label.setText("请先加载图片再调整参数！")
            self.filtered_spectrum_label.setText("请先加载图片再调整参数！")
            return
        self.hpf_cutoff = value
        self.hpf_label.setText(f"高斯高通 - 截止频率：{self.hpf_cutoff}")
        if self.selected_freq_filter == "高斯高通滤波":
            self.apply_freq_filter()

    def update_br_center_param(self, value):
        """更新带阻滤波中心频率（新增图片校验）"""
        # 保险措施：判断图片是否存在
        if not self.main_window.image:
            self.freq_filtered_image_label.setText("请先加载图片再调整参数！")
            self.filtered_spectrum_label.setText("请先加载图片再调整参数！")
            return
        self.br_center_freq = value
        self.br_center_label.setText(f"中心频率：{self.br_center_freq}")
        if self.selected_freq_filter == "带阻滤波（去周期噪声）":
            self.apply_freq_filter()

    def update_br_bandwidth_param(self, value):
        """更新带阻滤波带宽（新增图片校验）"""
        # 保险措施：判断图片是否存在
        if not self.main_window.image:
            self.freq_filtered_image_label.setText("请先加载图片再调整参数！")
            self.filtered_spectrum_label.setText("请先加载图片再调整参数！")
            return
        self.br_bandwidth = value
        self.br_bandwidth_label.setText(f"带宽：{self.br_bandwidth}")
        if self.selected_freq_filter == "带阻滤波（去周期噪声）":
            self.apply_freq_filter()

    # -------------------------- 滤波核心逻辑（保留原有校验，优化提示） --------------------------
    def apply_freq_filter(self):
        """执行频域滤波（使用固定尺寸显示，避免缩放）"""
        # 保险措施：判断图片是否存在（核心校验）
        if not self.main_window.image:
            self.freq_filtered_image_label.setText("请先加载图片再执行滤波！")
            self.original_spectrum_label.setText("请先加载图片查看原始频谱！")
            self.filtered_spectrum_label.setText("请先加载图片查看滤波后频谱！")
            return

        try:
            # 图像格式转换（PIL→OpenCV）
            cv_image = cv2.cvtColor(np.array(self.main_window.image), cv2.COLOR_RGB2BGR)
            gray_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
            h, w = gray_image.shape

            # 傅里叶变换（频谱中心化）
            new_h, new_w = cv2.getOptimalDFTSize(h), cv2.getOptimalDFTSize(w)
            padded = cv2.copyMakeBorder(gray_image, 0, new_h - h, 0, new_w - w, cv2.BORDER_CONSTANT, value=0)
            dft = cv2.dft(np.float32(padded), flags=cv2.DFT_COMPLEX_OUTPUT)
            dft_shift = np.fft.fftshift(dft)

            # 显示原始频谱（按固定尺寸缩放）
            self.show_spectrum(dft_shift, self.original_spectrum_label)

            # 创建滤波器
            if self.selected_freq_filter == "高斯低通滤波":
                filter_mask = self.create_gaussian_lpf(new_h, new_w, cutoff=self.lpf_cutoff)
            elif self.selected_freq_filter == "高斯高通滤波":
                filter_mask = self.create_gaussian_hpf(new_h, new_w, cutoff=self.hpf_cutoff)
            elif self.selected_freq_filter == "带阻滤波（去周期噪声）":
                filter_mask = self.create_band_reject_filter(
                    new_h, new_w, 
                    center_freq=self.br_center_freq, 
                    bandwidth=self.br_bandwidth
                )

            # 频谱滤波 + 显示滤波后频谱（固定尺寸）
            filtered_dft = dft_shift * filter_mask[:, :, np.newaxis]
            self.show_spectrum(filtered_dft, self.filtered_spectrum_label)

            # 逆傅里叶变换（得到滤波后图像）
            dft_ishift = np.fft.ifftshift(filtered_dft)
            idft = cv2.idft(dft_ishift)
            result = cv2.magnitude(idft[:, :, 0], idft[:, :, 1])
            result = cv2.normalize(result, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U)
            result = result[:h, :w]

            # 显示滤波后图像（按固定尺寸缩放，保持比例）
            from PIL import Image
            pil_result = Image.fromarray(result)
            q_image = self.main_window.pil_to_qimage(pil_result)
            # 强制按固定尺寸缩放，KeepAspectRatio确保不拉伸
            self.freq_filtered_image_label.setPixmap(
                QPixmap.fromImage(q_image).scaled(
                    self.IMAGE_DISPLAY_SIZE[0], self.IMAGE_DISPLAY_SIZE[1], 
                    Qt.KeepAspectRatio, Qt.SmoothTransformation  # 平滑缩放，避免锯齿
                )
            )

        except Exception as e:
            err_msg = f"出错：{str(e)}"
            self.freq_filtered_image_label.setText(err_msg)
            self.original_spectrum_label.setText(err_msg)
            self.filtered_spectrum_label.setText(err_msg)

    def show_spectrum(self, dft_data, label):
        """显示频域频谱（按固定尺寸缩放，对数缩放优化）"""
        magnitude = 20 * np.log(cv2.magnitude(dft_data[:, :, 0], dft_data[:, :, 1]) + 1)
        magnitude = cv2.normalize(magnitude, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U)
        # 按固定频谱尺寸缩放，保持比例
        magnitude_resized = cv2.resize(
            magnitude, self.SPECTRUM_DISPLAY_SIZE, 
            interpolation=cv2.INTER_LINEAR  # 线性插值，保证频谱清晰度
        )
        spectrum_qimg = QImage(
            magnitude_resized.data, magnitude_resized.shape[1], magnitude_resized.shape[0],
            magnitude_resized.strides[0], QImage.Format_Grayscale8
        )
        label.setPixmap(QPixmap.fromImage(spectrum_qimg))

    def sync_original_image(self):
        """同步主窗口的原始图和原始频谱到Tab3（固定尺寸显示）"""
        # 保险措施：判断图片是否存在
        if not self.main_window.image:
            self.original_image_label_t3.setText("请先加载图片！")
            self.original_spectrum_label.setText("请先加载图片查看原始频谱！")
            return
        # 同步原始图（固定尺寸，平滑缩放）
        q_image = self.main_window.pil_to_qimage(self.main_window.image)
        self.original_image_label_t3.setPixmap(
            QPixmap.fromImage(q_image).scaled(
                self.IMAGE_DISPLAY_SIZE[0], self.IMAGE_DISPLAY_SIZE[1],
                Qt.KeepAspectRatio, Qt.SmoothTransformation
            )
        )
        # 同步原始频谱（固定尺寸）
        cv_image = cv2.cvtColor(np.array(self.main_window.image), cv2.COLOR_RGB2BGR)
        gray_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
        new_h, new_w = cv2.getOptimalDFTSize(gray_image.shape[0]), cv2.getOptimalDFTSize(gray_image.shape[1])
        padded = cv2.copyMakeBorder(gray_image, 0, new_h - gray_image.shape[0], 0, new_w - gray_image.shape[1], cv2.BORDER_CONSTANT, value=0)
        dft = cv2.dft(np.float32(padded), flags=cv2.DFT_COMPLEX_OUTPUT)
        dft_shift = np.fft.fftshift(dft)
        self.show_spectrum(dft_shift, self.original_spectrum_label)

    # -------------------------- 滤波器创建方法 --------------------------
    def create_gaussian_lpf(self, h, w, cutoff):
        """高斯低通滤波器"""
        x, y = np.meshgrid(np.arange(w), np.arange(h))
        cx, cy = w // 2, h // 2
        distance = np.sqrt((x - cx)**2 + (y - cy)**2)
        return np.exp(-(distance**2) / (2 * cutoff**2))

    def create_gaussian_hpf(self, h, w, cutoff):
        """高斯高通滤波器"""
        return 1 - self.create_gaussian_lpf(h, w, cutoff)

    def create_band_reject_filter(self, h, w, center_freq, bandwidth):
        """高斯带阻滤波器"""
        x, y = np.meshgrid(np.arange(w), np.arange(h))
        cx, cy = w // 2, h // 2
        distance = np.sqrt((x - cx)**2 + (y - cy)**2)
        band_pass = np.exp(-((distance - center_freq)**2) / (2 * (bandwidth/2)**2)) - \
                    np.exp(-((distance + center_freq)**2) / (2 * (bandwidth/2)**2))
        return 1 - band_pass

    def get_layout(self):
        """返回Tab3布局（供主窗口调用）"""
        return self.layout