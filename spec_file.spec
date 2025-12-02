# -*- mode: python ; coding: utf-8 -*-

import sys
from PyInstaller.building.api import PYZ, EXE, COLLECT
from PyInstaller.building.build_main import Analysis
from PyInstaller.utils.hooks import collect_data_files, collect_submodules

# 基础配置
block_cipher = None
sys.setrecursionlimit(10000)  # 解决递归深度问题

# 分析主程序及依赖
a = Analysis(
    ['main_window.py'],  # 主程序入口
    pathex=['.'],  # 项目根目录
    binaries=[],
    datas=collect_data_files('cv2') + collect_data_files('numpy') + collect_data_files('PIL'),
    hiddenimports=collect_submodules('cv2') + collect_submodules('numpy') + collect_submodules('PIL') + [
        'PyQt5.QtWidgets', 'PyQt5.QtGui', 'PyQt5.QtCore',  # GUI核心模块
        'tab1_process', 'tab2_spatial', 'tab3_frequency',  # 各Tab模块
        'tab4_morphology', 'tab5_edge_detection', 'tab7_about'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'tkinter', 'PyQt6', 'matplotlib.testing',  # 排除未使用模块
        'unittest', 'pydoc', 'doctest', 'setuptools'
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

# 打包为单一文件
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='图像处理工具',  # 生成的EXE文件名
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,  # 启用UPX压缩
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # 无控制台窗口（黑框）
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,  # 如需图标可指定，如'icon.ico'
    base='Win32GUI'  # Windows GUI程序模式
)