"""
Tests for the QR code generator.
"""

import os
import pytest
import tempfile
from PIL import Image

from qr_generator import QRGenerator
from qr_generator.utils import detect_content_type, format_wifi_data, format_contact_data


class TestQRGenerator:
    """Test cases for the QRGenerator class."""

    def setup_method(self):
        """Set up test fixtures."""
        self.qr = QRGenerator()
        self.temp_dir = tempfile.mkdtemp()
        self.test_output = os.path.join(self.temp_dir, "test_qr.png")

    def teardown_method(self):
        """Tear down test fixtures."""
        # Clean up temporary files
        if os.path.exists(self.test_output):
            os.remove(self.test_output)
        os.rmdir(self.temp_dir)

    def test_generate_url(self):
        """Test generating a QR code from a URL."""
        url = "https://example.com"
        output_path = self.qr.generate(url, self.test_output)
        
        # Check that the file was created
        assert os.path.exists(output_path)
        
        # Check that it's a valid image
        img = Image.open(output_path)
        assert img.format == "PNG"
        
        # Check content type detection
        assert detect_content_type(url) == "url"

    def test_generate_text(self):
        """Test generating a QR code from plain text."""
        text = "Hello, World!"
        output_path = self.qr.generate(text, self.test_output)
        
        # Check that the file was created
        assert os.path.exists(output_path)
        
        # Check that it's a valid image
        img = Image.open(output_path)
        assert img.format == "PNG"
        
        # Check content type detection
        assert detect_content_type(text) == "text"

    def test_generate_with_custom_parameters(self):
        """Test generating a QR code with custom parameters."""
        text = "Custom QR Code"
        output_path = self.qr.generate(
            text,
            self.test_output,
            version=2,
            box_size=15,
            border=2,
            fg_color="blue",
            bg_color="#FFFF00",
        )
        
        # Check that the file was created
        assert os.path.exists(output_path)
        
        # Check that it's a valid image
        img = Image.open(output_path)
        assert img.format == "PNG"

    def test_wifi_format(self):
        """Test formatting WiFi data."""
        # Test with password
        wifi_data = format_wifi_data("MyNetwork", "password123", "WPA")
        assert "WIFI:S:MyNetwork;T:WPA;P:password123;" in wifi_data
        
        # Test without password
        wifi_data = format_wifi_data("OpenNetwork", security="nopass")
        assert "WIFI:S:OpenNetwork;T:nopass;;" in wifi_data

    def test_contact_format(self):
        """Test formatting contact data."""
        vcard = format_contact_data(
            name="John Doe",
            phone="+1234567890",
            email="john@example.com",
            company="Example Corp",
            title="Developer",
            website="https://example.com",
        )
        
        # Check that it contains all the expected fields
        assert "BEGIN:VCARD" in vcard
        assert "VERSION:3.0" in vcard
        assert "N:John Doe" in vcard
        assert "TEL:+1234567890" in vcard
        assert "EMAIL:john@example.com" in vcard
        assert "ORG:Example Corp" in vcard
        assert "TITLE:Developer" in vcard
        assert "URL:https://example.com" in vcard
        assert "END:VCARD" in vcard


# Run the tests if the file is executed directly
if __name__ == "__main__":
    pytest.main(["-v", __file__])
