import cv2
import validators
from pyzbar.pyzbar import decode
from PIL import Image
import re

def classify_qr_data(data):
    if validators.url(data):
        if any(short in data for short in ['bit.ly', 'tinyurl', 't.co']):
            return 'Shortened URL - ⚠️ Possibly risky'
        elif 'wa.me/' in data or 'api.whatsapp.com' in data:
            return 'WhatsApp Chat Link'
        elif 'upi:' in data:
            return 'UPI Payment Link'
        return 'Website URL'
    elif data.startswith('tel:'):
        return 'Phone Number'
    elif data.startswith('mailto:'):
        return 'Email Link'
    elif 'WIFI:' in data:
        return 'Wi-Fi Configuration'
    elif 'BEGIN:VCARD' in data:
        return 'Contact Card (vCard)'
    elif re.match(r'\d{10}$', data):
        return 'Plain Phone Number'
    else:
        return 'Plain Text or Unknown Format'

def check_safety(data):
    if any(x in data for x in ['bit.ly', 'tinyurl', 't.co']):
        return "⚠️ Suspicious: Shortened URL"
    elif validators.url(data):
        domain = data.split("//")[-1].split("/")[0]
        return f"✅ Safe-looking URL (domain: {domain})"
    else:
        return "ℹ️ Cannot determine safety - not a URL"

def scan_qr_from_image(image_path):
    img = cv2.imread(image_path)
    decoded_objects = decode(img)

    if not decoded_objects:
        return "No QR code found."

    results = []
    for obj in decoded_objects:
        data = obj.data.decode('utf-8')
        qr_type = classify_qr_data(data)
        safety = check_safety(data)
        results.append({
            'data': data,
            'type': qr_type,
            'safety': safety
        })
    return results
