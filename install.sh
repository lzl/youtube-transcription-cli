#!/bin/bash
# YouTube Transcription CLI 快速安装脚本

echo "🚀 正在安装 YouTube Transcription CLI (yt-t)..."

# 检查 Python 是否已安装
if ! command -v python3 &> /dev/null; then
    echo "❌ 错误: 未找到 Python 3"
    echo "请先安装 Python 3: https://www.python.org/downloads/"
    exit 1
fi

# 检查 pip 是否已安装
if ! command -v pip3 &> /dev/null; then
    echo "❌ 错误: 未找到 pip3"
    echo "请先安装 pip"
    exit 1
fi

# 创建临时目录
TEMP_DIR=$(mktemp -d)
cd "$TEMP_DIR"

# 下载项目文件
echo "📥 正在下载项目文件..."
curl -L https://github.com/yourusername/youtube-transcription-cli/archive/main.zip -o yt-t.zip
unzip -q yt-t.zip
cd youtube-transcription-cli-main

# 安装依赖
echo "📦 正在安装依赖..."
pip3 install --user -r requirements.txt

# 安装工具
echo "🔧 正在安装 yt-t..."
pip3 install --user .

# 清理临时文件
cd /
rm -rf "$TEMP_DIR"

echo "✅ 安装完成！"
echo ""
echo "使用方法:"
echo "  yt-t <YouTube视频URL>"
echo ""
echo "示例:"
echo "  yt-t https://www.youtube.com/watch?v=dQw4w9WgXcQ"
echo ""
echo "注意: 如果命令找不到，可能需要将 ~/.local/bin 添加到 PATH"
echo "可以运行: export PATH=\"\$PATH:\$HOME/.local/bin\""