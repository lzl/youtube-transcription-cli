# YouTube Transcription CLI Tool - Product Requirements Document

## 1. Product Overview

### 1.1 Product Name
YouTube Transcription CLI (yt-t)

### 1.2 Product Goal
Develop a command-line tool to quickly extract transcriptions from YouTube videos and save them as formatted text files.

### 1.3 Target Users
Developers, content creators, researchers, and anyone who needs to extract text from YouTube videos.

## 2. Functional Requirements

### 2.1 Core Features

#### 2.1.1 Command Line Interface
- **Command**: `yt-t`
- **Parameter**: YouTube video URL
- **Usage Example**: `yt-t https://www.youtube.com/watch?v=pyRcHZWqIhw`

#### 2.1.2 Transcription Retrieval Logic

**Priority 1: Native YouTube Subtitles**
- First attempt to retrieve native subtitles/captions from YouTube
- Support multiple languages (prioritize user's system language or English)

**Priority 2: Google Gemini API Generation**
- When video lacks native subtitles, use Google Gemini API for transcription
- Model: `gemini-2.5-flash`
- API Method: Pass YouTube video URL as file_data to the API

#### 2.1.3 Output Format
- File Format: `.txt`
- File Naming: `{video_title}_transcript_{timestamp}.txt` or `youtube_transcript_{video_id}.txt`
- Storage Location: Current working directory
- Content Format:
  ```
  [00:01] Hello world
  [00:05] This is the second sentence
  [00:10] Continuing with more content
  ```

### 2.2 Technical Implementation Requirements

#### 2.2.1 Programming Language
- Python 3.8+

#### 2.2.2 Dependencies
- `google-genai`: Google Gemini API client
- `youtube-transcript-api` or similar: Retrieve native YouTube subtitles
- `click` or `argparse`: Command-line argument parsing
- `requests`: HTTP request handling

#### 2.2.3 API Configuration
- Required environment variable: `GEMINI_API_KEY`
- Provide friendly error messages when API key is missing

### 2.3 Gemini API Call Example

```python
import os
from google import genai
from google.genai import types

def transcribe_with_gemini(youtube_url):
    client = genai.Client(
        api_key=os.environ.get("GEMINI_API_KEY"),
    )
    
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
                    text="Extract the transcription from the video. Output format:\n\n[00:10] Subtitle content here"
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
    
    transcript = ""
    for chunk in client.models.generate_content_stream(
        model=model,
        contents=contents,
        config=generate_content_config,
    ):
        transcript += chunk.text
    
    return transcript
```

## 3. Implementation Steps

### 3.1 Project Structure
```
youtube-transcription-cli/
├── yt_t/
│   ├── __init__.py
│   ├── cli.py          # CLI entry point
│   ├── youtube.py      # YouTube subtitle retrieval logic
│   ├── gemini.py       # Gemini API call logic
│   └── utils.py        # Utility functions
├── setup.py
├── requirements.txt
└── README.md
```

### 3.2 Core Workflow
1. Parse command-line arguments to get YouTube URL
2. Validate URL format
3. Extract video ID and title
4. Attempt to retrieve native YouTube subtitles
5. If failed, check if GEMINI_API_KEY exists
6. Call Gemini API for transcription
7. Format output content
8. Save to text file
9. Display success message and file path

### 3.3 Error Handling
- Invalid YouTube URL
- Network connection errors
- Missing or invalid API key
- API rate limits
- Video too long or inaccessible

### 3.4 Performance Optimization
- Implement progress bar for transcription progress
- Support resume capability for long videos
- Cache transcribed videos

## 4. Optional Features

- Batch processing of multiple URLs
- Support different output formats (SRT, VTT, etc.)
- Specify output directory
- Language selection for subtitles
- Video segment transcription (specify time range)

## 5. Success Criteria

- Successfully retrieve native subtitles from YouTube videos with captions
- Successfully transcribe videos without captions using Gemini API
- Output format meets requirements
- Comprehensive error handling with good user experience