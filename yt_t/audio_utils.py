import os
import tempfile
import shutil
import subprocess
import json
from typing import List, Optional
import yt_dlp
import math


def check_ffmpeg():
    """检查ffmpeg是否已安装"""
    try:
        subprocess.run(['ffmpeg', '-version'], capture_output=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("错误: 未安装 ffmpeg。请先安装 ffmpeg:")
        print("  macOS: brew install ffmpeg")
        print("  Ubuntu/Debian: sudo apt-get install ffmpeg")
        print("  Windows: 从 https://ffmpeg.org/download.html 下载")
        return False


def download_audio(youtube_url: str, output_dir: str = None) -> Optional[str]:
    """下载YouTube视频的音频
    
    Args:
        youtube_url: YouTube视频URL
        output_dir: 输出目录，默认使用临时目录
    
    Returns:
        下载的音频文件路径，失败返回None
    """
    if not check_ffmpeg():
        return None
        
    if output_dir is None:
        output_dir = tempfile.mkdtemp(prefix="yt_audio_")
    
    # 配置yt-dlp只下载音频
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
        'quiet': True,
        'no_warnings': True,
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            print("正在下载音频...")
            info = ydl.extract_info(youtube_url, download=True)
            
            # 获取下载后的文件路径
            filename = ydl.prepare_filename(info)
            # 替换扩展名为mp3
            audio_path = os.path.splitext(filename)[0] + '.mp3'
            
            if os.path.exists(audio_path):
                print(f"音频已下载到: {audio_path}")
                return audio_path
            else:
                print("音频下载失败")
                return None
                
    except Exception as e:
        print(f"下载音频失败: {str(e)}")
        return None


def speed_up_audio(audio_path: str, speed: float = 2.0) -> str:
    """加速音频文件
    
    Args:
        audio_path: 原始音频文件路径
        speed: 加速倍数，默认2倍速
    
    Returns:
        加速后的音频文件路径
    """
    print(f"正在将音频加速到 {speed}x...")
    
    # 输出文件路径
    speeded_path = audio_path.replace('.mp3', f'_speed{speed}x.mp3')
    
    # 使用ffmpeg加速音频，保持音调
    cmd = [
        'ffmpeg', '-i', audio_path,
        '-filter:a', f'atempo={speed}',
        '-y',  # 覆盖输出文件
        speeded_path
    ]
    
    try:
        subprocess.run(cmd, capture_output=True, check=True)
        print(f"加速音频已保存到: {speeded_path}")
        return speeded_path
    except subprocess.CalledProcessError as e:
        print(f"音频加速失败: {e.stderr.decode()}")
        raise


def get_audio_duration(audio_path: str) -> float:
    """获取音频文件时长（秒）"""
    cmd = [
        'ffprobe', '-v', 'quiet', '-print_format', 'json',
        '-show_format', '-show_streams', audio_path
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, check=True, text=True)
        data = json.loads(result.stdout)
        duration = float(data['format']['duration'])
        return duration
    except (subprocess.CalledProcessError, KeyError, ValueError) as e:
        print(f"获取音频时长失败: {str(e)}")
        raise


def split_audio(audio_path: str, segment_minutes: int = 50) -> List[str]:
    """分割音频文件
    
    Args:
        audio_path: 音频文件路径
        segment_minutes: 每段时长（分钟）
    
    Returns:
        分割后的音频文件路径列表
    """
    duration = get_audio_duration(audio_path)
    duration_minutes = duration / 60
    
    # 计算需要分割的段数
    num_segments = math.ceil(duration_minutes / segment_minutes)
    
    if num_segments == 1:
        # 不需要分割
        return [audio_path]
    
    print(f"音频将被分割为 {num_segments} 段...")
    
    # 分割音频
    segments = []
    base_name = os.path.splitext(audio_path)[0]
    segment_seconds = segment_minutes * 60
    
    for i in range(num_segments):
        start_seconds = i * segment_seconds
        
        # 输出文件路径
        segment_path = f"{base_name}_part{i+1}.mp3"
        
        # 构建ffmpeg命令
        cmd = [
            'ffmpeg', '-i', audio_path,
            '-ss', str(start_seconds),  # 开始时间
            '-t', str(segment_seconds),  # 持续时间
            '-c', 'copy',  # 直接复制，不重新编码
            '-y',  # 覆盖输出文件
            segment_path
        ]
        
        try:
            subprocess.run(cmd, capture_output=True, check=True)
            segments.append(segment_path)
            
            # 显示进度
            end_seconds = min((i + 1) * segment_seconds, duration)
            start_time = format_time_seconds(start_seconds)
            end_time = format_time_seconds(end_seconds)
            print(f"  第 {i+1} 段: {start_time} - {end_time} 已保存")
            
        except subprocess.CalledProcessError as e:
            print(f"分割音频失败: {e.stderr.decode()}")
            raise
    
    return segments


def format_time_seconds(seconds: float) -> str:
    """将秒数格式化为时间字符串"""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = int(seconds % 60)
    
    if hours > 0:
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    else:
        return f"{minutes:02d}:{seconds:02d}"


def cleanup_temp_files(file_paths: List[str]):
    """清理临时文件"""
    for file_path in file_paths:
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                print(f"已删除临时文件: {file_path}")
        except Exception as e:
            print(f"删除文件失败 {file_path}: {str(e)}")
    
    # 清理临时目录
    for file_path in file_paths:
        dir_path = os.path.dirname(file_path)
        if dir_path.startswith(tempfile.gettempdir()) and os.path.exists(dir_path):
            try:
                shutil.rmtree(dir_path)
                print(f"已删除临时目录: {dir_path}")
                break  # 只需要删除一次目录
            except Exception as e:
                print(f"删除目录失败 {dir_path}: {str(e)}")