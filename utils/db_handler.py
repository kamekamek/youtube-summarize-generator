from datetime import datetime
import os
from postgrest import AsyncPostgrestClient
import asyncio
from typing import List, Optional
import urllib.parse
from functools import wraps

class VideoSummary:
    def __init__(self, id: int, video_id: str, title: str, summary: str, 
                 language: str, timestamp: datetime, source_urls: str):
        self.id = id
        self.video_id = video_id
        self.title = title
        self.summary = summary
        self.language = language
        self.timestamp = timestamp
        self.source_urls = source_urls

def ensure_event_loop():
    """Ensure there's an event loop set for the current thread."""
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    return loop

class DatabaseHandler:
    def __init__(self):
        try:
            # Parse Supabase URL and auth key
            supabase_url = os.environ.get('SUPABASE_URL')
            supabase_key = os.environ.get('SUPABASE_KEY')
            
            if not supabase_url or not supabase_key:
                raise ValueError("Supabase credentials not found in environment variables")
            
            # Extract the host and construct REST URL
            parsed_url = urllib.parse.urlparse(supabase_url)
            rest_url = f"{parsed_url.scheme}://{parsed_url.netloc}/rest/v1"
            
            # Initialize Postgrest client
            self.client = AsyncPostgrestClient(
                base_url=rest_url,
                headers={
                    "apikey": supabase_key,
                    "Authorization": f"Bearer {supabase_key}"
                }
            )
            
            # Test connection
            loop = ensure_event_loop()
            loop.run_until_complete(self._verify_connection())
            
        except Exception as e:
            raise Exception(f"Failed to initialize database connection: {str(e)}")

    async def _verify_connection(self) -> bool:
        """Verify database connection is active."""
        try:
            await self.client.from_("video_summaries").select("id").limit(1).execute()
            return True
        except Exception as e:
            print(f"Connection verification failed: {str(e)}")
            return False

    def verify_connection(self) -> bool:
        """Synchronous wrapper for connection verification."""
        loop = ensure_event_loop()
        return loop.run_until_complete(self._verify_connection())

    async def _save_summary(self, video_id: str, title: str, summary: str, 
                          language: str, source_urls: str) -> bool:
        """Async method to save a video summary."""
        try:
            data = {
                "video_id": video_id,
                "title": title,
                "summary": summary,
                "language": language,
                "source_urls": source_urls,
                "timestamp": datetime.utcnow().isoformat()
            }
            await self.client.from_("video_summaries").insert(data).execute()
            return True
        except Exception as e:
            raise Exception(f"Database error: {str(e)}")

    def save_summary(self, video_id: str, title: str, summary: str, 
                    language: str, source_urls: str) -> bool:
        """Save a video summary to the database."""
        if not self.verify_connection():
            raise Exception("Database connection is not active")
        
        loop = ensure_event_loop()
        return loop.run_until_complete(
            self._save_summary(video_id, title, summary, language, source_urls)
        )

    async def _get_recent_summaries(self, limit: int = 5) -> List[VideoSummary]:
        """Async method to get recent summaries."""
        try:
            response = await self.client.from_("video_summaries")\
                .select("*")\
                .order("timestamp", desc=True)\
                .limit(limit)\
                .execute()
            
            return [
                VideoSummary(
                    id=item['id'],
                    video_id=item['video_id'],
                    title=item['title'],
                    summary=item['summary'],
                    language=item['language'],
                    timestamp=datetime.fromisoformat(item['timestamp']),
                    source_urls=item['source_urls']
                )
                for item in response.data
            ] if response.data else []
        except Exception as e:
            print(f"Error fetching recent summaries: {str(e)}")
            return []

    def get_recent_summaries(self, limit: int = 5) -> List[VideoSummary]:
        """Get recent summaries from the database."""
        try:
            if not self.verify_connection():
                return []
            
            loop = ensure_event_loop()
            return loop.run_until_complete(self._get_recent_summaries(limit))
        except Exception:
            return []

    async def _get_summaries_by_language(self, language: str, 
                                       limit: int = 5) -> List[VideoSummary]:
        """Async method to get summaries by language."""
        try:
            response = await self.client.from_("video_summaries")\
                .select("*")\
                .eq("language", language)\
                .order("timestamp", desc=True)\
                .limit(limit)\
                .execute()
            
            return [
                VideoSummary(
                    id=item['id'],
                    video_id=item['video_id'],
                    title=item['title'],
                    summary=item['summary'],
                    language=item['language'],
                    timestamp=datetime.fromisoformat(item['timestamp']),
                    source_urls=item['source_urls']
                )
                for item in response.data
            ] if response.data else []
        except Exception as e:
            print(f"Error fetching summaries by language: {str(e)}")
            return []

    def get_summaries_by_language(self, language: str, 
                                limit: int = 5) -> List[VideoSummary]:
        """Get summaries filtered by language."""
        try:
            if not self.verify_connection():
                return []
            
            loop = ensure_event_loop()
            return loop.run_until_complete(
                self._get_summaries_by_language(language, limit)
            )
        except Exception:
            return []

    def __del__(self):
        """Cleanup."""
        pass  # No cleanup needed for REST client
