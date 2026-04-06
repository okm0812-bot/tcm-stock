# -*- coding: utf-8 -*-
"""
YouTube 字幕抓取
"""
from youtube_transcript_api import YouTubeTranscriptApi

video_id = "EaN5QwdWgLw"

print(f"\n[YouTube Transcript] {video_id}\n")
print("="*60)

try:
    api = YouTubeTranscriptApi()
    result = api.fetch(video_id)
    
    print(f"取得成功！共 {len(result)} 段\n")
    
    # 合併所有文字
    full_text = ""
    for item in result:
        full_text += item['text'] + " "
    
    # 顯示前 3000 字
    print("字幕內容 (前3000字):")
    print("-"*60)
    print(full_text[:3000])
    print("\n...")
    print(f"\n[總字數: {len(full_text)} 字]")
    
except Exception as e:
    print(f"Error: {e}")
    
    # 嘗試 list
    try:
        transcripts = api.list(video_id)
        print(f"\nAvailable: {transcripts}")
    except:
        pass

print("\n" + "="*60)
