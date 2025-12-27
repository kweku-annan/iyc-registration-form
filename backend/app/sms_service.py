"""
SMS service integration using mNotify API.
Sends confirmation messages to registered attendees.
"""

import requests
import logging
import re
from .config import settings

# Set up logging
logger = logging.getLogger(__name__)


class SMSService:
    """
    Service class for sending SMS messages via mNotify API.
    mNotify is a Ghana-based SMS service provider.
    """
    
    def __init__(self):
        """Initialize mNotify service with API key from settings."""
        try:
            self.api_key = settings.mnotify_api_key
            self.endpoint = "https://api.mnotify.com/api/sms/quick"
            self.sender_id = "IYC-C 2025"  # mNotify sender ID (max 11 chars)
            logger.info("mNotify SMS service initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize mNotify service: {str(e)}")
            self.api_key = None
    
    def format_phone_number(self, phone: str) -> str:
        """
        Format phone number to Ghana format for mNotify.
        Converts to 0XXXXXXXXX format (local Ghana format).
        
        Args:
            phone: Phone number in various formats
            
        Returns:
            str: Phone number in 0XXXXXXXXX format
        """
        # Remove spaces, dashes, and other characters
        cleaned = re.sub(r'[\s\-\(\)]', '', phone)
        
        # Convert to local Ghana format (0XXXXXXXXX)
        if cleaned.startswith('+233'):
            # +233241234567 -> 0241234567
            return f"0{cleaned[4:]}"
        elif cleaned.startswith('233'):
            # 233241234567 -> 0241234567
            return f"0{cleaned[3:]}"
        elif cleaned.startswith('0'):
            # Already in correct format
            return cleaned
        else:
            # Unknown format, add 0 prefix
            logger.warning("Unknown phone format received, normalizing...")
            return f"0{cleaned}"
    
    def send_confirmation_sms(self, phone: str, name: str) -> tuple[bool, str]:
        """
        Send a confirmation SMS to the registered attendee via mNotify.
        
        Args:
            phone: Attendee's phone number
            name: Attendee's full name
            
        Returns:
            tuple: (success: bool, message: str)
        """
        if not self.api_key:
            error_msg = "SMS service not initialized. Check mNotify API key."
            logger.error(error_msg)
            return False, error_msg
        
        try:
            # Format phone number for Ghana
            to_number = self.format_phone_number(phone)
            
            # Get first name for personalization
            first_name = name.split()[0] if name else "Guest"
            
            # Create SMS message
            message_body = (
                f"Hello {first_name.upper()}!\n\n"
                f"Thank you for registering for {settings.conference_name}! "
                f"Your registration is confirmed.\n\n"
            )
            
            # Prepare mNotify API request
            url = f"{self.endpoint}?key={self.api_key}"
            data = {
                'recipient': [to_number],
                'sender': self.sender_id,
                'message': message_body,
                'is_schedule': False,
                'schedule_date': '',
            }
            
            # Send SMS via mNotify API
            response = requests.post(url, json=data)
            response_data = response.json()
            print(response_data)
            
            # Check response status
            if response_data.get('code') == '2000' or response_data.get('status') == 'success':
                logger.info("SMS sent successfully via mNotify")
                return True, f"SMS sent successfully to {to_number}"
            else:
                error_msg = response_data.get('message', response_data.get('message'))
                logger.error(f"mNotify API error: {error_msg}")
                return False, f"mNotify error: {error_msg}"
            
        except requests.exceptions.Timeout:
            error_msg = "Request timeout - mNotify API did not respond in time"
            logger.error(f"SMS request timeout: {error_msg}")
            return False, error_msg
            
        except requests.exceptions.RequestException as e:
            error_msg = f"Network error: {str(e)}"
            logger.error(f"SMS network error: {error_msg}")
            return False, error_msg
            
        except Exception as e:
            error_msg = f"Failed to send SMS: {str(e)}"
            logger.error(f"SMS unexpected error: {error_msg}")
            return False, error_msg


# Global instance
sms_service = SMSService()
