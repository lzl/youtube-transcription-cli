import os
from typing import Optional
from google import genai
from google.genai import types


def transcribe_with_gemini(youtube_url: str) -> Optional[str]:
    """Transcribe YouTube video using Google Gemini API"""
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
                thinking_budget=-1,
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