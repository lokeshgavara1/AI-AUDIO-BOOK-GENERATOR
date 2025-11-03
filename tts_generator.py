"""
Text-to-Speech Generator Module
Supports multiple TTS engines: OpenAI TTS, gTTS, and pyttsx3
"""

import os
import tempfile
from pathlib import Path
from gtts import gTTS
import pyttsx3
from openai import OpenAI
import streamlit as st
from typing import Optional, Literal


class TTSGenerator:
    """Generate speech from text using various TTS engines"""
    
    @staticmethod
    def generate_with_openai(text: str, api_key: str, voice: str = "alloy", 
                            speed: float = 1.0, output_path: Optional[str] = None) -> str:
        """
        Generate speech using OpenAI TTS API
        
        Args:
            text: Text to convert to speech
            api_key: OpenAI API key
            voice: Voice to use (alloy, echo, fable, onyx, nova, shimmer)
            speed: Speed of speech (0.25 to 4.0)
            output_path: Optional output file path
            
        Returns:
            str: Path to generated audio file
        """
        try:
            client = OpenAI(api_key=api_key)
            
            # Create temp file if no output path specified
            if output_path is None:
                temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3')
                output_path = temp_file.name
                temp_file.close()
            
            # Generate speech
            response = client.audio.speech.create(
                model="tts-1",
                voice=voice,
                input=text,
                speed=speed
            )
            
            # Save to file
            response.stream_to_file(output_path)
            
            return output_path
        
        except Exception as e:
            raise Exception(f"Error generating speech with OpenAI TTS: {str(e)}")
    
    @staticmethod
    def generate_with_gtts(text: str, language: str = "en", speed: bool = False, 
                          accent: str = "com", output_path: Optional[str] = None) -> str:
        """
        Generate speech using Google Text-to-Speech (gTTS)
        
        Args:
            text: Text to convert to speech
            language: Language code (en, es, fr, etc.)
            speed: If True, use slower speed
            accent: TLD for accent (com, co.uk, com.au, etc.)
            output_path: Optional output file path
            
        Returns:
            str: Path to generated audio file
        """
        try:
            # Create temp file if no output path specified
            if output_path is None:
                temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3')
                output_path = temp_file.name
                temp_file.close()
            
            # Generate speech
            tts = gTTS(text=text, lang=language, slow=speed, tld=accent)
            tts.save(output_path)
            
            return output_path
        
        except Exception as e:
            raise Exception(f"Error generating speech with gTTS: {str(e)}")
    
    @staticmethod
    def generate_with_pyttsx3(text: str, rate: int = 150, volume: float = 1.0,
                             voice_gender: str = "female", output_path: Optional[str] = None) -> str:
        """
        Generate speech using pyttsx3 (offline TTS)
        
        Args:
            text: Text to convert to speech
            rate: Speech rate (words per minute)
            volume: Volume level (0.0 to 1.0)
            voice_gender: Preferred voice gender (male, female)
            output_path: Optional output file path
            
        Returns:
            str: Path to generated audio file
        """
        try:
            # Create temp file if no output path specified
            if output_path is None:
                temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.wav')
                output_path = temp_file.name
                temp_file.close()
            
            # Initialize engine
            engine = pyttsx3.init()
            
            # Set properties
            engine.setProperty('rate', rate)
            engine.setProperty('volume', volume)
            
            # Try to set voice based on gender preference
            voices = engine.getProperty('voices')
            for voice in voices:
                if voice_gender.lower() in voice.name.lower():
                    engine.setProperty('voice', voice.id)
                    break
            
            # Save to file
            engine.save_to_file(text, output_path)
            engine.runAndWait()
            
            return output_path
        
        except Exception as e:
            raise Exception(f"Error generating speech with pyttsx3: {str(e)}")
    
    @staticmethod
    def generate_speech(text: str, engine: str = "gtts", **kwargs) -> str:
        """
        Main method to generate speech using specified engine
        
        Args:
            text: Text to convert to speech
            engine: TTS engine to use (openai, gtts, pyttsx3)
            **kwargs: Additional arguments for specific engine
            
        Returns:
            str: Path to generated audio file
        """
        engine = engine.lower()
        
        if engine == "openai":
            return TTSGenerator.generate_with_openai(text, **kwargs)
        elif engine == "gtts":
            return TTSGenerator.generate_with_gtts(text, **kwargs)
        elif engine == "pyttsx3":
            return TTSGenerator.generate_with_pyttsx3(text, **kwargs)
        else:
            raise ValueError(f"Unsupported TTS engine: {engine}")
    
    @staticmethod
    def chunk_text_for_tts(text: str, max_length: int = 5000) -> list:
        """
        Split text into chunks suitable for TTS processing
        
        Args:
            text: Input text
            max_length: Maximum characters per chunk
            
        Returns:
            list: List of text chunks
        """
        if len(text) <= max_length:
            return [text]
        
        chunks = []
        sentences = text.replace('\n', ' ').split('. ')
        current_chunk = ""
        
        for sentence in sentences:
            if len(current_chunk) + len(sentence) + 2 <= max_length:
                current_chunk += sentence + ". "
            else:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                current_chunk = sentence + ". "
        
        if current_chunk:
            chunks.append(current_chunk.strip())
        
        return chunks
    
    @staticmethod
    def get_available_openai_voices() -> list:
        """Get list of available OpenAI TTS voices"""
        return ["alloy", "echo", "fable", "onyx", "nova", "shimmer"]
    
    @staticmethod
    def get_available_gtts_accents() -> dict:
        """Get list of available gTTS accents"""
        return {
            "US English": "com",
            "UK English": "co.uk",
            "Australian English": "com.au",
            "Indian English": "co.in",
            "Canadian English": "ca"
        }
