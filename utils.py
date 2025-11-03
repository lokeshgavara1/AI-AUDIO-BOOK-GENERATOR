"""
Utility Functions Module
Helper functions for the AI Audio Book Generator
"""

import os
import tempfile
from pathlib import Path
from datetime import datetime
import streamlit as st


def get_file_extension(filename: str) -> str:
    """
    Get file extension from filename
    
    Args:
        filename: Name of the file
        
    Returns:
        str: File extension without dot
    """
    return Path(filename).suffix[1:].lower()


def format_file_size(size_bytes: int) -> str:
    """
    Format file size in human-readable format
    
    Args:
        size_bytes: Size in bytes
        
    Returns:
        str: Formatted size (e.g., "1.5 MB")
    """
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} TB"


def create_temp_file(suffix: str = ".mp3") -> str:
    """
    Create a temporary file
    
    Args:
        suffix: File suffix/extension
        
    Returns:
        str: Path to temporary file
    """
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
    temp_file.close()
    return temp_file.name


def clean_temp_files(file_paths: list):
    """
    Remove temporary files
    
    Args:
        file_paths: List of file paths to delete
    """
    for file_path in file_paths:
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
        except Exception as e:
            st.warning(f"Could not delete temp file {file_path}: {str(e)}")


def estimate_reading_time(text: str, words_per_minute: int = 150) -> dict:
    """
    Estimate reading/listening time for text
    
    Args:
        text: Input text
        words_per_minute: Average reading speed
        
    Returns:
        dict: Dictionary with minutes and seconds
    """
    word_count = len(text.split())
    total_minutes = word_count / words_per_minute
    minutes = int(total_minutes)
    seconds = int((total_minutes - minutes) * 60)
    
    return {
        "word_count": word_count,
        "minutes": minutes,
        "seconds": seconds,
        "total_minutes": round(total_minutes, 2)
    }


def generate_output_filename(original_filename: str, suffix: str = "_audiobook") -> str:
    """
    Generate output filename for audio file
    
    Args:
        original_filename: Original uploaded file name
        suffix: Suffix to add to filename
        
    Returns:
        str: Output filename
    """
    stem = Path(original_filename).stem
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{stem}{suffix}_{timestamp}.mp3"


def truncate_text(text: str, max_length: int = 200) -> str:
    """
    Truncate text to specified length
    
    Args:
        text: Input text
        max_length: Maximum length
        
    Returns:
        str: Truncated text
    """
    if len(text) <= max_length:
        return text
    return text[:max_length] + "..."


def validate_text_length(text: str, min_length: int = 10, max_length: int = 100000) -> tuple:
    """
    Validate text length
    
    Args:
        text: Input text
        min_length: Minimum allowed length
        max_length: Maximum allowed length
        
    Returns:
        tuple: (is_valid, error_message)
    """
    text_length = len(text.strip())
    
    if text_length < min_length:
        return False, f"Text is too short. Minimum {min_length} characters required."
    
    if text_length > max_length:
        return False, f"Text is too long. Maximum {max_length} characters allowed."
    
    return True, ""


def get_session_state_default(key: str, default_value):
    """
    Get value from Streamlit session state with default
    
    Args:
        key: Session state key
        default_value: Default value if key doesn't exist
        
    Returns:
        Value from session state or default
    """
    if key not in st.session_state:
        st.session_state[key] = default_value
    return st.session_state[key]


def init_session_state():
    """Initialize Streamlit session state variables"""
    defaults = {
        'extracted_text': None,
        'rewritten_text': None,
        'audio_file_path': None,
        'processing_complete': False,
        'current_step': 0
    }
    
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def display_progress_bar(current: int, total: int, message: str = "Processing"):
    """
    Display progress bar
    
    Args:
        current: Current progress value
        total: Total value
        message: Progress message
    """
    progress = current / total if total > 0 else 0
    st.progress(progress, text=f"{message}... {current}/{total}")


def safe_api_call(func, *args, **kwargs):
    """
    Safely execute API call with error handling
    
    Args:
        func: Function to call
        *args: Positional arguments
        **kwargs: Keyword arguments
        
    Returns:
        Result of function call or None if error
    """
    try:
        return func(*args, **kwargs)
    except Exception as e:
        st.error(f"API Error: {str(e)}")
        return None
