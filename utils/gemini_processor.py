from typing import List, Dict
import google.generativeai as genai

class GeminiProcessor:
    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-pro')

    def generate_article(self, video_data: List[Dict], language: str = 'ja') -> str:
        """Generate an article from multiple video sources in specified language."""
        # Prepare prompt with video information
        prompt = self._prepare_prompt(video_data, language)
        
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            raise Exception(f"Gemini AI error: {str(e)}")

    def _prepare_prompt(self, video_data: List[Dict], language: str) -> str:
        """Prepare prompt for Gemini AI with language specification."""
        language_prompt = {
            'ja': """以下のYouTube動画に基づいて包括的な記事を生成してください：

記事は以下の要件を満たす必要があります：
1. すべての動画の情報を統合する
2. 関連する引用と参照を含める
3. 明確な導入、本文、結論を持つ
4. 見出しと段落を使用して適切にフォーマットする
5. プロフェッショナルなトーンを維持する
6. 魅力的で有益な内容にする

すべての出力は日本語で生成してください。""",
            
            'en': """Generate a comprehensive article based on the following YouTube videos:

Please create a well-structured article that:
1. Synthesizes information from all videos
2. Includes relevant quotes and references
3. Has a clear introduction, body, and conclusion
4. Uses proper formatting with headers and paragraphs
5. Maintains a professional tone
6. Is engaging and informative

Generate all output in English."""
        }

        prompt = language_prompt[language] + "\n\n"
        
        for video in video_data:
            if 'error' not in video:
                prompt += f"Video Title: {video['title']}\n"
                prompt += f"Transcript: {video['transcript'][:1000]}...\n\n"
        
        return prompt
