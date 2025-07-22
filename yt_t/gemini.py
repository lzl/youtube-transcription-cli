import os
from typing import Optional, List
from google import genai
from google.genai import types
from .video_utils import get_video_info, should_split_video
from .audio_utils import download_audio, speed_up_audio, get_audio_duration, split_audio, cleanup_temp_files


def transcribe_audio_file(client: genai.Client, audio_path: str, segment_info: str = "") -> Optional[str]:
    """转录音频文件
    
    Args:
        client: Gemini API 客户端
        audio_path: 音频文件路径
        segment_info: 段落信息（用于提示）
    
    Returns:
        转录的字幕内容
    """
    model = "gemini-2.5-flash"
    
    prompt = f"""请提取音频的完整字幕内容{segment_info}。

输出格式要求：
[MM:SS] 字幕内容
[MM:SS] 下一句字幕

请确保：
1. 时间戳格式为 [MM:SS] 或 [HH:MM:SS]
2. 按时间顺序排列
3. 准确识别说话内容，包括标点符号"""

    # 上传音频文件
    try:
        # 直接使用文件路径上传
        audio_file = client.files.upload(file=audio_path)
        print(f"音频文件已上传: {audio_file.name}")
        
        contents = [
            types.Content(
                role="user",
                parts=[
                    types.Part(
                        file_data=types.FileData(
                            file_uri=audio_file.uri,
                            mime_type="audio/mpeg",
                        )
                    ),
                    types.Part.from_text(text=prompt),
                ],
            ),
        ]
        
        generate_content_config = types.GenerateContentConfig(
            response_mime_type="text/plain",
        )
        
        transcript = ""
        for chunk in client.models.generate_content_stream(
            model=model,
            contents=contents,
            config=generate_content_config,
        ):
            if chunk.text:
                transcript += chunk.text
        
        return transcript.strip()
        
    except Exception as e:
        print(f"转录音频失败: {str(e)}")
        return None


def transcribe_with_gemini(youtube_url: str) -> Optional[str]:
    """Transcribe YouTube video using Google Gemini API
    
    对于超过50分钟的视频，会下载音频并分段处理
    """
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY 环境变量未设置")
    
    # 获取视频信息
    print("正在获取视频信息...")
    video_info = get_video_info(youtube_url)
    if not video_info:
        print("无法获取视频信息，尝试直接转录...")
        return transcribe_youtube_direct(youtube_url)
    
    duration = video_info['duration']
    title = video_info['title']
    print(f"视频标题: {title}")
    print(f"视频时长: {format_time(duration)}")
    
    # 检查是否需要下载和分割
    if not should_split_video(duration):
        print("视频时长小于50分钟，直接转录...")
        return transcribe_youtube_direct(youtube_url)
    
    # 需要下载音频并处理
    print("\n视频超过50分钟，需要下载音频并处理...")
    
    temp_files = []  # 记录所有临时文件
    
    try:
        # 1. 下载音频
        audio_path = download_audio(youtube_url)
        if not audio_path:
            print("音频下载失败，尝试直接转录...")
            return transcribe_youtube_direct(youtube_url)
        temp_files.append(audio_path)
        
        # 2. 加速音频到2倍速
        speeded_audio_path = speed_up_audio(audio_path, speed=2.0)
        temp_files.append(speeded_audio_path)
        
        # 3. 检查加速后的音频时长
        speeded_duration = get_audio_duration(speeded_audio_path)
        print(f"\n加速后音频时长: {format_time(int(speeded_duration))}")
        
        # 4. 根据加速后的时长决定是否分割
        client = genai.Client(api_key=api_key)
        
        if speeded_duration <= 50 * 60:  # 50分钟
            print("加速后音频小于50分钟，直接转录...")
            transcript = transcribe_audio_file(client, speeded_audio_path)
            cleanup_temp_files(temp_files)
            return transcript
        else:
            # 需要分割音频
            print("加速后音频仍超过50分钟，需要分割...")
            audio_segments = split_audio(speeded_audio_path, segment_minutes=50)
            temp_files.extend(audio_segments)
            
            # 转录每个分段
            all_transcripts = []
            for i, segment_path in enumerate(audio_segments):
                print(f"\n正在转录第 {i+1}/{len(audio_segments)} 段...")
                segment_info = f"（第 {i+1} 段，共 {len(audio_segments)} 段）"
                segment_transcript = transcribe_audio_file(client, segment_path, segment_info)
                
                if segment_transcript:
                    all_transcripts.append(segment_transcript)
                    print(f"第 {i+1} 段转录完成")
                else:
                    print(f"第 {i+1} 段转录失败，跳过")
            
            # 合并所有段落
            if all_transcripts:
                print("\n正在合并所有转录结果...")
                transcript = merge_transcripts(all_transcripts)
                cleanup_temp_files(temp_files)
                return transcript
            else:
                print("所有段落转录失败")
                cleanup_temp_files(temp_files)
                return None
                
    except Exception as e:
        print(f"处理失败: {str(e)}")
        cleanup_temp_files(temp_files)
        return None


def transcribe_youtube_direct(youtube_url: str) -> Optional[str]:
    """直接转录YouTube视频（不下载）"""
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY 环境变量未设置")
    
    try:
        client = genai.Client(api_key=api_key)
        
        model = "gemini-2.5-flash"
        contents = [
            types.Content(
                role="user",
                parts=[
                    types.Part(
                        file_data=types.FileData(
                            file_uri=youtube_url,
                            mime_type="video/*",
                        )
                    ),
                    types.Part.from_text(
                        text="请提取视频的完整字幕内容。输出格式要求：\n\n[00:10] 字幕内容\n[00:15] 下一句字幕\n\n请确保时间戳格式为 [MM:SS]，并按时间顺序排列。"
                    ),
                ],
            ),
        ]
        
        generate_content_config = types.GenerateContentConfig(
            thinking_config=types.ThinkingConfig(
                thinking_budget=-1
            ),
            response_mime_type="text/plain",
        )
        
        print("正在使用 Gemini API 生成字幕...")
        transcript = ""
        for chunk in client.models.generate_content_stream(
            model=model,
            contents=contents,
            config=generate_content_config,
        ):
            if chunk.text:
                transcript += chunk.text
        
        return transcript.strip()
        
    except Exception as e:
        print(f"Gemini API 调用失败: {str(e)}")
        return None


def merge_transcripts(transcripts: List[str]) -> str:
    """合并多个转录片段
    
    Args:
        transcripts: 转录片段列表
    
    Returns:
        合并后的完整转录文本
    """
    # 合并时添加分段标记
    merged = []
    for i, transcript in enumerate(transcripts):
        if i > 0:
            merged.append(f"\n\n--- 第 {i+1} 段 ---\n")
        merged.append(transcript)
    
    return "\n".join(merged)


def format_time(seconds: int) -> str:
    """将秒数格式化为时间字符串"""
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    
    if hours > 0:
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    else:
        return f"{minutes:02d}:{seconds:02d}"