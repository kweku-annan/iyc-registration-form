#!/bin/bash

# IYC Conference - SMS Test Script
# Tests mNotify API with sample registration data

echo "============================================================"
echo "IYC Conference - mNotify SMS Test"
echo "============================================================"
echo ""

# Load environment variables
if [ ! -f "backend/.env" ]; then
    echo "❌ Error: backend/.env file not found"
    exit 1
fi

# Source the .env file
source backend/.env

# Test configuration
PHONE_NUMBER="0554957158"  # Ghana format
NAME="Emmanuel"

echo "📋 Configuration:"
echo "   API Key: ${MNOTIFY_API_KEY:0:10}..."
echo "   Phone: $PHONE_NUMBER"
echo "   Name: $NAME"
echo ""

# Create message
MESSAGE="Hello $NAME!

Thank you for registering for $CONFERENCE_NAME! Your registration is confirmed.

Theme: Holy Spirit Invasion
Date: 24-27 Dec 2025
Location: The Prayer City, Apam Junction

Join WhatsApp: $WHATSAPP_GROUP_LINK

God bless you!"

echo "💬 Message Preview:"
echo "-----------------------------------------------------------"
echo "$MESSAGE"
echo "-----------------------------------------------------------"
echo ""

# Send SMS via mNotify
echo "📤 Sending SMS via mNotify API..."
echo ""

RESPONSE=$(curl -s -X POST "https://api.mnotify.com/api/sms/quick?key=$MNOTIFY_API_KEY" \
  -d "recipient[]=$PHONE_NUMBER" \
  -d "sender=IYC-C 2025" \
  -d "message=$MESSAGE")

echo "📥 API Response:"
echo "$RESPONSE" | jq . 2>/dev/null || echo "$RESPONSE"
echo ""

# Check response
if echo "$RESPONSE" | grep -q '"code":"2000"' || echo "$RESPONSE" | grep -q '"status":"success"'; then
    echo "✅ SMS sent successfully!"
else
    echo "❌ SMS failed!"
    echo ""
    echo "💡 Troubleshooting:"
    echo "   1. Check if MNOTIFY_API_KEY is correct in backend/.env"
    echo "   2. Verify you have SMS credits in your mNotify account"
    echo "   3. Check if sender ID 'IYC-C 2025' is registered"
    echo "   4. Ensure phone number format is correct (0XXXXXXXXX)"
    echo "   5. Visit https://dashboard.mnotify.com/ to check your account"
fi

echo ""
echo "============================================================"
