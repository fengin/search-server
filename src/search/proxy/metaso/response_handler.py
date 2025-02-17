"""
秘塔AI响应数据处理器

作者: 凌封（微信：fengin）
网站: AI全书（https://aibook.ren）
"""

import json
import re
from typing import Dict, List, Optional

class MetasoResponseHandler:
    """秘塔AI响应数据处理器"""
    
    def __init__(self):
        """初始化处理器"""
        self._references: List = []  # 引用列表
        self._images: List = []  # 图片列表
        self._markdown_images: List = []  # markdown中的图片
        self._recommended_questions: List = []  # 推荐问题
        self._highlights: List = [] # 高亮列表
        self._tables: List = [] # 表格数据
        self._query_info: Dict = {} # 查询信息
        self._content_parts: List = [] # 有序内容片段
        
    def _extract_markdown_image(self, text: str) -> List[Dict]:
        """从markdown文本中提取图片信息
        
        Args:
            text: markdown文本
            
        Returns:
            List[Dict]: 图片信息列表
        """
        images = []
        # 匹配markdown图片语法 ![alt](url)
        pattern = r'!\[(.*?)\]\((.*?)\)'
        matches = re.finditer(pattern, text)
        
        for match in matches:
            alt_text = match.group(1)
            url = match.group(2)
            images.append({
                "name": alt_text,
                "thumbnail_url": url,
                "caption": alt_text,
                "source": None,
                "width": None,
                "height": None
            })
            
        return images
        
    def _is_encoded_content(self, text: str) -> bool:
        """检查文本是否为编码内容
        
        Args:
            text: 要检查的文本
            
        Returns:
            bool: 是否为编码内容
        """
        if not text:
            return False
        
        # 检查长度是否异常（超过200字符可能是编码内容）
        if len(text) > 200:
            return True
        
        # 检查是否包含大量特殊字符
        special_chars = set('+/=')
        special_char_count = sum(1 for c in text if c in special_chars)
        if special_char_count > len(text) * 0.1:  # 如果特殊字符占比超过10%
            return True
        
        # 检查是否全是ASCII字符
        if all(ord(c) < 128 for c in text):
            # 检查是否包含过多的随机字符
            import string
            random_chars = set(string.ascii_letters + string.digits + '+/=')
            random_char_count = sum(1 for c in text if c in random_chars)
            if random_char_count > len(text) * 0.9:  # 如果随机字符占比超过90%
                return True
            
        return False

    def clean_response(self, text: str) -> str:
        """清理和处理响应数据"""
        try:
            if text.startswith("data:"):
                text = text[5:]
            text = text.strip()
            
            if not text or text == "[DONE]":
                return ""
            
            try:
                data = json.loads(text)
                data_type = data.get("type")
                
                if data_type == "query":
                    self._query_info = {
                        "real_question": data.get("realQuestion"),
                        "suggestions": data.get("data", []),
                        "debug_id": data.get("debugId"),
                        "query_id": data.get("id"),
                        "label": data.get("label", "")
                    }
                    
                elif data_type == "append-text":
                    text = data.get("text", "")
                    if text and not text.isspace():
                        self._content_parts.append(text)
                        # 提取图片信息但不修改原文
                        markdown_images = self._extract_markdown_image(text)
                        if markdown_images:
                            self._markdown_images.extend(markdown_images)
                            self._images.extend(markdown_images)
                        return text
                        
                elif data_type == "set-reference":
                    self._references = []
                    for ref in data.get("list", []):
                        ref_data = {
                            "id": ref.get("id"),
                            "display_id": ref.get("display", {}).get("refer_id"),
                            "title": ref.get("title"),
                            "link": ref.get("link"),
                            "source": ref.get("displaySource"),
                            "date": ref.get("date"),
                            "author": ref.get("author"),
                            "article_type": ref.get("article_type"),
                            "abstract": ref.get("abstract"),
                            "scholar": ref.get("scholar", False),
                            "publish_date": ref.get("publish_date"),
                            "export": ref.get("export"),
                            "matched_snippet": None,
                            "file_meta": {
                                "file_path": ref.get("file_meta", {}).get("file_path"),
                                "source": ref.get("file_meta", {}).get("source"),
                                "url": ref.get("file_meta", {}).get("url"),
                                "type": ref.get("file_meta", {}).get("type")
                            } if ref.get("file_meta") else None
                        }
                        self._references.append(ref_data)
                        
                elif data_type == "img-meta":
                    for img in data.get("list", []):
                        caption = img.get("caption", "")
                        # 检查caption是否为编码内容
                        if self._is_encoded_content(caption):
                            caption = ""
                        
                        img_data = {
                            "name": img.get("name"),
                            "url": img.get("contentUrl"),
                            "thumbnail_url": img.get("thumbnailUrl"),
                            "width": img.get("width"),
                            "height": img.get("height"),
                            "caption": caption,  # 使用处理后的caption
                            "source": img.get("hostPageDisplayUrl"),
                            "rerank_score": img.get("rerank_score"),
                            "dedup_hash": img.get("dedup_hash"),
                            "blur": img.get("blur"),
                            "format": img.get("endoingFormat"),
                            "aes_score": img.get("aes"),
                            "image_id": img.get("image_id")
                        }
                        self._images.append(img_data)
                        
                elif data_type == "recommended-question":
                    if "data" in data:
                        self._recommended_questions.extend(data["data"])
                        
                elif data_type == "answer-link-num-highlights":
                    if "data" in data:
                        self._highlights.extend(data["data"])
                        
                elif data_type == "update-reference":
                    for update in data.get("list", []):
                        ref_id = update.get("id")
                        for ref in self._references:
                            if ref["id"] == ref_id:
                                ref["matched_snippet"] = update.get("matched_snippet")
                                
                elif data_type == "heartbeat":
                    return ""
                    
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON: {e}")
                print(f"Problematic text: {text}")
                return ""
            
            return ""
            
        except Exception as e:
            print(f"Error in clean_response: {e}")
            print(f"Full input text: {text}")
            return ""
        
    def format_markdown(self, data: Dict) -> str:
        """格式化markdown输出"""
        # 直接拼接content_parts，保持原有格式
        content = "".join(self._content_parts)
        
        # 处理引用标记
        for ref in self._references:
            ref_id = ref.get("display_id")
            if ref_id:
                # 使用更精确的正则表达式
                pattern = r'\[\[' + re.escape(str(ref_id)) + r'\]\]'
                content = re.sub(pattern, f"[{ref_id}]", content)
        
        # 添加额外图片
        if self._images:
            extra_images = [img for img in self._images 
                           if img not in self._markdown_images]
            if extra_images:
                content += "\n\n**相关图片:**\n"
                for img in extra_images:
                    if img.get("name") and img.get("thumbnail_url"):
                        caption = img.get("caption", img["name"])
                        content += f"![{caption}]({img['thumbnail_url']})\n"
        
        return content.strip()
        
    def get_references_markdown(self) -> str:
        """获取参考文献的markdown格式
        
        Returns:
            str: 参考文献的markdown文本
        """
        if not self._references:
            return ""
        
        content = "**参考文献:**\n"
        for ref in self._references:
            ref_id = ref.get("display_id")
            title = ref.get("title", "")
            link = ref.get("link", "")
            source = ref.get("source", "")
            date = ref.get("date", "")
            
            ref_text = f"{ref_id}. "
            if link:
                ref_text += f"[{title}]({link})"
            else:
                ref_text += title
            if source:
                ref_text += f" - {source}"
            if date:
                ref_text += f" ({date})"
            content += ref_text + "\n"
        
        return content
        
    def _format_table(self, table_data: Dict) -> str:
        """格式化表格数据为markdown格式"""
        if not table_data:
            return ""
            
        # 实现表格转markdown的逻辑
        # ...
        return ""
        
    @property 
    def content(self) -> str:
        """获取完整内容"""
        return "".join(self._content_parts)
        
    @property
    def references(self) -> List:
        """获取引用列表"""
        return self._references
        
    @property
    def images(self) -> List:
        """获取图片列表"""
        return self._images
        
    @property
    def tables(self) -> List:
        """获取表格列表"""
        return self._tables
        
    @property
    def query_info(self) -> Dict:
        """获取查询信息"""
        return self._query_info
        
    @property
    def recommended_questions(self) -> List:
        """获取推荐问题列表"""
        return self._recommended_questions
        
    @property
    def highlights(self) -> List:
        """获取高亮列表"""
        return self._highlights 