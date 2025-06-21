#!/usr/bin/env python
"""
Example usage of the QR code generator.

This script demonstrates various ways to use the QR code generator.
"""

import os
from qr_generator import QRGenerator
from qr_generator.utils import format_wifi_data, format_contact_data


def main():
    """Run the examples."""
    # Create output directory if it doesn't exist
    os.makedirs("output", exist_ok=True)

    # Create a QR generator instance
    qr = QRGenerator()

    # Example 1: Generate a basic QR code from a URL
    print("Generating URL QR code...")
    qr.generate(
        content="https://kusinadeamadeo.vercel.app/normal-menu",
        output_path="output/kda.png",
        title="Kusina de Amadeo Menu"
    )
    print("URL QR code generated: output/kda.png")

    # Example 2: Generate a QR code with custom appearance
    print("\nGenerating custom QR code...")
    qr.generate(
        content="Hello World",
        output_path="output/custom_qr.png",
        title="Custom QR Code Example",
        version=2,
        box_size=15,
        border=2,
        fg_color="blue",
        bg_color="#FFFF00"
    )
    print("Custom QR code generated: output/custom_qr.png")

    # Example 3: Generate a WiFi QR code
    print("\nGenerating WiFi QR code...")
    wifi_data = format_wifi_data(
        ssid="VirusM5G",
        password="Famarquez2!?",
        security="WPA/WPA-2"
    )
    qr.generate(
        content=wifi_data,
        output_path="output/wifi_qr.png",
        title="WiFi: VirusM5G"
    )
    print("WiFi QR code generated: output/wifi_qr.png")

    # Example 4: Generate a contact QR code (vCard)
    print("\nGenerating contact QR code...")
    vcard_data = format_contact_data(
        name="John Doe",
        phone="+1234567890",
        email="john@example.com",
        company="Example Corp",
        title="Developer",
        website="https://example.com"
    )
    qr.generate(
        content=vcard_data,
        output_path="output/contact_qr.png",
        title="Contact: John Doe"
    )
    print("Contact QR code generated: output/contact_qr.png")

    # Example 5: Generate a QR code with a logo
    # Note: You need to provide a logo image for this to work
    print("\nTo generate a QR code with a logo, run:")
    print("qr.generate_with_logo(")
    print('    content="https://example.com",')
    print('    output_path="output/logo_qr.png",')
    print('    logo_path="path/to/your/logo.png",')
    print('    logo_size=0.2,')
    print('    title="Website with Logo"')
    print(")")

    print("\nAll examples completed. Check the 'output' directory for the generated QR codes.")


if __name__ == "__main__":
    main()
