from PIL import Image
# 打开含ZY的原始图片（替换为你的图片路径）
img = Image.open("Qt 中设置控件样式表.png")
# 转换为RGBA模式以支持透明背景
img = img.convert("RGBA")
# 保存为ico，包含多尺寸适配不同场景
img.save("zy_app.ico", sizes=((32,32), (48,48), (256,256)))