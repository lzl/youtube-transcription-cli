# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 项目概述

这是一个 YouTube 字幕提取命令行工具，支持获取原生字幕或使用 Google Gemini API 自动生成字幕。

## 开发命令

```bash
# 安装依赖（使用 uv 包管理器）
uv sync

# 运行程序
uv run yt-t [URL]

# 代码格式化
uv run black .

# 代码检查
uv run ruff check .

# 构建发布包
uv run python -m build
```

## 核心架构

### 模块结构
- `cli.py`: 命令行入口，处理参数解析和流程协调
- `youtube.py`: YouTube 原生字幕获取逻辑
- `gemini.py`: Gemini API 转录实现，包含长视频分割处理
- `audio_utils.py`: 音频下载和处理（依赖 yt-dlp 和 ffmpeg）
- `video_utils.py`: 视频信息提取
- `utils.py`: 通用工具函数

### 字幕获取流程
1. 优先尝试获取 YouTube 原生字幕（支持多语言）
2. 原生字幕不可用时，下载音频并使用 Gemini API 转录
3. 长视频（>50分钟）会自动进行音频加速和分割处理

### 关键技术决策
- 使用 uv 作为包管理器（而非 pip）
- 使用 click 框架构建 CLI
- 长音频通过 2x 加速优化 API 调用时间
- 自动处理视频 ID 提取和各种 URL 格式

## 注意事项

1. **环境变量**: Gemini API 需要设置 `GEMINI_API_KEY`
2. **系统依赖**: 音频处理需要 ffmpeg（程序会检查并提示安装）
3. **输出目录**: 默认输出到 `transcripts/` 目录
4. **临时文件**: 音频文件下载到系统临时目录，处理后自动清理