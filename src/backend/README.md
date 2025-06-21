# QR Code Generator

A flexible Python package for generating QR codes from various input types.

## Features

- Generate QR codes from URLs, text, contact information, WiFi credentials, and more
- Customize QR code appearance (size, colors, error correction level)
- Add logos to QR codes
- Command-line interface for easy usage
- Python API for integration into other applications

## Installation

### From Source

1. Clone the repository
2. Navigate to the `src/backend` directory
3. Install the package:

```bash
pip install -e .
```

### Dependencies

- Python 3.7+
- qrcode
- Pillow (PIL)
- click

## Usage

### Command Line Interface

#### Generate a basic QR code

```bash
python main.py generate --content "https://example.com" --output qr_code.png
```

#### Generate a QR code with custom appearance

```bash
python main.py generate --content "Hello World" --output qr_code.png --version 2 --box-size 15 --border 2 --fg-color "blue" --bg-color "#FFFF00"
```

#### Generate a QR code with a logo

```bash
python main.py generate-with-logo --content "https://example.com" --output qr_code.png --logo logo.png --logo-size 0.2
```

#### Generate a WiFi QR code

```bash
python main.py wifi --ssid "MyNetwork" --password "password123" --security WPA --output wifi_qr.png
```

#### Generate a contact QR code (vCard)

```bash
python main.py contact --name "John Doe" --phone "+1234567890" --email "john@example.com" --company "Example Corp" --title "Developer" --website "https://example.com" --output contact_qr.png
```

### Python API

```python
from qr_generator import QRGenerator

# Create a QR generator instance
qr = QRGenerator()

# Generate a basic QR code
qr.generate("https://example.com", "qr_code.png")

# Generate a QR code with custom appearance
qr.generate(
    content="Hello World",
    output_path="custom_qr.png",
    version=2,
    box_size=15,
    border=2,
    fg_color="blue",
    bg_color="#FFFF00"
)

# Generate a QR code with a logo
qr.generate_with_logo(
    content="https://example.com",
    output_path="logo_qr.png",
    logo_path="logo.png",
    logo_size=0.2
)
```

## Testing

Run the tests using pytest:

```bash
pytest
```

## License

MIT
