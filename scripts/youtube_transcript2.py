# -*- coding: utf-8 -*-
"""
YouTube 字幕抓取
"""
from youtube_transcript_api import YouTubeTranscriptApi

video_id = "Ea5QwdWgLw"

print(f"\n[YouTube Transcript] {video_id}\n")
print("="*60)

try:
    # 用 fetch 方法
    api = YouTubeTranscriptApi()
    result = api.fetch(video_id)
    
    print(f"Result type: {type(result)}")
    print(f"Result: {result}")
    
except Exception as e:
    print(f"Error with fetch: {e}")

print("\n" + "="*60)

# 嘗試 list
try:
    api2 = YouTubeTranscriptApi()
    transcripts = api2.list(video_id)
    print(f"Available transcripts: {transcripts}")
    
except Exception as e:
    print(f"Error with list: {e}")
