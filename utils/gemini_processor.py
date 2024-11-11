from typing import List, Dict
import google.generativeai as genai
import re

class GeminiProcessor:
    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-pro')

    def generate_article(self, video_data: List[Dict], language: str = 'ja') -> str:
        """Generate a summary from multiple video sources in specified language."""
        prompt = self._prepare_prompt(video_data, language)
        
        try:
            # Configure generation parameters based on language
            temperature = 0.9 if language == 'zh' else 0.7  # Higher temperature for more natural Chinese
            response = self.model.generate_content(
                prompt,
                generation_config={
                    'temperature': temperature,
                    'top_p': 0.95,  # Increased for more diverse Chinese expressions
                    'top_k': 40,
                    'candidate_count': 1,
                }
            )
            return response.text
        except Exception as e:
            raise Exception(f"Gemini AI error: {str(e)}")

    def _preprocess_chinese_text(self, text: str) -> str:
        """Preprocess Chinese text to handle encoding and segmentation properly."""
        # Remove extra whitespace between Chinese characters
        text = re.sub(r'([^\x00-\xff])\s+([^\x00-\xff])', r'\1\2', text)
        # Ensure proper sentence breaks at Chinese punctuation
        text = re.sub(r'([。！？；])\s*', r'\1\n', text)
        return text

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
            
            'zh': """【输出要求】
使用简体中文生成视频内容摘要。

【摘要结构】
1. 核心要点
- 提取视频的主要观点
- 突出关键信息
- 保持逻辑连贯

2. 表达方式
- 使用规范的简体中文
- 保持专业性
- 确保表达自然流畅

3. 专业术语
- 使用准确的中文术语
- 必要时保留英文原文

【重要提示】
• 确保中文表达地道自然
• 避免生硬的翻译腔
• 保持专业性的同时确保可读性"""
        }

        # Start with explicit language instruction
        prompt = f"Output Language: {language}\n"
        if language == 'zh':
            prompt += "请使用标准简体中文输出所有内容。确保使用地道的中文表达。\n\n"
        prompt += language_prompt[language] + "\n\n"
        
        # Process video data
        for video in video_data:
            if 'error' not in video:
                # Use Chinese labels for Chinese output
                title_label = "标题：" if language == 'zh' else "Title: "
                content_label = "内容：" if language == 'zh' else "Content: "
                
                prompt += f"{title_label}{video['title']}\n"
                
                # Preprocess transcript for Chinese content
                transcript = video['transcript']
                if language == 'zh':
                    # Limit transcript length at character boundaries
                    if len(transcript) > 2000:
                        transcript = transcript[:2000]
                        # Find last complete Chinese sentence
                        last_period = max(transcript.rfind('。'), transcript.rfind('！'), transcript.rfind('？'))
                        if last_period > 0:
                            transcript = transcript[:last_period + 1]
                    transcript = self._preprocess_chinese_text(transcript)
                else:
                    # For non-Chinese content, use simple truncation
                    transcript = transcript[:2000].rsplit('.', 1)[0] + '...'
                
                prompt += f"{content_label}{transcript}\n\n"
        
        return prompt
