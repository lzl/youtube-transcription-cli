#!/usr/bin/env python3
import click
import sys
import os
from dotenv import load_dotenv
from .youtube import extract_video_id, get_native_subtitles
from .gemini import transcribe_with_gemini
from .utils import save_transcript

# 加载 .env 文件
load_dotenv()


@click.command()
@click.argument('url')
@click.option('--output', '-o', help='输出文件路径')
@click.option('--output-dir', '-d', help='输出目录（默认: transcripts）')
@click.option('--language', '-l', default='zh-CN', help='字幕语言代码（默认: zh-CN）')
def main(url: str, output: str = None, output_dir: str = None, language: str = 'zh-CN'):
    """YouTube Transcription CLI - 从YouTube视频提取字幕"""
    
    print(f"正在处理视频: {url}")
    
    video_id = extract_video_id(url)
    if not video_id:
        click.echo("错误: 无法从URL中提取视频ID", err=True)
        sys.exit(1)
    
    print(f"视频ID: {video_id}")
    
    print("尝试获取原生字幕...")
    transcript = get_native_subtitles(video_id)
    
    if transcript:
        print("成功获取原生字幕！")
    else:
        print("未找到原生字幕，尝试使用 Gemini API...")
        
        if not os.environ.get("GEMINI_API_KEY"):
            click.echo("错误: 未设置 GEMINI_API_KEY 环境变量", err=True)
            click.echo("请设置环境变量: export GEMINI_API_KEY='your-api-key'", err=True)
            sys.exit(1)
        
        transcript = transcribe_with_gemini(url)
        
        if not transcript:
            click.echo("错误: 无法获取视频字幕", err=True)
            sys.exit(1)
    
    if output:
        # 如果指定了具体输出文件路径，直接使用
        filepath = output
        os.makedirs(os.path.dirname(filepath), exist_ok=True) if os.path.dirname(filepath) else None
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(transcript)
    else:
        # 使用默认保存逻辑，支持自定义输出目录
        filepath = save_transcript(transcript, video_id, url, output_dir)
    
    print(f"\n字幕已保存到: {filepath}")
    print(f"文件大小: {os.path.getsize(filepath) / 1024:.1f} KB")


if __name__ == '__main__':
    main()