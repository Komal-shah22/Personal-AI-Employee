#!/usr/bin/env python3
"""
Simple script to send WhatsApp message to +923170027046
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import the send function from the existing script
from send_whatsapp_direct import send_whatsapp_direct
import json

def main():
    phone = "+923170027046"

    # Create a random message
    import random
    messages = [
        "Hello! This is a test message from your AI assistant.",
        "Hi there! Just checking in to see how you're doing.",
        "Greetings! This is an automated message from your personal AI employee.",
        "Hello! Sending you a friendly message from your AI assistant.",
        "Hi! This is a sample message sent automatically by AI."
    ]

    message = random.choice(messages)

    print(f"Attempting to send message to {phone}...")
    print(f"Message: {message}")

    result = send_whatsapp_direct(phone, message)

    print("Result:", json.dumps(result, indent=2))

if __name__ == "__main__":
    main()