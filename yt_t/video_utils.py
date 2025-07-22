import yt_dlp
from typing import Dict, List, Tuple, Optional
import math


def get_video_info(url: str) -> Dict:
    """获取YouTube视频信息，包括时长"""
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'extract_flat': False,
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(url, download=False)
            return {
                'title': info.get('title', ''),
                'duration': info.get('duration', 0),  # 秒
                'video_id': info.get('id', ''),
                'uploader': info.get('uploader', ''),
                'upload_date': info.get('upload_date', ''),
            }
        except Exception as e:
            print(f"获取视频信息失败: {str(e)}")
            return None


def calculate_segments(duration_seconds: int, segment_minutes: int = 50) -> List[Tuple[int, int]]:
    """计算视频分段时间点
    
    Args:
        duration_seconds: 视频总时长（秒）
        segment_minutes: 每段时长（分钟），默认50分钟
    
    Returns:
        分段列表，每个元素为 (开始时间, 结束时间) 的元组，单位为秒
    """
    segment_seconds = segment_minutes * 60
    total_segments = math.ceil(duration_seconds / segment_seconds)
    
    segments = []
    for i in range(total_segments):
        start = i * segment_seconds
        end = min((i + 1) * segment_seconds, duration_seconds)
        segments.append((start, end))
    
    return segments


def format_time(seconds: int) -> str:
    """将秒数格式化为 HH:MM:SS 格式"""
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    
    if hours > 0:
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    else:
        return f"{minutes:02d}:{seconds:02d}"


def should_split_video(duration_seconds: int, threshold_minutes: int = 50) -> bool:
    """判断视频是否需要分割
    
    Args:
        duration_seconds: 视频时长（秒）
        threshold_minutes: 分割阈值（分钟），默认50分钟
    
    Returns:
        是否需要分割
    """
    return duration_seconds > threshold_minutes * 60