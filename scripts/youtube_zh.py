# -*- coding: utf-8 -*-
"""
YouTube 字幕抓取 - 繁體中文
"""
from youtube_transcript_api import YouTubeTranscriptApi

video_id = "EaN5QwdWgLw"

print(f"\n[YouTube Transcript] {video_id}\n")
print("="*60)

api = YouTubeTranscriptApi()

# 用正確的方法
try:
    # 先列出可用字幕
    transcript_list = api.list(video_id)
    print(f"可用字幕: {transcript_list}")
    
    # 取得繁體中文
    transcript = transcript_list.find_transcript(['zh-TW'])
    result = transcript.fetch()
    
    print(f"\n取得成功！共 {len(result)} 段\n")
    
    # 合併所有文字
    full_text = ""
    for item in result:
        full_text += item['text'] + " "
    
    # 顯示前 3000 字
    print("="*60)
    print("字幕內容 (前3000字):")
    print("="*60)
    print(full_text[:3000])
    print("\n...")
    print(f"\n[總字數: {len(full_text)} 字]")
    
except Exception as e:
    print(f"Error: {e}")
    
    # 嘗試翻譯成英文
    try:
        print("\n嘗試取得並翻譯...")
        transcript = transcript_list.find_transcript(['zh-TW'])
        translated = transcript.translate('en')
        result2 = translated.fetch()
        
        full_text = ""
        for item in result2:
            full_text += item['text'] + " "
        
        print("翻譯結果:")
        print(full_text[:3000])
        
    except Exception as e2:
        print(f"翻譯也失敗: {e2}")

print("\n" + "="*60)
