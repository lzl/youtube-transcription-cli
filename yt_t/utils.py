import re
import os
from datetime import datetime
from typing import Optional
import requests


def sanitize_filename(filename: str) -> str:
    """Sanitize filename for filesystem"""
    filename = re.sub(r'[<>:"/\\|?*]', '', filename)
    filename = filename.strip('. ')
    return filename[:200] if len(filename) > 200 else filename


def get_video_title(video_id: str) -> Optional[str]:
    """Get video title from YouTube (simplified without API)"""
    try:
        url = f"https://www.youtube.com/watch?v={video_id}"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        
        match = re.search(r'<title>(.*?) - YouTube</title>', response.text)
        if match:
            return match.group(1)
        
        match = re.search(r'"title":"(.*?)"', response.text)
        if match:
            return match.group(1).encode().decode('unicode_escape')
            
    except:
        pass
    
    return None


def save_transcript(transcript: str, video_id: str, video_url: str, output_dir: str = None) -> str:
    """Save transcript to file"""
    # 默认保存目录
    if output_dir is None:
        output_dir = "transcripts"
    
    # 确保输出目录存在
    os.makedirs(output_dir, exist_ok=True)
    
    title = get_video_title(video_id)
    
    if title:
        filename = f"{sanitize_filename(title)}_transcript_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    else:
        filename = f"youtube_transcript_{video_id}.txt"
    
    # 组合完整路径
    filepath = os.path.join(output_dir, filename)
    
    content = f"原始视频地址: {video_url}\n"
    content += f"视频ID: {video_id}\n"
    if title:
        content += f"视频标题: {title}\n"
    content += f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
    content += "=" * 50 + "\n\n"
    content += transcript
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return os.path.abspath(filepath)