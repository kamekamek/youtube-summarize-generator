from typing import Dict, List
import google.api_core.exceptions
from googleapiclient.discovery import build
from youtube_transcript_api import YouTubeTranscriptApi
import re

class YouTubeHandler:
    def __init__(self, api_key: str):
        self.youtube = build('youtube', 'v3', developerKey=api_key)

    def extract_video_id(self, url: str) -> str:
        """Extract video ID from YouTube URL."""
        patterns = [
            r'(?:v=|\/)([0-9A-Za-z_-]{11}).*',
            r'(?:youtu\.be\/)([0-9A-Za-z_-]{11})',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        raise ValueError("Invalid YouTube URL")

    def get_video_details(self, video_id: str) -> Dict:
        """Get video title and description."""
        try:
            response = self.youtube.videos().list(
                part='snippet',
                id=video_id
            ).execute()

            if not response['items']:
                raise ValueError("Video not found")

            snippet = response['items'][0]['snippet']
            return {
                'title': snippet['title'],
                'description': snippet['description']
            }
        except google.api_core.exceptions.Error as e:
            raise Exception(f"YouTube API error: {str(e)}")

    def get_transcript(self, video_id: str) -> str:
        """Get video transcript."""
        try:
            transcript_list = YouTubeTranscriptApi.get_transcript(video_id, languages=['en', 'ja', 'zh'])
            return " ".join([entry['text'] for entry in transcript_list])
        except Exception as e:
            raise Exception(f"Could not fetch transcript: {str(e)}")

    def get_recommendations(self, url: str, max_results: int = 5) -> List[Dict]:
        """Get video recommendations based on a video."""
        try:
            video_id = self.extract_video_id(url)
            response = self.youtube.search().list(
                part='snippet',
                relatedToVideoId=video_id,
                type='video',
                maxResults=max_results
            ).execute()

            recommendations = []
            for item in response.get('items', []):
                if item['id']['kind'] == 'youtube#video':
                    recommendations.append({
                        'id': item['id']['videoId'],
                        'title': item['snippet']['title'],
                        'thumbnail': item['snippet']['thumbnails']['default']['url']
                    })
            
            if not recommendations:
                raise Exception("No recommendations found")
                
            return recommendations
        except Exception as e:
            raise Exception(f"Error getting recommendations: {str(e)}")

    def process_videos(self, urls: List[str]) -> List[Dict]:
        """Process multiple YouTube videos."""
        results = []
        for url in urls:
            try:
                video_id = self.extract_video_id(url)
                details = self.get_video_details(video_id)
                transcript = self.get_transcript(video_id)
                
                results.append({
                    'url': url,
                    'video_id': video_id,
                    'title': details['title'],
                    'description': details['description'],
                    'transcript': transcript
                })
            except Exception as e:
                results.append({
                    'url': url,
                    'error': str(e)
                })
        return results
