from typing import List, Dict
import google.generativeai as genai

class GeminiProcessor:
    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-pro')

    def generate_article(self, video_data: List[Dict], language: str = 'ja', generate_summary: bool = False) -> str:
        """Generate an article from multiple video sources in specified language."""
        # Prepare prompt with video information
        prompt = self._prepare_prompt(video_data, language, generate_summary)
        
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            raise Exception(f"Gemini AI error: {str(e)}")

    def _prepare_prompt(self, video_data: List[Dict], language: str, generate_summary: bool) -> str:
        """Prepare prompt for Gemini AI with language specification."""
        language_prompt = {
            'ja': """以下のYouTube動画に基づいて{}を生成してください：

記事は以下の要件を満たす必要があります：
1. すべての動画の情報を統合する
2. 関連する引用と参照を含める
3. 明確な導入、本文、結論を持つ
4. 見出しと段落を使用して適切にフォーマットする
5. プロフェッショナルなトーンを維持する
6. 魅力的で有益な内容にする

すべての出力は日本語で生成してください。""",
            
            'en': """Generate a {} based on the following YouTube videos:

Please create a well-structured {} that:
1. Synthesizes information from all videos
2. Includes relevant quotes and references
3. Has a clear introduction, body, and conclusion
4. Uses proper formatting with headers and paragraphs
5. Maintains a professional tone
6. Is engaging and informative

Generate all output in English.""",

            'zh': """根据以下YouTube视频生成{}：

请创建一个结构完善的{}，要求：
1. 综合所有视频的信息
2. 包含相关引用和参考
3. 有清晰的引言、正文和结论
4. 使用适当的标题和段落格式
5. 保持专业的语气
6. 内容引人入胜且富有信息价值

所有输出均使用中文生成。"""
        }

        content_type = "summary" if generate_summary else "comprehensive article"
        prompt = language_prompt[language].format(
            "要約" if language == 'ja' and generate_summary else "包括的な記事" if language == 'ja' else
            "摘要" if language == 'zh' and generate_summary else "综合文章" if language == 'zh' else
            content_type
        ) + "\n\n"
        
        for video in video_data:
            if 'error' not in video:
                prompt += f"Video Title: {video['title']}\n"
                prompt += f"Transcript: {video['transcript'][:1000]}...\n\n"
        
        return prompt
