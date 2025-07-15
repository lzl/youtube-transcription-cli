# YouTube Transcription CLI (yt-t)

一个命令行工具，用于快速从 YouTube 视频中提取字幕并保存为格式化的文本文件。

## 功能特点

- 优先获取 YouTube 原生字幕
- 当视频没有字幕时，使用 Google Gemini API 自动生成字幕
- 支持自定义输出文件路径
- 自动提取视频标题作为文件名
- 时间戳格式化输出

## 安装

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
uv run yt-t https://www.youtube.com/watch?v=VIDEO_ID
```

或者在激活虚拟环境后：

```bash
yt-t https://www.youtube.com/watch?v=VIDEO_ID
```

### 指定输出文件

```bash
uv run yt-t https://www.youtube.com/watch?v=VIDEO_ID -o output.txt
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

## 许可证

MIT License