"""
Pydantic models for request/response validation.
"""

from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional
import re


class RegistrationRequest(BaseModel):
    """
    Model for validating conference registration form data.
    """
    
    # Required fields
    full_name: str = Field(..., min_length=2, max_length=100, description="Full name of the attendee")
    church: str = Field(..., min_length=2, max_length=100, description="Church name")
    city: str = Field(..., min_length=2, max_length=100, description="City or location")
    
    # Optional fields
    phone: Optional[str] = Field(None, min_length=10, max_length=15, description="Phone number in Ghana format")
    institution: Optional[str] = Field(None, min_length=2, max_length=150, description="School or institution name")
    leader: Optional[str] = Field(None, min_length=2, max_length=100, description="Name of person who invited or leader")
    email: Optional[EmailStr] = Field(None, description="Email address (optional)")
    contact_method: Optional[str] = Field(None, description="Preferred contact method")
    first_time_attendee: Optional[str] = Field(None, description="First-time attendee (Yes/No)")
    prayer_request: Optional[str] = Field(None, max_length=500, description="Prayer request")
    
    # Privacy consent (required)
    privacy_consent: bool = Field(..., description="User must consent to data collection")
    
    @field_validator('phone')
    @classmethod
    def validate_ghana_phone(cls, v: Optional[str]) -> Optional[str]:
        """
        Validate phone number accepts common Ghana formats:
        - 0241234567 (10 digits starting with 0)
        - +233241234567 (international format)
        - 233241234567 (international without +)
        """
        # Allow None/empty for optional field
        if not v:
            return v
            
        # Remove spaces and dashes
        cleaned = re.sub(r'[\s\-]', '', v)
        
        # Check various Ghana phone formats
        patterns = [
            r'^0\d{9}$',           # 0241234567
            r'^\+233\d{9}$',       # +233241234567
            r'^233\d{9}$',         # 233241234567
        ]
        
        if not any(re.match(pattern, cleaned) for pattern in patterns):
            raise ValueError('Phone number must be in Ghana format (e.g., 0241234567 or +233241234567)')
        
        return cleaned
    
    @field_validator('privacy_consent')
    @classmethod
    def validate_consent(cls, v: bool) -> bool:
        """Ensure privacy consent is explicitly given."""
        if not v:
            raise ValueError('You must agree to the privacy terms to register')
        return v
    
    @field_validator('contact_method')
    @classmethod
    def validate_contact_method(cls, v: Optional[str]) -> Optional[str]:
        """Validate contact method is one of the allowed options."""
        if v and v not in ['Phone', 'Email', 'WhatsApp']:
            raise ValueError('Contact method must be one of: Phone, Email, WhatsApp')
        return v


class RegistrationResponse(BaseModel):
    """
    Standard API response model.
    """
    success: bool
    message: str
    data: Optional[dict] = None
