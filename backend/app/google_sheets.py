"""
Google Sheets integration for storing registration data.
Uses gspread library with service account authentication.
"""

import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
from typing import Optional
import logging
from .config import settings

# Set up logging
logger = logging.getLogger(__name__)


class GoogleSheetsService:
    """
    Service class for interacting with Google Sheets API.
    """
    
    def __init__(self):
        """Initialize the Google Sheets client with service account credentials."""
        self.credentials_path = settings.google_sheets_credentials_path
        self.sheet_id = settings.google_sheet_id
        self.client: Optional[gspread.Client] = None
        self.worksheet = None
    
    def authenticate(self):
        """
        Authenticate with Google Sheets API using service account credentials.
        
        Setup instructions:
        1. Go to Google Cloud Console: https://console.cloud.google.com/
        2. Create a new project or select existing one
        3. Enable Google Sheets API
        4. Create service account credentials
        5. Download JSON key file
        6. Share your Google Sheet with the service account email
        """
        try:
            scope = [
                'https://spreadsheets.google.com/feeds',
                'https://www.googleapis.com/auth/drive'
            ]
            
            creds = ServiceAccountCredentials.from_json_keyfile_name(
                self.credentials_path,
                scope
            )
            
            self.client = gspread.authorize(creds)
            logger.info("Successfully authenticated with Google Sheets API")
            
        except FileNotFoundError:
            logger.error("Credentials file not found")
            raise Exception(f"Google Sheets credentials file not found. Please check {self.credentials_path}")
        except Exception as e:
            logger.error(f"Failed to authenticate with Google Sheets: {str(e)}")
            raise Exception(f"Google Sheets authentication failed: {str(e)}")
    
    def get_worksheet(self):
        """Open the Google Sheet and get the first worksheet."""
        try:
            if not self.client:
                self.authenticate()
            
            sheet = self.client.open_by_key(self.sheet_id)
            self.worksheet = sheet.get_worksheet(0)  # Get first sheet
            logger.info(f"Successfully opened Google Sheet: {sheet.title}")
            
        except gspread.SpreadsheetNotFound:
            logger.error("Spreadsheet not found - check configuration")
            raise Exception(
                "Google Sheet not found. Please check:\n"
                "1. The GOOGLE_SHEET_ID in your .env file\n"
                "2. The sheet is shared with your service account email"
            )
        except Exception as e:
            logger.error(f"Failed to open Google Sheet: {str(e)}")
            raise Exception(f"Failed to open Google Sheet: {str(e)}")
    
    def append_registration(self, registration_data: dict) -> bool:
        """
        Append a new registration to the Google Sheet.
        
        Args:
            registration_data: Dictionary containing registration form data
            
        Returns:
            bool: True if successful, raises exception otherwise
        """
        try:
            if not self.worksheet:
                self.get_worksheet()
            
            # Create headers if sheet is empty
            if self.worksheet.row_count == 0 or not self.worksheet.row_values(1):
                headers = [
                    'Timestamp',
                    'Full Name',
                    'Phone',
                    'Church',
                    'Institution',
                    'City/Location',
                    'Leader/Inviter',
                    'Email',
                    'Contact Method',
                    'First-Time Attendee',
                    'Prayer Request',
                    'Status'
                ]
                self.worksheet.append_row(headers)
                logger.info("Created headers in Google Sheet")
            
            # Prepare row data
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            row_data = [
                timestamp,
                registration_data.get('full_name', ''),
                registration_data.get('phone', ''),
                registration_data.get('church', ''),
                registration_data.get('institution', ''),
                registration_data.get('city', ''),
                registration_data.get('leader', ''),
                registration_data.get('email', ''),
                registration_data.get('contact_method', ''),
                registration_data.get('first_time_attendee', ''),
                registration_data.get('prayer_request', ''),
                'Success'
            ]
            
            # Append the row
            self.worksheet.append_row(row_data)
            logger.info("Successfully added registration to Google Sheets")
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to append registration to Google Sheets: {str(e)}")
            # Mark as failed in sheet if possible
            try:
                row_data[-1] = 'Failed'
                self.worksheet.append_row(row_data)
            except:
                pass
            raise Exception(f"Failed to save to Google Sheets: {str(e)}")


# Global instance
sheets_service = GoogleSheetsService()
