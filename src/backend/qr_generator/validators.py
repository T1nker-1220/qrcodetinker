"""
Input validation for QR code generation.
"""

import os
import re
from typing import Dict, List, Optional, Tuple, Union

from .utils import is_url, get_file_extension


def validate_content(content: str) -> Tuple[bool, Optional[str]]:
    """
    Validate the content to be encoded in the QR code.

    Args:
        content: The content to validate

    Returns:
        A tuple of (is_valid, error_message)
    """
    if not content:
        return False, "Content cannot be empty"

    # QR codes have a maximum capacity depending on version and error correction
    # This is a simplified check - actual capacity depends on the QR version and error correction level
    if len(content) > 4000:
        return False, "Content is too long for a QR code"

    return True, None


def validate_output_path(output_path: str) -> Tuple[bool, Optional[str]]:
    """
    Validate the output path for the QR code image.

    Args:
        output_path: The path where the QR code image will be saved

    Returns:
        A tuple of (is_valid, error_message)
    """
    if not output_path:
        return False, "Output path cannot be empty"

    # Check if the file extension is supported
    ext = get_file_extension(output_path)
    if ext not in ["png", "jpg", "jpeg", "gif", "svg"]:
        return False, f"Unsupported file format: {ext}. Supported formats: png, jpg, jpeg, gif, svg"

    # Check if the directory exists or can be created
    try:
        directory = os.path.dirname(os.path.abspath(output_path))
        os.makedirs(directory, exist_ok=True)
    except Exception as e:
        return False, f"Cannot create directory for output path: {str(e)}"

    return True, None


def validate_logo_path(logo_path: str) -> Tuple[bool, Optional[str]]:
    """
    Validate the logo path for QR codes with logos.

    Args:
        logo_path: The path to the logo image

    Returns:
        A tuple of (is_valid, error_message)
    """
    if not logo_path:
        return False, "Logo path cannot be empty"

    if not os.path.exists(logo_path):
        return False, f"Logo file does not exist: {logo_path}"

    # Check if the file is an image
    ext = get_file_extension(logo_path)
    if ext not in ["png", "jpg", "jpeg", "gif"]:
        return False, f"Unsupported logo format: {ext}. Supported formats: png, jpg, jpeg, gif"

    return True, None


def validate_color(color: Union[str, Tuple[int, int, int]]) -> Tuple[bool, Optional[str]]:
    """
    Validate a color value.

    Args:
        color: The color to validate (string or RGB tuple)

    Returns:
        A tuple of (is_valid, error_message)
    """
    if isinstance(color, tuple):
        # Check if it's a valid RGB tuple
        if len(color) != 3:
            return False, "RGB color must have exactly 3 values"
        
        for value in color:
            if not isinstance(value, int) or value < 0 or value > 255:
                return False, "RGB values must be integers between 0 and 255"
        
        return True, None
    
    elif isinstance(color, str):
        # Check if it's a hex color code
        if re.match(r"^#?[0-9a-fA-F]{6}$", color):
            return True, None
        
        # Check if it's a named color (simplified check)
        named_colors = [
            "black", "white", "red", "green", "blue", "yellow", "purple", 
            "cyan", "magenta", "gray", "grey", "orange", "pink", "brown"
        ]
        
        if color.lower() in named_colors:
            return True, None
        
        return False, f"Invalid color: {color}. Use a hex code, RGB tuple, or named color."
    
    return False, f"Invalid color type: {type(color)}. Must be a string or RGB tuple."


def validate_qr_parameters(
    version: Optional[int] = None,
    error_correction: Optional[int] = None,
    box_size: Optional[int] = None,
    border: Optional[int] = None,
) -> Tuple[bool, Optional[str]]:
    """
    Validate QR code parameters.

    Args:
        version: QR code version (1-40)
        error_correction: Error correction level
        box_size: Size of each box in pixels
        border: Border size in boxes

    Returns:
        A tuple of (is_valid, error_message)
    """
    if version is not None and (not isinstance(version, int) or version < 1 or version > 40):
        return False, "QR code version must be an integer between 1 and 40"
    
    if box_size is not None and (not isinstance(box_size, int) or box_size < 1):
        return False, "Box size must be a positive integer"
    
    if border is not None and (not isinstance(border, int) or border < 0):
        return False, "Border must be a non-negative integer"
    
    return True, None


def validate_logo_size(logo_size: float) -> Tuple[bool, Optional[str]]:
    """
    Validate the logo size parameter.

    Args:
        logo_size: Size of the logo as a fraction of the QR code size (0.0-1.0)

    Returns:
        A tuple of (is_valid, error_message)
    """
    if not isinstance(logo_size, (int, float)):
        return False, "Logo size must be a number"
    
    if logo_size <= 0 or logo_size >= 1:
        return False, "Logo size must be between 0 and 1 (exclusive)"
    
    # Logo shouldn't be too large or it might make the QR code unreadable
    if logo_size > 0.3:
        return False, "Logo size should not exceed 0.3 (30% of QR code size) for reliable scanning"
    
    return True, None
