#!/usr/bin/env python3
"""
SMS Service Test Script
Tests the mNotify SMS service with sample registration data.
"""

import sys
import os

# Add backend directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from app.sms_service import sms_service
from app.config import settings

def test_sms_service():
    """Test the SMS service configuration and send a test message."""
    
    print("=" * 60)
    print("IYC Conference - SMS Service Test")
    print("=" * 60)
    print()
    
    # Test data
    test_phone = "+233554957158"
    test_name = "Emmanuel Adu Saah"
    
    # Check configuration
    print("📋 Configuration Check:")
    print(f"   mNotify API Key: {'✅ Set' if sms_service.api_key else '❌ Not Set'}")
    print(f"   Endpoint: {sms_service.endpoint}")
    print(f"   Sender ID: {sms_service.sender_id}")
    print(f"   Conference Name: {settings.conference_name}")
    print(f"   WhatsApp Link: {settings.whatsapp_group_link}")
    print()
    
    # Format phone number
    formatted_phone = sms_service.format_phone_number(test_phone)
    print(f"📱 Phone Number:")
    print(f"   Original: {test_phone}")
    print(f"   Formatted: {formatted_phone}")
    print()
    
    # Show message preview
    first_name = test_name.split()[0]
    message_preview = (
        f"Hello {first_name.upper()}!\\n\\n"
        f"Thank you for registering for {settings.conference_name}! "
        f"Your registration is confirmed.\\n\\n"
        f"Theme: Holy Spirit Invasion\\n"
        f"Date: 24-27 Dec 2025\\n"
        f"Location: The Prayer City, Apam Junction\\n\\n"
        f"Join WhatsApp: {settings.whatsapp_group_link}\\n\\n"
        f"God bless you!"
    )
    
    print("💬 Message Preview:")
    print("-" * 60)
    print(message_preview)
    print("-" * 60)
    print(f"Message Length: {len(message_preview)} characters")
    print()
    
    # Send test SMS
    print("📤 Sending Test SMS...")
    success, message = sms_service.send_confirmation_sms(test_phone, test_name)
    
    print()
    if success:
        print("✅ SUCCESS!")
        print(f"   {message}")
    else:
        print("❌ FAILED!")
        print(f"   Error: {message}")
        print()
        print("💡 Troubleshooting Tips:")
        print("   1. Check if mNotify API key is correct in .env file")
        print("   2. Verify you have sufficient SMS credits in mNotify")
        print("   3. Ensure the sender ID 'IYC-C 2025' is approved")
        print("   4. Check if the phone number is valid and active")
        print("   5. Review mNotify API documentation for error codes")
    
    print()
    print("=" * 60)

if __name__ == "__main__":
    test_sms_service()
