@echo off
REM YouTube Transcription CLI Windows 安装脚本

echo 🚀 正在安装 YouTube Transcription CLI (yt-t)...

REM 检查 Python 是否已安装
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ 错误: 未找到 Python
    echo 请先安装 Python: https://www.python.org/downloads/
    pause
    exit /b 1
)

REM 检查 pip 是否已安装
pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ 错误: 未找到 pip
    echo 请确保 Python 安装时勾选了 "Add Python to PATH"
    pause
    exit /b 1
)

echo 📦 正在安装 yt-t...
pip install yt-t

if %errorlevel% equ 0 (
    echo.
    echo ✅ 安装完成！
    echo.
    echo 使用方法:
    echo   yt-t ^<YouTube视频URL^>
    echo.
    echo 示例:
    echo   yt-t https://www.youtube.com/watch?v=dQw4w9WgXcQ
) else (
    echo.
    echo ❌ 安装失败，请检查错误信息
)

pause