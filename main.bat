@echo off
chcp 65001 >nul
echo 正在批量导入图片到 Scratch 项目...
python import_costumes.py
echo.
echo 按任意键退出...
pause >nul