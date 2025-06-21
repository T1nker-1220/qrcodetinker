"""
Core QR code generation functionality.
"""

import os
import qrcode
from PIL import Image, ImageDraw, ImageFont
from typing import Optional, Tuple, Union


class QRGenerator:
    """
    A flexible QR code generator that supports various input types and customization options.
    """

    def __init__(self):
        """Initialize the QR code generator."""
        self.default_version = 1
        self.default_error_correction = qrcode.constants.ERROR_CORRECT_M
        self.default_box_size = 20  # Increased from 10 to 20 for larger QR codes
        self.default_border = 4
        self.default_fg_color = "black"
        self.default_bg_color = "white"
        self.default_title_bg_color = "#42f593"  # Default blue background for title
        self.default_title_text_color = "white"  # Default white text for title

    def generate(
        self,
        content: str,
        output_path: str,
        version: Optional[int] = None,
        error_correction: Optional[int] = None,
        box_size: Optional[int] = None,
        border: Optional[int] = None,
        fg_color: Optional[Union[str, Tuple[int, int, int]]] = None,
        bg_color: Optional[Union[str, Tuple[int, int, int]]] = None,
        title: Optional[str] = None,
    ) -> str:
        """
        Generate a QR code from the given content and save it to the specified path.

        Args:
            content: The content to encode in the QR code (URL, text, etc.)
            output_path: The path where the QR code image will be saved
            version: QR code version (1-40, controls size)
            error_correction: Error correction level
            box_size: Size of each box in pixels
            border: Border size in boxes
            fg_color: Foreground color (color of the QR code)
            bg_color: Background color

        Returns:
            The path to the generated QR code image
        """
        # Set default values if not provided
        version = version or self.default_version
        error_correction = error_correction or self.default_error_correction
        box_size = box_size or self.default_box_size
        border = border or self.default_border
        fg_color = fg_color or self.default_fg_color
        bg_color = bg_color or self.default_bg_color

        # Create QR code instance
        qr = qrcode.QRCode(
            version=version,
            error_correction=error_correction,
            box_size=box_size,
            border=border,
        )

        # Add data to the QR code
        qr.add_data(content)
        qr.make(fit=True)

        # Create an image from the QR code
        qr_img = qr.make_image(fill_color=fg_color, back_color=bg_color)
        
        # If a title is provided, add it to the image
        if title:
            img = self._add_title_to_image(qr_img, title)
        else:
            img = qr_img
            
        # Ensure the directory exists
        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)

        # Save the image
        img.save(output_path)

        return output_path

    def generate_with_logo(
        self,
        content: str,
        output_path: str,
        logo_path: str,
        logo_size: Optional[float] = 0.2,  # Logo size as a fraction of QR code size
        title: Optional[str] = None,
        **kwargs
    ) -> str:
        """
        Generate a QR code with a logo in the center.

        Args:
            content: The content to encode in the QR code
            output_path: The path where the QR code image will be saved
            logo_path: Path to the logo image
            logo_size: Size of the logo as a fraction of the QR code size (0.0-1.0)
            **kwargs: Additional arguments to pass to the generate method

        Returns:
            The path to the generated QR code image with logo
        """
        # First generate a regular QR code
        self.generate(content, output_path, **kwargs)

        # Open the QR code image
        qr_img = Image.open(output_path)
        qr_width, qr_height = qr_img.size

        # Open the logo image
        logo_img = Image.open(logo_path)

        # Calculate the size of the logo
        logo_max_size = int(min(qr_width, qr_height) * logo_size)
        logo_width, logo_height = logo_img.size

        # Resize the logo to fit within the QR code
        if logo_width > logo_max_size or logo_height > logo_max_size:
            logo_img = logo_img.resize(
                (logo_max_size, int(logo_height * logo_max_size / logo_width))
                if logo_width > logo_height
                else (int(logo_width * logo_max_size / logo_height), logo_max_size)
            )
            logo_width, logo_height = logo_img.size

        # Calculate position to place the logo (center)
        position = ((qr_width - logo_width) // 2, (qr_height - logo_height) // 2)

        # Create a new image for the result
        result = Image.new("RGBA", (qr_width, qr_height), (0, 0, 0, 0))

        # Paste the QR code onto the new image
        result.paste(qr_img, (0, 0))

        # Paste the logo onto the new image
        result.paste(logo_img, position, logo_img if logo_img.mode == 'RGBA' else None)

        # If a title is provided, add it to the image
        if title:
            final_img = self._add_title_to_image(result, title)
            final_img.save(output_path)
        else:
            result.save(output_path)

        return output_path
        
    def _add_title_to_image(self, img: Image.Image, title: str) -> Image.Image:
        """
        Add a title to the QR code image.
        
        Args:
            img: The QR code image
            title: The title text to add
            
        Returns:
            The QR code image with the title added
        """
        # Convert the image to RGB if it's not already
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        # Get the size of the original image
        qr_width, qr_height = img.size
        
        # Define title area height - increased for better visibility
        title_height = 80
        
        # Create a new blank image with space for the title
        new_img = Image.new('RGB', (qr_width, qr_height + title_height), 'white')
        
        # Create a drawing context for the new image
        draw = ImageDraw.Draw(new_img)
        
        # Draw the title background
        draw.rectangle([(0, 0), (qr_width, title_height)], fill=self.default_title_bg_color)
        
        # Copy the QR code to the bottom part of the new image
        for y in range(qr_height):
            for x in range(qr_width):
                pixel = img.getpixel((x, y))
                new_img.putpixel((x, y + title_height), pixel)
        
        # Try to use a larger font
        font_size = 30
        try:
            # Try common system fonts
            if os.name == 'nt':  # Windows
                font = ImageFont.truetype("arial.ttf", font_size)
            else:  # Linux/Mac
                font = ImageFont.truetype("DejaVuSans.ttf", font_size)
        except:
            # Fall back to default
            font = ImageFont.load_default()
        
        # Try to center the text
        try:
            # For newer Pillow versions
            text_width = draw.textlength(title, font=font)
        except AttributeError:
            # Fallback for older Pillow versions
            text_width = font.getsize(title)[0]
        
        text_x = (qr_width - text_width) // 2
        text_y = (title_height - font_size) // 2  # Center vertically in title area
        
        # Draw the title
        draw.text((text_x, text_y), title, fill=self.default_title_text_color, font=font)
        
        return new_img
