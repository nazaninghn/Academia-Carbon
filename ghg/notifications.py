# -*- coding: utf-8 -*-
"""
Notification system for Academia Carbon
Handles email notifications to admins and users
"""

from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib.auth.models import User
import logging

logger = logging.getLogger(__name__)


def send_material_request_notification(material_request):
    """
    Send email notification to admins when a new material is requested
    
    Args:
        material_request: MaterialRequest instance
    """
    try:
        # Get admin emails
        admin_emails = settings.ADMIN_NOTIFICATION_EMAILS
        
        # Also get superuser emails
        superuser_emails = list(User.objects.filter(is_superuser=True).values_list('email', flat=True))
        all_admin_emails = list(set(admin_emails + superuser_emails))
        
        # Remove empty emails
        all_admin_emails = [email for email in all_admin_emails if email]
        
        if not all_admin_emails:
            logger.warning("No admin emails configured for material request notifications")
            return False
        
        # Email subject
        subject = f'[{settings.SITE_NAME}] New Material Request: {material_request.material_name}'
        
        # Plain text message
        message = f"""
New Material Request Submitted

Material Name: {material_request.material_name}
Category: {material_request.category}
Requested by: {material_request.user.username} ({material_request.user.email})
Description: {material_request.description}

"""
        
        if material_request.suggested_factor:
            message += f"""
Suggested Emission Factor: {material_request.suggested_factor} {material_request.suggested_unit or 'kg CO2e/unit'}
Source: {material_request.suggested_source or 'Not provided'}

"""
        
        message += f"""
Please review this request in the admin panel:
{settings.SITE_URL}/admin/ghg/materialrequest/{material_request.id}/change/

---
Academia Carbon - Automated Notification
"""
        
        # Send email
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=all_admin_emails,
            fail_silently=False,
        )
        
        logger.info(f"Material request notification sent for: {material_request.material_name}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to send material request notification: {str(e)}")
        return False


def send_custom_factor_notification(custom_factor):
    """
    Send email notification to admins when a new custom factor is added
    (Optional - for high-value factors that need verification)
    
    Args:
        custom_factor: CustomEmissionFactor instance
    """
    try:
        # Get admin emails
        admin_emails = settings.ADMIN_NOTIFICATION_EMAILS
        superuser_emails = list(User.objects.filter(is_superuser=True).values_list('email', flat=True))
        all_admin_emails = list(set(admin_emails + superuser_emails))
        all_admin_emails = [email for email in all_admin_emails if email]
        
        if not all_admin_emails:
            return False
        
        subject = f'[{settings.SITE_NAME}] New Custom Emission Factor: {custom_factor.material_name}'
        
        message = f"""
New Custom Emission Factor Added

Material Name: {custom_factor.material_name}
Category: {custom_factor.category}
Emission Factor: {custom_factor.emission_factor} kg CO2e/{custom_factor.unit}
Added by: {custom_factor.user.username} ({custom_factor.user.email})

"""
        
        if custom_factor.supplier:
            message += f"Supplier: {custom_factor.supplier.name}\n"
        
        if custom_factor.source_reference:
            message += f"Source/Reference: {custom_factor.source_reference}\n"
        
        message += f"""

Please verify this custom factor in the admin panel:
{settings.SITE_URL}/admin/ghg/customemissionfactor/{custom_factor.id}/change/

---
Academia Carbon - Automated Notification
"""
        
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=all_admin_emails,
            fail_silently=False,
        )
        
        logger.info(f"Custom factor notification sent for: {custom_factor.material_name}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to send custom factor notification: {str(e)}")
        return False


def send_material_request_status_notification(material_request):
    """
    Send email to user when their material request status changes
    
    Args:
        material_request: MaterialRequest instance
    """
    try:
        user_email = material_request.user.email
        
        if not user_email:
            logger.warning(f"User {material_request.user.username} has no email address")
            return False
        
        status_messages = {
            'approved': 'has been approved! The emission factor has been added to the system.',
            'rejected': 'has been reviewed and unfortunately cannot be added at this time.',
            'in_progress': 'is currently being researched by our team.',
        }
        
        status_msg = status_messages.get(material_request.status, 'status has been updated.')
        
        subject = f'[{settings.SITE_NAME}] Material Request Update: {material_request.material_name}'
        
        message = f"""
Hello {material_request.user.first_name or material_request.user.username},

Your material request for "{material_request.material_name}" {status_msg}

Status: {material_request.get_status_display()}
"""
        
        if material_request.admin_notes:
            message += f"\nAdmin Notes:\n{material_request.admin_notes}\n"
        
        if material_request.status == 'approved' and material_request.system_source_key:
            message += f"""
You can now use this material in your calculations. Look for it in the emission source dropdown.
"""
        
        message += f"""

View your request:
{settings.SITE_URL}/history/

Thank you for using Academia Carbon!

---
Academia Carbon Team
"""
        
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user_email],
            fail_silently=False,
        )
        
        logger.info(f"Status notification sent to user for: {material_request.material_name}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to send status notification: {str(e)}")
        return False


def send_test_notification():
    """
    Send a test notification to verify email configuration
    """
    try:
        admin_emails = settings.ADMIN_NOTIFICATION_EMAILS
        
        send_mail(
            subject=f'[{settings.SITE_NAME}] Test Notification',
            message='This is a test notification from Academia Carbon. Email system is working correctly!',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=admin_emails,
            fail_silently=False,
        )
        
        return True
    except Exception as e:
        logger.error(f"Test notification failed: {str(e)}")
        return False
