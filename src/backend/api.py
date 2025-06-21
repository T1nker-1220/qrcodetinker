"""
QR Code Generator API.

A Flask API for generating QR codes from various input types.
Designed to work with Vercel serverless deployment.
"""

import os
import base64
import io
import uuid
import tempfile
import re
import sys
import traceback
import logging
from flask import Flask, request, jsonify, send_from_directory, Response
from flask_cors import CORS
from qr_generator import QRGenerator
from qr_generator.utils import format_wifi_data, format_contact_data

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Environment configuration
is_production = os.environ.get('ENVIRONMENT', 'development') == 'production'
allowed_origins = os.environ.get('ALLOWED_ORIGINS', '*')

logger.info(f"Starting API in {'production' if is_production else 'development'} mode")
logger.info(f"CORS allowed origins: {allowed_origins}")

app = Flask(__name__, static_folder='../frontend')
CORS(app, resources={r"/api/*": {"origins": allowed_origins}}, supports_credentials=True)

# Create a QR generator instance
qr_generator = QRGenerator()

# In-memory storage for generated QR codes (for serverless environment)
qr_codes = {}

# Create a temporary directory for file operations if needed
temp_dir = tempfile.gettempdir()


def sanitize_filename(title, max_length=50):
    """
    Sanitize a title to make it suitable for use as a filename.
    
    Args:
        title: The title to sanitize
        max_length: Maximum length of the resulting filename (before extension)
        
    Returns:
        A sanitized filename
    """
    # Replace spaces with underscores and remove special characters
    sanitized = re.sub(r'[^\w\-_]', '', title.replace(' ', '_'))
    
    # Limit the length
    if len(sanitized) > max_length:
        sanitized = sanitized[:max_length]
    
    # Ensure the filename is not empty
    if not sanitized:
        sanitized = "qr_code"
    
    return sanitized


@app.route('/')
def index():
    """Serve the frontend index.html file."""
    return send_from_directory('../frontend/html', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    """Serve static files from the frontend directory."""
    if path.startswith('css/'):
        return send_from_directory('../frontend', path)
    elif path.startswith('js/'):
        return send_from_directory('../frontend', path)
    else:
        return send_from_directory('../frontend/html', path)


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint to verify the API is working."""
    return jsonify({
        'status': 'ok',
        'environment': 'production' if is_production else 'development'
    })

@app.route('/api/generate', methods=['POST'])
def generate_qr():
    """Generate a QR code based on the request data."""
    logger.info("Received request to generate QR code")
    try:
        data = request.json
        qr_type = data.get('type', 'custom')
        title = data.get('title', 'QR Code')
        
        # Prepare content based on QR type
        if qr_type == 'url':
            content = data.get('content', '')
        elif qr_type == 'wifi':
            ssid = data.get('ssid', '')
            password = data.get('password', '')
            security = data.get('security', 'WPA')
            content = format_wifi_data(ssid, password, security)
        elif qr_type == 'contact':
            name = data.get('name', '')
            phone = data.get('phone', '')
            email = data.get('email', '')
            company = data.get('company', '')
            job_title = data.get('jobTitle', '')
            website = data.get('website', '')
            content = format_contact_data(
                name=name,
                phone=phone,
                email=email,
                company=company,
                title=job_title,
                website=website
            )
        else:  # custom
            content = data.get('content', '')
        
        # Set QR code options
        options = {
            'title': title,
            'box_size': 20,  # Larger QR code
        }
        
        # Add custom colors if provided
        if qr_type == 'custom':
            fg_color = data.get('fgColor', '#000000')
            bg_color = data.get('bgColor', '#FFFFFF')
            options['fg_color'] = fg_color
            options['bg_color'] = bg_color
        
        # Generate a filename based on the title
        sanitized_title = sanitize_filename(title)
        # Add a short random string to ensure uniqueness
        short_uuid = uuid.uuid4().hex[:8]
        filename = f"{sanitized_title}_{short_uuid}.png"
        
        try:
            # For serverless environment, use a temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as temp_file:
                temp_path = temp_file.name
                logger.info(f"Created temporary file at {temp_path}")
                
                # Generate the QR code
                qr_generator.generate(
                    content=content,
                    output_path=temp_path,
                    **options
                )
                logger.info("QR code generated successfully")
                
                # Convert the image to base64 for direct embedding in HTML
                with open(temp_path, "rb") as image_file:
                    encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
                
                # Store the image data in memory for download
                qr_codes[filename] = encoded_string
                logger.info(f"QR code stored in memory with filename {filename}")
                
                # Clean up the temporary file
                try:
                    os.unlink(temp_path)
                    logger.info("Temporary file cleaned up")
                except Exception as e:
                    logger.warning(f"Failed to clean up temporary file: {str(e)}")
        except Exception as e:
            logger.error(f"Error in QR code generation: {str(e)}")
            logger.error(traceback.format_exc())
            raise
        
        # Return the QR code as base64 data URL
        return jsonify({
            'success': True,
            'qrCodeUrl': f"data:image/png;base64,{encoded_string}",
            'filename': filename
        })
        
    except Exception as e:
        logger.error(f"Error handling request: {str(e)}")
        logger.error(traceback.format_exc())
        return jsonify({
            'success': False,
            'error': str(e),
            'details': traceback.format_exc() if not is_production else "An error occurred while generating the QR code."
        }), 500


@app.route('/api/download/<filename>', methods=['GET'])
def download_qr(filename):
    """Download a generated QR code."""
    logger.info(f"Received request to download QR code: {filename}")
    if filename in qr_codes:
        logger.info("QR code found in memory")
        # Create a response with the image data
        image_data = base64.b64decode(qr_codes[filename])
        response = Response(image_data, mimetype='image/png')
        # Extract the original filename from the storage key
        original_filename = filename
        response.headers.set('Content-Disposition', f'attachment; filename="{original_filename}"')
        return response
    else:
        logger.warning(f"QR code not found: {filename}")
        return jsonify({
            'success': False,
            'error': 'File not found'
        }), 404

# For local development
if __name__ == '__main__':
    app.run(debug=True, port=5000)

# For Vercel serverless deployment
app_handler = app
