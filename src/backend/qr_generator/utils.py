"""
Utility functions for QR code generation.
"""

import os
import re
from typing import Dict, Optional, Tuple, Union
from urllib.parse import urlparse


def is_url(text: str) -> bool:
    """
    Check if the given text is a valid URL.

    Args:
        text: The text to check

    Returns:
        True if the text is a valid URL, False otherwise
    """
    try:
        result = urlparse(text)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False


def detect_content_type(content: str) -> str:
    """
    Detect the type of content (URL, email, phone, text, etc.).

    Args:
        content: The content to analyze

    Returns:
        The detected content type as a string
    """
    # Check if it's a URL
    if is_url(content):
        return "url"

    # Check if it's an email address
    if re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", content):
        return "email"

    # Check if it's a phone number
    if re.match(r"^\+?[\d\s\-\(\)]{7,}$", content):
        return "phone"

    # Default to text
    return "text"


def parse_color(color: Union[str, Tuple[int, int, int]]) -> Union[str, Tuple[int, int, int]]:
    """
    Parse a color string into a format accepted by PIL.

    Args:
        color: Color as a string (name or hex) or RGB tuple

    Returns:
        The parsed color
    """
    if isinstance(color, tuple):
        return color

    # If it's a hex color code, ensure it has a # prefix
    if re.match(r"^[0-9a-fA-F]{6}$", color):
        return f"#{color}"

    return color


def ensure_directory(path: str) -> None:
    """
    Ensure that the directory for the given path exists.

    Args:
        path: The file path
    """
    directory = os.path.dirname(os.path.abspath(path))
    os.makedirs(directory, exist_ok=True)


def get_file_extension(path: str) -> str:
    """
    Get the file extension from a path.

    Args:
        path: The file path

    Returns:
        The file extension (without the dot)
    """
    _, ext = os.path.splitext(path)
    return ext.lstrip(".").lower()


def format_wifi_data(ssid: str, password: Optional[str] = None, security: str = "WPA") -> str:
    """
    Format WiFi network data for QR code generation.

    Args:
        ssid: The WiFi network name
        password: The WiFi password (optional)
        security: The security type (WPA, WEP, or nopass)

    Returns:
        Formatted WiFi data string
    """
    if security.lower() == "nopass":
        return f"WIFI:S:{ssid};T:nopass;;"
    else:
        return f"WIFI:S:{ssid};T:{security};P:{password or ''};"


def format_contact_data(
    name: str,
    phone: Optional[str] = None,
    email: Optional[str] = None,
    company: Optional[str] = None,
    title: Optional[str] = None,
    website: Optional[str] = None,
) -> str:
    """
    Format contact data as a vCard for QR code generation.

    Args:
        name: Contact name
        phone: Phone number (optional)
        email: Email address (optional)
        company: Company name (optional)
        title: Job title (optional)
        website: Website URL (optional)

    Returns:
        Formatted vCard string
    """
    vcard = [
        "BEGIN:VCARD",
        "VERSION:3.0",
        f"N:{name}",
        f"FN:{name}",
    ]

    if company:
        vcard.append(f"ORG:{company}")

    if title:
        vcard.append(f"TITLE:{title}")

    if phone:
        vcard.append(f"TEL:{phone}")

    if email:
        vcard.append(f"EMAIL:{email}")

    if website:
        vcard.append(f"URL:{website}")

    vcard.append("END:VCARD")

    return "\n".join(vcard)


def format_event_data(
    name: str,
    start_iso: str,
    end_iso: Optional[str] = None,
    location: Optional[str] = None,
) -> str:
    """
    Format calendar event data as a VCALENDAR for QR code generation.

    Args:
        name: Event name/title
        start_iso: Start date/time in ISO format (YYYY-MM-DDTHH:MM)
        end_iso: End date/time in ISO format (optional)
        location: Event location (optional)

    Returns:
        Formatted VCALENDAR string
    """
    from datetime import datetime
    
    def iso_to_ics(dt: str) -> str:
        """Convert ISO datetime to ICS format."""
        if not dt:
            return ''
        # Parse datetime-local format: YYYY-MM-DDTHH:MM
        return datetime.strptime(dt, '%Y-%m-%dT%H:%M').strftime('%Y%m%dT%H%M%S')
    
    dtstart = iso_to_ics(start_iso)
    
    lines = [
        'BEGIN:VCALENDAR',
        'VERSION:2.0',
        'PRODID:-//QRGenerator//EN',
        'BEGIN:VEVENT',
        f'SUMMARY:{name}',
        f'DTSTART:{dtstart}',
    ]
    
    if end_iso:
        dtend = iso_to_ics(end_iso)
        if dtend:
            lines.append(f'DTEND:{dtend}')
    
    if location:
        lines.append(f'LOCATION:{location}')
    
    lines.extend([
        'END:VEVENT',
        'END:VCALENDAR'
    ])
    
    return '\n'.join(lines)


def format_geo_data(latitude: str, longitude: str) -> str:
    """
    Format geolocation data as a geo URI for QR code generation.

    Args:
        latitude: Latitude coordinate
        longitude: Longitude coordinate

    Returns:
        Formatted geo URI string (RFC 5870)
    """
    return f'geo:{latitude},{longitude}'


def format_email_data(
    recipient: str,
    subject: Optional[str] = None,
    body: Optional[str] = None,
) -> str:
    """
    Format email data as a mailto URI for QR code generation.

    Args:
        recipient: Email recipient address
        subject: Email subject (optional)
        body: Email body text (optional)

    Returns:
        Formatted mailto URI string
    """
    from urllib.parse import quote
    
    query_params = []
    
    if subject:
        query_params.append(f'subject={quote(subject)}')
    
    if body:
        query_params.append(f'body={quote(body)}')
    
    query_string = ('?' + '&'.join(query_params)) if query_params else ''
    
    return f'mailto:{recipient}{query_string}'
