# QR Code Generator

A flexible QR code generator with both a Python backend and a web-based frontend. This application allows you to generate QR codes for various types of content including URLs, WiFi networks, contact information, and custom text.

## Features

- Generate QR codes for:
  - URLs
  - WiFi networks (with network name, password, and security type)
  - Contact information (vCard format)
  - Custom text or data
- Customize QR codes with:
  - Custom titles with colored backgrounds
  - Custom foreground and background colors
  - Adjustable size
- Download generated QR codes as PNG files
- Add logos to QR codes (via Python API)
- User-friendly web interface

## Project Structure

```
qr-code/
├── src/
│   ├── backend/             # Python backend
│   │   ├── qr_generator/    # QR generator package
│   │   ├── output/          # Generated QR codes
│   │   ├── examples.py      # Example usage
│   │   ├── api.py           # Flask API
│   │   └── main.py          # CLI interface
│   └── frontend/            # Web frontend
│       ├── css/             # Stylesheets
│       ├── html/            # HTML files
│       └── js/              # JavaScript files
```

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/qr-code.git
   cd qr-code
   ```

2. Install the required Python packages:
   ```
   pip install -r src/backend/requirements.txt
   ```

## Usage

### Running the Backend API

1. Start the Flask API server:
   ```
   cd src/backend
   python api.py
   ```
   The API will be available at http://localhost:5000

### Running the Frontend

1. With the backend running, open the frontend in your browser:
   ```
   http://localhost:5000
   ```

### Using the Python Package Directly

You can also use the QR generator package directly in your Python code:

```python
from qr_generator import QRGenerator

# Create a QR generator instance
qr = QRGenerator()

# Generate a basic URL QR code
qr.generate(
    content="https://example.com",
    output_path="output/url_qr.png",
    title="My Website"
)

# Generate a WiFi QR code
from qr_generator.utils import format_wifi_data
wifi_data = format_wifi_data(
    ssid="MyNetwork",
    password="password123",
    security="WPA"
)
qr.generate(
    content=wifi_data,
    output_path="output/wifi_qr.png",
    title="WiFi: MyNetwork"
)
```

See `src/backend/examples.py` for more examples.

## API Endpoints

- `POST /api/generate`: Generate a QR code
  - Request body: JSON with QR code parameters
  - Response: JSON with QR code data URL and filename

- `GET /api/download/<filename>`: Download a generated QR code

## License

This project is licensed under the MIT License - see the LICENSE file for details.
