# -*- coding: utf-8 -*-
"""
YouTube 字幕
"""
import sys

try:
    from youtube_transcript_api import YouTubeTranscriptApi
    print("youtube_transcript_api imported successfully")
    print(f"Module: {YouTubeTranscriptApi}")
    print(f"Methods: {dir(YouTubeTranscriptApi)}")
except Exception as e:
    print(f"Import error: {e}")
