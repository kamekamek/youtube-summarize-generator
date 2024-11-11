from typing import List, Dict
import google.generativeai as genai

class GeminiProcessor:
    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-pro')

    def generate_article(self, video_data: List[Dict], language: str = 'ja') -> str:
        """Generate a summary from multiple video sources in specified language."""
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
            'ja': """以下のYouTube動画に基づいて簡潔な要約を生成してください：

要約は以下の要件を満たす必要があります：
1. すべての動画の重要なポイントを統合する
2. 主要な引用と参照を含める
3. 明確な構造で整理する
4. 簡潔で分かりやすい文章にする
5. プロフェッショナルなトーンを維持する
6. 重要な情報に焦点を当てる

すべての出力は日本語で生成してください。""",
            
            'en': """Generate a concise summary based on the following YouTube videos:

Please create a well-structured summary that:
1. Integrates key points from all videos
2. Includes essential quotes and references
3. Is organized with clear structure
4. Uses concise and clear language
5. Maintains a professional tone
6. Focuses on important information

Generate all output in English.""",

            'zh': """根据以下YouTube视频生成简明扼要的摘要：

请创建一个结构完善的摘要，要求：
1. 整合所有视频的重点信息
2. 包含重要引用和参考
3. 结构清晰有序
4. 使用简洁明了的语言
5. 保持专业的语气
6. 突出重要信息

所有输出均使用中文生成。"""
        }

        prompt = language_prompt[language] + "\n\n"
        
        for video in video_data:
            if 'error' not in video:
                prompt += f"Video Title: {video['title']}\n"
                prompt += f"Transcript: {video['transcript'][:1000]}...\n\n"
        
        return prompt
