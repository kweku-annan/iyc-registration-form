"""
API routes for conference registration.
"""

from fastapi import APIRouter, HTTPException, Request
from slowapi import Limiter
from slowapi.util import get_remote_address
import logging
import html
from .models import RegistrationRequest, RegistrationResponse
from .google_sheets import sheets_service
from .sms_service import sms_service

# Set up logging
logger = logging.getLogger(__name__)

# Set up rate limiter
limiter = Limiter(key_func=get_remote_address)

# Create router
router = APIRouter(prefix="/api", tags=["registration"])


def sanitize_input(text: str) -> str:
    """
    Sanitize user input to prevent injection attacks.
    Escapes HTML and removes potentially dangerous characters.
    """
    if not text:
        return ""
    # Escape HTML
    sanitized = html.escape(text.strip())
    return sanitized


@router.post("register", response_model=RegistrationResponse)
@limiter.limit("5/minute")  # Max 5 registrations per minute per IP
async def register_attendee(request: Request, registration: RegistrationRequest):
    """
    Register a new conference attendee.
    
    This endpoint:
    1. Validates the registration data
    2. Sanitizes all inputs
    3. Saves to Google Sheets
    4. Sends SMS confirmation (non-blocking, errors logged but don't fail registration)
    5. Returns success response
    
    Rate limited to 5 requests per minute per IP address.
    """
    try:
        logger.info("Processing new registration")
        
        # Sanitize all text inputs
        sanitized_data = {
            'full_name': sanitize_input(registration.full_name),
            'church': sanitize_input(registration.church),
            'city': sanitize_input(registration.city),
            'phone': sanitize_input(registration.phone) if registration.phone else '',
            'institution': sanitize_input(registration.institution) if registration.institution else '',
            'leader': sanitize_input(registration.leader) if registration.leader else '',
            'email': registration.email if registration.email else '',
            'contact_method': registration.contact_method if registration.contact_method else '',
            'first_time_attendee': registration.first_time_attendee if registration.first_time_attendee else '',
            'prayer_request': sanitize_input(registration.prayer_request) if registration.prayer_request else '',
        }
        
        # Save to Google Sheets
        try:
            sheets_service.append_registration(sanitized_data)
            logger.info("Registration saved to Google Sheets successfully")
        except Exception as e:
            logger.error(f"Failed to save to Google Sheets: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail={
                    "message": "Failed to save registration. Please try again or contact support.",
                    "error": "google_sheets_error"
                }
            )
        
        # Send SMS confirmation (non-blocking - don't fail registration if SMS fails)
        sms_sent = False
        sms_message = ""
        if sanitized_data.get('phone'):
            try:
                sms_sent, sms_message = sms_service.send_confirmation_sms(
                    sanitized_data['phone'],
                    sanitized_data['full_name']
                )
                if sms_sent:
                    logger.info("SMS confirmation sent successfully")
                else:
                    logger.warning(f"SMS failed but registration succeeded: {sms_message}")
            except Exception as e:
                logger.error(f"SMS service error (non-critical): {str(e)}")
                sms_message = str(e)
        else:
            sms_message = "No phone number provided"
        
        # Return success response
        return RegistrationResponse(
            success=True,
            message=f"Registration successful! Welcome, {sanitized_data['full_name']}!",
            data={
                'name': sanitized_data['full_name'],
                'sms_sent': sms_sent,
                'sms_message': sms_message if not sms_sent else 'Confirmation SMS sent successfully'
            }
        )
        
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        logger.error(f"Unexpected error during registration: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail={
                "message": "An unexpected error occurred. Please try again.",
                "error": "internal_server_error"
            }
        )


@router.get("/health", response_model=dict)
async def health_check():
    """
    Health check endpoint to verify service status.
    
    Checks:
    - API is running
    - Google Sheets connectivity
    - SMS service initialization
    """
    health_status = {
        "status": "healthy",
        "services": {
            "api": "operational",
            "google_sheets": "unknown",
            "sms": "unknown"
        }
    }
    
    # Check Google Sheets
    try:
        sheets_service.authenticate()
        sheets_service.get_worksheet()
        health_status["services"]["google_sheets"] = "operational"
    except Exception as e:
        logger.error(f"Google Sheets health check failed: {str(e)}")
        health_status["services"]["google_sheets"] = f"error: {str(e)}"
        health_status["status"] = "degraded"
    
    # Check SMS service
    if sms_service.client:
        health_status["services"]["sms"] = "operational"
    else:
        health_status["services"]["sms"] = "not_initialized"
        health_status["status"] = "degraded"
    
    return health_status
