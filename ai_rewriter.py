"""
AI Rewriter Module
Uses OpenAI GPT models to rewrite text in audiobook narration style
"""

import os
from openai import OpenAI
import streamlit as st
from typing import Optional


class AIRewriter:
    """Rewrite text using OpenAI GPT models for audiobook narration"""
    
    def __init__(self, api_key: str, model: str = "gpt-4o-mini"):
        """
        Initialize AI Rewriter
        
        Args:
            api_key: OpenAI API key
            model: Model to use (gpt-4o-mini, gpt-4-turbo, etc.)
        """
        self.client = OpenAI(api_key=api_key)
        self.model = model
    
    def rewrite_text(self, text: str, creativity: float = 0.7, style: str = "storytelling") -> str:
        """
        Rewrite text in audiobook narration style
        
        Args:
            text: Original text to rewrite
            creativity: Temperature setting (0.0 to 1.0)
            style: Narration style (storytelling, professional, casual)
            
        Returns:
            str: Rewritten text
        """
        try:
            # Define prompts based on style
            style_prompts = {
                "storytelling": "Rewrite the following text in a natural, engaging storytelling narration style suitable for an audiobook. Make it flow smoothly and sound conversational while maintaining the original meaning and key information.",
                "professional": "Rewrite the following text in a clear, professional narration style suitable for an educational or business audiobook. Keep it formal but accessible.",
                "casual": "Rewrite the following text in a friendly, casual conversational style suitable for an audiobook. Make it sound like a friend telling a story."
            }
            
            prompt = style_prompts.get(style, style_prompts["storytelling"])
            
            # Make API call
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert audiobook narrator and editor. Your task is to rewrite text to make it perfect for audio narration."
                    },
                    {
                        "role": "user",
                        "content": f"{prompt}\n\nText to rewrite:\n{text}"
                    }
                ],
                temperature=creativity,
                max_tokens=4000
            )
            
            rewritten_text = response.choices[0].message.content
            return rewritten_text.strip()
        
        except Exception as e:
            raise Exception(f"Error rewriting text with AI: {str(e)}")
    
    def rewrite_chunks(self, chunks: list, creativity: float = 0.7, 
                      style: str = "storytelling", progress_callback=None) -> str:
        """
        Rewrite multiple text chunks and combine them
        
        Args:
            chunks: List of text chunks
            creativity: Temperature setting
            style: Narration style
            progress_callback: Optional callback function for progress updates
            
        Returns:
            str: Combined rewritten text
        """
        rewritten_chunks = []
        total_chunks = len(chunks)
        
        for idx, chunk in enumerate(chunks):
            if progress_callback:
                progress_callback(idx + 1, total_chunks)
            
            rewritten = self.rewrite_text(chunk, creativity, style)
            rewritten_chunks.append(rewritten)
        
        return " ".join(rewritten_chunks)
    
    @staticmethod
    def validate_api_key(api_key: str) -> bool:
        """
        Validate OpenAI API key
        
        Args:
            api_key: API key to validate
            
        Returns:
            bool: True if valid, False otherwise
        """
        try:
            client = OpenAI(api_key=api_key)
            # Make a minimal API call to test
            client.models.list()
            return True
        except Exception as e:
            return False
