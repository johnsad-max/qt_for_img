import os
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QTabWidget, 
                            QLabel, QPushButton, QRadioButton, QFileDialog, QMessageBox,
                            QDialog)
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QDesktopServices
from PIL import Image

# 假设其他Tab的类定义已存在（Tab1Processor, Tab2SpatialFilter等）
from tab1_process import Tab1Processor
from tab2_spatial import Tab2SpatialFilter
from tab3_frequency import Tab3FrequencyFilter
from tab4_morphology import Tab4Morphology
from tab5_edge_detection import Tab5EdgeDetection
from tab7_about import Tab7About

class MyMainWindow(QMainWindow):
    def __init__(self):
        super(MyMainWindow, self).__init__()
        self.init_global_attrs()  # 初始化全局属性（跨Tab共享）
        self.init_window_style()  # 设置窗口样式（全局渐变背景）
        self.init_ui()            # 构建主界面

    def init_global_attrs(self):
        """全局共享属性"""
        self.image = None          # 加载的图像（PIL格式）
        self.image_path = None     # 图像路径
        self.temp_png_path = "temp_process.png"  # 临时PNG路径
        self.temp_files = [
            "gray_image.png",
            "frequency_image.png",
            self.temp_png_path  # 假设临时PNG路径也需要清理
        ]   
    def init_window_style(self):
        """设置窗口基础样式（全局渐变背景+Tab样式）"""
        self.setWindowTitle("Image Processing Tool")
        self.setGeometry(100, 100, 1400, 700)
        
        # 全局样式（渐变背景+Tab控件优化）
        self.setStyleSheet("""
            QMainWindow {
                /* 纵向渐变：浅蓝→浅紫（柔和对比） */
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                           stop:0 #E0F7FA, stop:1 #F3E5F5);
            }
            /* Tab容器样式 */
            QTabWidget::pane {
                border: 2px solid #B0B0B0;
                background: transparent;  /* 继承主窗口渐变 */
                border-radius: 4px;
            }
            /* Tab标签样式 */
            QTabBar::tab {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                           stop:0 #E1E1E1, stop:0.4 #DDDDDD,
                                           stop:0.5 #D8D8D8, stop:1.0 #D3D3D3);
                border: 1px solid #C4C4C3;
                border-bottom-color: #C2C7CB;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
                min-width: 8ex;
                padding: 8px;
                margin-right: 2px;
                font-size: 13px;
            }
            /* 选中/悬浮Tab样式 */
            QTabBar::tab:selected, QTabBar::tab:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                           stop:0 #fafafa, stop:0.4 #f4f4f4,
                                           stop:0.5 #e7e7e7, stop:1.0 #fafafa);
                border-color: #999999;
            }
            /* 图像显示标签边框优化 */
            QLabel {
                font-size: 14px;
                color: #333333;
            }
        """)

    def init_ui(self):
        """构建主窗口（Tab容器）- 包含导出按钮"""
        main_layout = QHBoxLayout()
        # 创建Tab控件
        self.tabs = QTabWidget(self)
        self.tabs.setTabPosition(QTabWidget.North)
        
        # 添加导出按钮
        self.top_right_widget = QWidget()
        self.top_right_layout = QHBoxLayout(self.top_right_widget)
        self.top_right_layout.setContentsMargins(0, 0, 10, 0)
        
        # 导出按钮
        self.export_button = QPushButton("导出图片")
        self.set_button_style(self.export_button)
        self.export_button.clicked.connect(self.show_export_dialog)
        self.top_right_layout.addWidget(self.export_button)
        
        # 将按钮容器添加到主窗口
        self.tabs.setCornerWidget(self.top_right_widget, Qt.TopRightCorner)
        
        # 设置Tab栏标签样式
        self.tabs.setStyleSheet("""
            QTabBar::tab {
                width: 120px;  /* 固定每个Tab标签的宽度 */
                height: 35px;  /* 固定标签高度 */
                text-align: center;  /* 标签文字居中 */
                font-size: 13px;  /* 统一标签文字大小 */
            }
            QTabBar::tab:selected {
                background-color: rgba(230, 126, 34, 0.1);  /* 选中标签背景色 */
            }
        """)
        
        # 创建Tab页面（移除了Tab6）
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tab3 = QWidget()
        self.tab4 = QWidget()
        self.tab5 = QWidget()
        self.tab7 = QWidget()  # 关于页面
        # 初始化各Tab内容
        self.init_tab1()
        self.init_tab2()
        self.init_tab3()
        self.init_tab4()
        self.init_tab5()
        self.init_tab7()
        # 添加Tab到容器
        self.tabs.addTab(self.tab1, "图像处理")
        self.tabs.addTab(self.tab2, "空间域滤波")
        self.tabs.addTab(self.tab3, "频域滤波")
        self.tabs.addTab(self.tab4, "形态学处理")
        self.tabs.addTab(self.tab5, "边缘检测")
        self.tabs.addTab(self.tab7, "关于")
        
        # 限制Tab内容区域最大宽度
        tab_container = QWidget()
        tab_container.setMaximumWidth(1900)
        tab_layout = QVBoxLayout(tab_container)
        tab_layout.addWidget(self.tabs)
        tab_layout.setContentsMargins(0, 0, 0, 0)
        
        # 设置主布局
        main_layout.addWidget(tab_container)
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

    def init_tab1(self):
        """初始化Tab1：基础图像处理"""
        self.tab1_processor = Tab1Processor(self)
        self.tab1.setLayout(self.tab1_processor.get_layout())

    def init_tab2(self):
        """初始化Tab2：空间域滤波"""
        self.tab2_filter = Tab2SpatialFilter(self)
        self.tab2.setLayout(self.tab2_filter.get_layout())

    def init_tab3(self):
        """初始化Tab3：频域滤波"""
        self.tab3_filter = Tab3FrequencyFilter(self)
        self.tab3.setLayout(self.tab3_filter.get_layout())

    def init_tab4(self):
        """初始化Tab4：形态学处理"""
        self.tab4_filter = Tab4Morphology(self)
        self.tab4.setLayout(self.tab4_filter.get_layout())

    def init_tab5(self):
        """初始化Tab5：边缘检测"""
        self.tab5_filter = Tab5EdgeDetection(self)
        self.tab5.setLayout(self.tab5_filter.get_layout())
    
    def init_tab7(self):
        """初始化Tab7：关于页面"""
        self.tab7_processor = Tab7About()
        self.tab7.setLayout(self.tab7_processor.get_layout())

    # 全局通用方法
    def pil_to_qimage(self, pil_image):
        """PIL图像转QImage（全局通用）"""
        pil_image = pil_image.convert("RGB")
        data = pil_image.tobytes("raw", "RGB")
        qim = QImage(data, pil_image.width, pil_image.height, 
                     pil_image.width * 3, QImage.Format_RGB888)
        return qim

    def set_button_style(self, button):
        """设置按钮默认样式"""
        button.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                                        stop:0 #FFFFFF, stop:1 #E0E0E0);
                color: #222222;
                font-size: 14px;
                padding: 10px;
                max-width: 200px;
                border: 1px solid #AAAAAA;
                border-radius: 6px;
                outline: none;
                font-weight: 500;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                                        stop:0 #F5F5F5, stop:1 #D0D0D0);
                border-color: #888888;
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                                        stop:0 #D0D0D0, stop:1 #F5F5F5);
            }
        """)

    # 导出图片功能
    def show_export_dialog(self):
        """显示导出选项对话框"""
        dialog = QDialog(self)
        dialog.setWindowTitle("导出图片")
        dialog.setGeometry(300, 300, 300, 150)
        
        layout = QVBoxLayout(dialog)
        
        # 导出选项
        self.current_tab_radio = QRadioButton("仅当前页面")
        self.all_tabs_radio = QRadioButton("全部页面")
        self.current_tab_radio.setChecked(True)
        
        layout.addWidget(QLabel("请选择导出范围："))
        layout.addWidget(self.current_tab_radio)
        layout.addWidget(self.all_tabs_radio)
        
        # 按钮区
        btn_layout = QHBoxLayout()
        ok_btn = QPushButton("确定")
        cancel_btn = QPushButton("取消")
        
        ok_btn.clicked.connect(lambda: self.export_images(dialog))
        cancel_btn.clicked.connect(dialog.close)
        
        btn_layout.addWidget(ok_btn)
        btn_layout.addWidget(cancel_btn)
        layout.addLayout(btn_layout)
        
        dialog.exec_()

    def export_images(self, dialog):
        """导出选中范围的图片"""
        # 获取导出范围
        export_all = self.all_tabs_radio.isChecked()
        current_index = self.tabs.currentIndex()
        dialog.close()
        
        # 获取保存路径
        if export_all:
            # 导出全部时选择文件夹
            save_path = QFileDialog.getExistingDirectory(self, "选择保存文件夹", "")
            if not save_path:
                return
                
            # 为每个页面创建子文件夹
            success = True
            tab_names = ["图像处理", "空间域滤波", "频域滤波", "形态学处理", "边缘检测"]
            
            for i in range(5):
                tab_folder = os.path.join(save_path, tab_names[i])
                os.makedirs(tab_folder, exist_ok=True)
                
                # 导出对应页面的图片
                if not self.export_tab_images(i, tab_folder):
                    success = False
                    break
                    
            if success:
                QMessageBox.information(self, "成功", f"所有页面图片已导出到:\n{save_path}")
            else:
                QMessageBox.warning(self, "失败", "部分图片导出失败")
                
        else:
            # 导出当前页面，选择文件路径
            tab_name = self.tabs.tabText(current_index)
            default_filename = f"{tab_name}_result.png"
            
            file_path, _ = QFileDialog.getSaveFileName(
                self, "保存图片", default_filename, "PNG图片 (*.png);;JPEG图片 (*.jpg);;所有文件 (*)"
            )
            
            if file_path:
                if self.export_tab_images(current_index, os.path.dirname(file_path), os.path.basename(file_path)):
                    QMessageBox.information(self, "成功", f"图片已保存到:\n{file_path}")
                else:
                    QMessageBox.warning(self, "失败", "图片导出失败")

    def export_tab_images(self, tab_index, save_dir, filename=None):
        """导出指定页面的图片"""
        try:
            if tab_index == 0:  # 图像处理
                # 导出灰度图和频谱图
                if filename:
                    # 只导出当前结果
                    self._export_label_image(self.tab1_processor.gray_image_label, save_dir, filename)
                else:
                    self._export_label_image(self.tab1_processor.gray_image_label, save_dir, "灰度图.png")
                    self._export_label_image(self.tab1_processor.frequency_image_label, save_dir, "频谱图.png")
                    
            elif tab_index == 1:  # 空间域滤波
                self._export_label_image(self.tab2_filter.filtered_image_label, save_dir, filename or "空间域滤波结果.png")
                
            elif tab_index == 2:  # 频域滤波
                self._export_label_image(self.tab3_filter.freq_filtered_image_label, save_dir, filename or "频域滤波结果.png")
                
            elif tab_index == 3:  # 形态学处理
                self._export_label_image(self.tab4_filter.morph_result_label, save_dir, filename or "形态学处理结果.png")
                
            elif tab_index == 4:  # 边缘检测
                self._export_label_image(self.tab5_filter.edge_result_label, save_dir, filename or "边缘检测结果.png")
                
            return True
        except Exception as e:
            print(f"导出图片失败: {str(e)}")
            return False

    def _export_label_image(self, label, save_dir, filename):
        """导出标签中显示的图片"""
        pixmap = label.pixmap()
        if pixmap and not pixmap.isNull():
            # 保存QPixmap到目标路径
            target_path = os.path.join(save_dir, filename)
            if pixmap.save(target_path):
                return True
            else:
                raise Exception(f"无法保存图片到 {target_path}")
        else:
            raise Exception(f"没有可导出的图片")
        
    def clean_temp_files(self):
        """清理程序运行过程中生成的临时文件"""
        for file_path in self.temp_files:
            try:
                if os.path.exists(file_path):
                    os.remove(file_path)
                    print(f"已删除临时文件: {file_path}")
            except Exception as e:
                print(f"删除临时文件 {file_path} 失败: {str(e)}")
    
    def closeEvent(self, event):
        """窗口关闭时执行清理操作"""
        self.clean_temp_files()
        event.accept()  # 接受关闭事件

if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    window = MyMainWindow()
    window.show()
    sys.exit(app.exec_())