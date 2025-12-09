# -*- mode: python ; coding: utf-8 -*-

import sys
import os  # 新增：处理路径，避免相对路径问题
from PyInstaller.building.api import PYZ, EXE, COLLECT
from PyInstaller.building.build_main import Analysis
from PyInstaller.utils.hooks import collect_data_files, collect_submodules

# 基础配置
block_cipher = None
sys.setrecursionlimit(10000)

# 新增：获取ICO文件绝对路径（避免相对路径坑）
ico_path = os.path.abspath("zy_app.ico")  # 确保zy_app.ico和spec文件同目录

# 分析主程序及依赖
a = Analysis(
    ['main_window.py'],
    pathex=['.'],
    binaries=[],
    datas=collect_data_files('cv2') + collect_data_files('numpy') + collect_data_files('PIL'),
    hiddenimports=collect_submodules('cv2') + collect_submodules('numpy') + collect_submodules('PIL') + [
        'PyQt5.QtWidgets', 'PyQt5.QtGui', 'PyQt5.QtCore',
        'tab1_process', 'tab2_spatial', 'tab3_frequency',
        'tab4_morphology', 'tab5_edge_detection', 'tab7_about'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'tkinter', 'PyQt6', 'matplotlib.testing',
        'unittest', 'pydoc', 'doctest', 'setuptools'
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='img_process_tool',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,  # 先关闭UPX测试图标，生效后再改True+upx_exclude
    upx_exclude=[ico_path],  # 备用：开启UPX时排除ICO文件
    runtime_tmpdir=None,
    console=False,  # 保留GUI模式，删除冗余的base='Win32GUI'
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=ico_path,  # 使用绝对路径
)