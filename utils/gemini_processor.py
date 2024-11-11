from typing import List, Dict
import google.generativeai as genai

class GeminiProcessor:
    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-pro')

    def generate_article(self, video_data: List[Dict]) -> str:
        """Generate an article from multiple video sources."""
        # Prepare prompt with video information
        prompt = self._prepare_prompt(video_data)
        
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            raise Exception(f"Gemini AI error: {str(e)}")

    def _prepare_prompt(self, video_data: List[Dict]) -> str:
        """Prepare prompt for Gemini AI."""
        prompt = "Generate a comprehensive article based on the following YouTube videos:\n\n"
        
        for video in video_data:
            if 'error' not in video:
                prompt += f"Video Title: {video['title']}\n"
                prompt += f"Transcript: {video['transcript'][:1000]}...\n\n"
        
        prompt += """
        Please create a well-structured article that:
        1. Synthesizes information from all videos
        2. Includes relevant quotes and references
        3. Has a clear introduction, body, and conclusion
        4. Uses proper formatting with headers and paragraphs
        5. Maintains a professional tone
        6. Is engaging and informative
        """
        
        return prompt
