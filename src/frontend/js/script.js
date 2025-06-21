/**
 * QR Code Generator JavaScript
 * This script handles the functionality of the QR code generator web interface.
 */

// API endpoint for the QR code generation
// Check if we're in a local development environment by looking for common local hostnames
const isLocalhost = window.location.hostname === 'localhost' || 
                    window.location.hostname === '127.0.0.1' ||
                    window.location.hostname.startsWith('192.168.') ||
                    window.location.hostname.endsWith('.local') ||
                    window.location.hostname.indexOf('.') === -1; // No dots usually means local hostname

const isProduction = !isLocalhost;
const API_ENDPOINT = isProduction 
  ? 'https://qrcodetinker.vercel.app/api/generate'
  : 'http://localhost:5000/api/generate';
const DOWNLOAD_ENDPOINT = isProduction
  ? 'https://qrcodetinker.vercel.app/api/download'
  : 'http://localhost:5000/api/download';

// DOM Elements
document.addEventListener('DOMContentLoaded', () => {
    // Tab navigation
    const tabButtons = document.querySelectorAll('.tab-btn');
    const tabPanes = document.querySelectorAll('.tab-pane');
    
    // Forms
    const urlForm = document.getElementById('url-form');
    const wifiForm = document.getElementById('wifi-form');
    const contactForm = document.getElementById('contact-form');
    const eventForm = document.getElementById('event-form');
    const geoForm = document.getElementById('geo-form');
    const emailForm = document.getElementById('email-form');
    const customForm = document.getElementById('custom-form');
    
    // Result container
    const resultContainer = document.getElementById('result-container');
    const qrImage = document.getElementById('qr-image');
    const downloadBtn = document.getElementById('download-btn');
    const newQrBtn = document.getElementById('new-qr-btn');
    
    // Password visibility toggle
    const showPasswordCheckbox = document.getElementById('show-wifi-password');
    const passwordInput = document.getElementById('wifi-password');

    // Initialize the application
    initTabs();
    initForms();
    initPasswordToggle();
    initResultActions();

    /**
     * Initialize tab navigation
     */
    function initTabs() {
        tabButtons.forEach(button => {
            button.addEventListener('click', () => {
                // Remove active class from all buttons and panes
                tabButtons.forEach(btn => btn.classList.remove('active'));
                tabPanes.forEach(pane => pane.classList.remove('active'));
                
                // Add active class to clicked button and corresponding pane
                button.classList.add('active');
                const tabId = button.getAttribute('data-tab');
                document.getElementById(tabId).classList.add('active');
                
                // Hide result container when switching tabs
                resultContainer.style.display = 'none';
            });
        });
    }

    /**
     * Initialize form submissions
     */
    function initForms() {
        // URL Form
        urlForm.addEventListener('submit', (e) => {
            e.preventDefault();
            const url = document.getElementById('url-input').value;
            const title = document.getElementById('url-title').value || 'URL QR Code';
            
            generateQRCode({
                type: 'url',
                content: url,
                title: title
            });
        });
        
        // WiFi Form
        wifiForm.addEventListener('submit', (e) => {
            e.preventDefault();
            const ssid = document.getElementById('wifi-ssid').value;
            const password = document.getElementById('wifi-password').value;
            const security = document.getElementById('wifi-security').value;
            const title = document.getElementById('wifi-title').value || `WiFi: ${ssid}`;
            
            generateQRCode({
                type: 'wifi',
                ssid: ssid,
                password: password,
                security: security,
                title: title
            });
        });
        
        // Contact Form
        contactForm.addEventListener('submit', (e) => {
            e.preventDefault();
            const name = document.getElementById('contact-name').value;
            const phone = document.getElementById('contact-phone').value;
            const email = document.getElementById('contact-email').value;
            const company = document.getElementById('contact-company').value;
            const jobTitle = document.getElementById('contact-job-title').value;
            const website = document.getElementById('contact-website').value;
            const title = document.getElementById('contact-title').value || `Contact: ${name}`;
            
            generateQRCode({
                type: 'contact',
                name: name,
                phone: phone,
                email: email,
                company: company,
                jobTitle: jobTitle,
                website: website,
                title: title
            });
        });
        
        // Event Form
        eventForm.addEventListener('submit', (e) => {
            e.preventDefault();
            const name = document.getElementById('event-name').value;
            const start = document.getElementById('event-start').value;
            const end = document.getElementById('event-end').value;
            const location = document.getElementById('event-location').value;
            const title = document.getElementById('event-title').value || `Event: ${name}`;
            
            generateQRCode({
                type: 'event',
                name: name,
                start: start,
                end: end,
                location: location,
                title: title
            });
        });
        
        // Geolocation Form
        geoForm.addEventListener('submit', (e) => {
            e.preventDefault();
            const latitude = document.getElementById('geo-latitude').value;
            const longitude = document.getElementById('geo-longitude').value;
            const title = document.getElementById('geo-title').value || `Location: ${latitude}, ${longitude}`;
            
            generateQRCode({
                type: 'geo',
                latitude: latitude,
                longitude: longitude,
                title: title
            });
        });
        
        // Email Form
        emailForm.addEventListener('submit', (e) => {
            e.preventDefault();
            const recipient = document.getElementById('email-recipient').value;
            const subject = document.getElementById('email-subject').value;
            const body = document.getElementById('email-body').value;
            const title = document.getElementById('email-title').value || `Email: ${recipient}`;
            
            generateQRCode({
                type: 'email',
                recipient: recipient,
                subject: subject,
                body: body,
                title: title
            });
        });
        
        // Custom Form
        customForm.addEventListener('submit', (e) => {
            e.preventDefault();
            const content = document.getElementById('custom-content').value;
            const title = document.getElementById('custom-title').value || 'Custom QR Code';
            const fgColor = document.getElementById('custom-fg-color').value;
            const bgColor = document.getElementById('custom-bg-color').value;
            
            generateQRCode({
                type: 'custom',
                content: content,
                title: title,
                fgColor: fgColor,
                bgColor: bgColor
            });
        });
    }

    /**
     * Initialize password visibility toggle
     */
    function initPasswordToggle() {
        if (showPasswordCheckbox && passwordInput) {
            showPasswordCheckbox.addEventListener('change', () => {
                passwordInput.type = showPasswordCheckbox.checked ? 'text' : 'password';
            });
        }
    }

    /**
     * Initialize result actions (download and new QR code)
     */
    function initResultActions() {
        // New QR Code button
        if (newQrBtn) {
            newQrBtn.addEventListener('click', () => {
                resultContainer.style.display = 'none';
            });
        }
        
        // Download button
        if (downloadBtn) {
            downloadBtn.addEventListener('click', () => {
                if (qrImage.src && qrImage.dataset.filename) {
                    // Use the backend download endpoint if we have a filename
                    window.open(`${DOWNLOAD_ENDPOINT}/${qrImage.dataset.filename}`, '_blank');
                } else if (qrImage.src) {
                    // Fallback to direct download from data URL
                    const link = document.createElement('a');
                    link.href = qrImage.src;
                    link.download = 'qrcode.png';
                    document.body.appendChild(link);
                    link.click();
                    document.body.removeChild(link);
                }
            });
        }
    }

    /**
     * Generate QR code based on form data
     * @param {Object} data - The data to encode in the QR code
     */
    function generateQRCode(data) {
        // Show loading state
        showLoading();
        
        // Make API call to our backend
        fetch(API_ENDPOINT, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Store the filename for download
                qrImage.dataset.filename = data.filename;
                displayQRCode(data.qrCodeUrl);
            } else {
                alert('Failed to generate QR code: ' + (data.error || 'Unknown error'));
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred while generating the QR code. Please try again.');
        });
    }

    /**
     * Show loading state
     */
    function showLoading() {
        resultContainer.style.display = 'block';
        qrImage.src = '';
        qrImage.alt = 'Generating QR code...';
        
        // Add a loading indicator
        const loadingDiv = document.createElement('div');
        loadingDiv.className = 'loading';
        loadingDiv.textContent = 'Generating QR code...';
        
        const imageContainer = document.querySelector('.qr-image-container');
        imageContainer.innerHTML = '';
        imageContainer.appendChild(loadingDiv);
        
        // Disable download button while loading
        downloadBtn.disabled = true;
    }

    /**
     * Display the generated QR code
     * @param {string} url - The URL of the QR code image
     */
    function displayQRCode(url) {
        const imageContainer = document.querySelector('.qr-image-container');
        imageContainer.innerHTML = '';
        
        qrImage.src = url;
        qrImage.alt = 'Generated QR Code';
        imageContainer.appendChild(qrImage);
        
        // Enable download button
        downloadBtn.disabled = false;
        
        // Scroll to result
        resultContainer.scrollIntoView({ behavior: 'smooth' });
    }
});
