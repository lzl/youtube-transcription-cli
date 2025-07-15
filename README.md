# YouTube Transcription CLI (yt-t)

一个命令行工具，用于快速从 YouTube 视频中提取字幕并保存为格式化的文本文件。

## 功能特点

- 优先获取 YouTube 原生字幕
- 当视频没有字幕时，使用 Google Gemini API 自动生成字幕
- 支持自定义输出文件路径
- 自动提取视频标题作为文件名
- 时间戳格式化输出

## 安装

### 方法一：直接下载可执行文件（推荐给非技术用户）

1. 下载对应系统的可执行文件：
   - macOS/Linux: `dist/yt-t`
   - Windows: `dist/yt-t.exe`

2. 给文件添加执行权限（macOS/Linux）：
   ```bash
   chmod +x yt-t
   ```

3. 直接运行：
   ```bash
   ./yt-t https://www.youtube.com/watch?v=VIDEO_ID
   ```

### 方法二：通过 pip 安装（需要 Python 环境）

```bash
pip install yt-t
```

### 方法三：使用安装脚本

**macOS/Linux:**
```bash
curl -L https://github.com/yourusername/youtube-transcription-cli/raw/main/install.sh | bash
```

**Windows:**
下载并运行 `install_windows.bat`

### 方法四：从源代码安装（开发者）

首先确保已安装 uv：

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

然后安装项目：

```bash
uv sync
```

或者在开发模式下安装：

```bash
uv pip install -e .
```

## 使用方法

### 基本用法

```bash
yt-t https://www.youtube.com/watch?v=VIDEO_ID
```

如果是从源代码运行：

```bash
uv run yt-t https://www.youtube.com/watch?v=VIDEO_ID
```

### 指定输出文件

```bash
yt-t https://www.youtube.com/watch?v=VIDEO_ID -o output.txt
```

### 设置 Gemini API Key

如果视频没有原生字幕，工具会使用 Gemini API 生成字幕。需要先设置环境变量：

```bash
export GEMINI_API_KEY='your-api-key-here'
```

## 输出格式

字幕文件包含以下信息：
- 原始视频地址
- 视频ID
- 视频标题
- 生成时间
- 带时间戳的字幕内容

示例：
```
[00:01] Hello world
[00:05] This is the second sentence
[00:10] Continuing with more content
```

## 依赖管理

本项目使用 [uv](https://github.com/astral-sh/uv) 进行 Python 依赖管理。

### 主要依赖

- Python 3.9+
- click>=8.0.0
- youtube-transcript-api>=0.6.0
- google-genai>=0.1.0
- requests>=2.25.0

### 开发依赖

- pytest>=7.0.0
- black>=23.0.0
- ruff>=0.1.0

所有依赖在 `pyproject.toml` 中定义，通过 `uv sync` 自动安装。

## 分享给朋友

如果你想分享这个工具给不懂编程的朋友，推荐使用以下方式：

### 最简单的方法

1. 运行构建脚本生成可执行文件：
   ```bash
   python build_executable.py
   ```

2. 将生成的 `dist/yt-t` 文件发送给朋友

3. 朋友收到后只需：
   - macOS/Linux: `chmod +x yt-t && ./yt-t <YouTube链接>`
   - Windows: 双击运行 `yt-t.exe <YouTube链接>`

### 其他分享方式

- **一键安装脚本**: 发送 `install.sh` (macOS/Linux) 或 `install_windows.bat` (Windows)
- **pip 安装**: 如果已发布到 PyPI，朋友可以直接 `pip install yt-t`

## 许可证

MIT License