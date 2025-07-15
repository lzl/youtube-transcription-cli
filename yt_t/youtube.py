from typing import Optional, List, Dict
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter
import re
from urllib.parse import urlparse, parse_qs


def extract_video_id(url: str) -> Optional[str]:
    """Extract video ID from YouTube URL"""
    patterns = [
        r'(?:v=|\/)([0-9A-Za-z_-]{11}).*',
        r'(?:embed\/)([0-9A-Za-z_-]{11})',
        r'(?:watch\?v=)([0-9A-Za-z_-]{11})',
        r'youtu\.be\/([0-9A-Za-z_-]{11})'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    
    parsed = urlparse(url)
    if parsed.hostname in ['www.youtube.com', 'youtube.com']:
        query = parse_qs(parsed.query)
        if 'v' in query:
            return query['v'][0]
    
    return None


def get_native_subtitles(video_id: str) -> Optional[str]:
    """Get native subtitles from YouTube with language priority"""
    # 语言优先级：英文 -> 中文 -> 其他可用语言
    preferred_languages = ['en', 'zh-CN', 'zh', 'zh-Hans', 'zh-Hant']
    
    try:
        # 获取所有可用字幕
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
        available_transcripts = {}
        
        # 收集所有可用的字幕语言
        for transcript in transcript_list:
            available_transcripts[transcript.language_code] = transcript
            print(f"发现字幕语言: {transcript.language_code} ({transcript.language})")
        
        # 按优先级尝试获取字幕
        selected_transcript = None
        selected_language = None
        
        for lang in preferred_languages:
            if lang in available_transcripts:
                selected_transcript = available_transcripts[lang]
                selected_language = lang
                print(f"选择字幕语言: {lang}")
                break
        
        # 如果优先语言都没有，选择第一个可用的
        if not selected_transcript and available_transcripts:
            first_lang = list(available_transcripts.keys())[0]
            selected_transcript = available_transcripts[first_lang]
            selected_language = first_lang
            print(f"使用可用字幕语言: {first_lang}")
        
        if not selected_transcript:
            print("未找到任何可用字幕")
            return None
        
        # 获取字幕内容
        transcript_data = selected_transcript.fetch()
        
        formatted_transcript = []
        for entry in transcript_data:
            start_time = int(entry.start)
            minutes = start_time // 60
            seconds = start_time % 60
            timestamp = f"[{minutes:02d}:{seconds:02d}]"
            text = entry.text.replace('\n', ' ')
            formatted_transcript.append(f"{timestamp} {text}")
        
        return '\n'.join(formatted_transcript)
        
    except Exception as e:
        print(f"无法获取原生字幕: {str(e)}")
        return None


def get_available_languages(video_id: str) -> List[Dict]:
    """Get available subtitle languages for a video"""
    try:
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
        languages = []
        for transcript in transcript_list:
            languages.append({
                'code': transcript.language_code,
                'name': transcript.language,
                'is_generated': transcript.is_generated,
                'is_translatable': transcript.is_translatable
            })
        return languages
    except:
        return []