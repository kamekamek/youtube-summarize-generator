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
            # Add specific language instruction to the model
            response = self.model.generate_content(
                prompt,
                generation_config={
                    'temperature': 0.7,
                    'top_p': 0.8,
                    'top_k': 40,
                }
            )
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

            'zh': """请根据以下YouTube视频内容生成一个全面而简洁的中文摘要。

摘要必须满足以下要求：
1. 提炼并整合所有视频中的核心观点
2. 准确引用关键内容和重要参考信息
3. 采用清晰的层次结构组织内容
4. 使用准确、简洁的中文表达
5. 保持专业的写作风格
6. 突出重点信息，避免冗余
7. 确保行文流畅，逻辑清晰

重要说明：
- 请使用标准中文（简体）
- 保持专业性和可读性的平衡
- 确保语言表达地道自然

请用中文生成所有内容。如果视频包含专业术语，请确保使用准确的中文术语对应。"""
        }

        # Add language-specific preprocessing instructions
        prompt = f"Target Language: {language}\n\n"
        prompt += language_prompt[language] + "\n\n"
        
        for video in video_data:
            if 'error' not in video:
                prompt += f"视频标题" if language == 'zh' else "Video Title"
                prompt += f": {video['title']}\n"
                # Limit transcript length but ensure we don't cut in the middle of a sentence
                transcript = video['transcript'][:2000].rsplit('.', 1)[0] + '...'
                prompt += f"内容记录" if language == 'zh' else "Transcript"
                prompt += f": {transcript}\n\n"
        
        return prompt
