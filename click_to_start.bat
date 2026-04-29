@echo off
:: 设置控制台编码为 UTF-8，防止打印的中文字符变成乱码
chcp 65001 >nul

cd /d "%~dp0"

:: 检查当前目录下是否已经存在 venv 文件夹
if not exist "venv\" (
    echo [提示] 未检测到虚拟环境，正在为您创建独立运行环境...
    python -m venv venv
    echo [成功] 虚拟环境创建完成！
)


echo [提示] 正在激活虚拟环境...
call venv\Scripts\activate.bat


echo [提示] 正在检查并安装 requirements.txt...
python -m pip install --upgrade pip >nul 2>&1
pip install -r requirements.txt


echo [提示] 正在运行主程序...
echo ==========================================
python main.py


echo.
echo [提示] 程序已结束。
pause
