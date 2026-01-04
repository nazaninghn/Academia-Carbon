"""
Email notification system for industry requests and other admin notifications
"""
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import logging

logger = logging.getLogger(__name__)

def send_industry_request_notification(industry_request):
    """Send email notification to admin when new industry is requested"""
    try:
        # Admin email addresses (you can configure this in settings)
        admin_emails = getattr(settings, 'ADMIN_NOTIFICATION_EMAILS', ['admin@academiacarbon.com'])
        
        if not admin_emails:
            logger.warning("No admin emails configured for industry request notifications")
            return False
        
        subject = f'New Industry Request: {industry_request.industry_name}'
        
        # Create email content
        context = {
            'industry_request': industry_request,
            'user': industry_request.user,
            'admin_url': f'{settings.SITE_URL}/admin/ghg/industryrequest/{industry_request.id}/change/' if hasattr(settings, 'SITE_URL') else '#'
        }
        
        # HTML email content
        html_message = f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                <h2 style="color: #22c55e; border-bottom: 2px solid #22c55e; padding-bottom: 10px;">
                    🏭 New Industry Type Request
                </h2>
                
                <div style="background: #f8f9fa; padding: 20px; border-radius: 8px; margin: 20px 0;">
                    <h3 style="margin-top: 0; color: #333;">Industry Details:</h3>
                    <p><strong>Name:</strong> {industry_request.industry_name}</p>
                    {f'<p><strong>Code:</strong> {industry_request.industry_code}</p>' if industry_request.industry_code else ''}
                    <p><strong>Description:</strong> {industry_request.description}</p>
                    {f'<p><strong>Business Context:</strong> {industry_request.business_context}</p>' if industry_request.business_context else ''}
                </div>
                
                <div style="background: #e0f2fe; padding: 20px; border-radius: 8px; margin: 20px 0;">
                    <h3 style="margin-top: 0; color: #333;">Requested By:</h3>
                    <p><strong>User:</strong> {industry_request.user.get_full_name() or industry_request.user.username}</p>
                    <p><strong>Email:</strong> {industry_request.user.email}</p>
                    <p><strong>Date:</strong> {industry_request.created_at.strftime('%Y-%m-%d %H:%M')}</p>
                </div>
                
                <div style="text-align: center; margin: 30px 0;">
                    <a href="{context['admin_url']}" 
                       style="background: #22c55e; color: white; padding: 12px 24px; text-decoration: none; border-radius: 8px; font-weight: bold;">
                        Review in Admin Panel
                    </a>
                </div>
                
                <hr style="border: none; border-top: 1px solid #e0e0e0; margin: 30px 0;">
                <p style="font-size: 12px; color: #666; text-align: center;">
                    This is an automated notification from Academia Carbon Tracker
                </p>
            </div>
        </body>
        </html>
        """
        
        # Plain text version
        plain_message = f"""
New Industry Type Request

Industry Details:
- Name: {industry_request.industry_name}
{f'- Code: {industry_request.industry_code}' if industry_request.industry_code else ''}
- Description: {industry_request.description}
{f'- Business Context: {industry_request.business_context}' if industry_request.business_context else ''}

Requested By:
- User: {industry_request.user.get_full_name() or industry_request.user.username}
- Email: {industry_request.user.email}
- Date: {industry_request.created_at.strftime('%Y-%m-%d %H:%M')}

Please review this request in the admin panel: {context['admin_url']}
        """
        
        # Send email
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=admin_emails,
            html_message=html_message,
            fail_silently=False,
        )
        
        logger.info(f"Industry request notification sent for: {industry_request.industry_name}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to send industry request notification: {str(e)}")
        return False


def send_industry_status_notification(industry_request):
    """Send email to user when their industry request status changes"""
    try:
        if not industry_request.user.email:
            logger.warning(f"No email address for user {industry_request.user.username}")
            return False
        
        status_messages = {
            'approved': {
                'subject': f'✅ Your industry request "{industry_request.industry_name}" has been approved!',
                'color': '#22c55e',
                'icon': '✅',
                'message': 'Great news! Your industry type request has been approved and added to our system.'
            },
            'rejected': {
                'subject': f'❌ Your industry request "{industry_request.industry_name}" needs revision',
                'color': '#ef4444',
                'icon': '❌',
                'message': 'Your industry type request needs some adjustments before we can approve it.'
            }
        }
        
        status_info = status_messages.get(industry_request.status)
        if not status_info:
            return False
        
        # HTML email content
        html_message = f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                <h2 style="color: {status_info['color']}; border-bottom: 2px solid {status_info['color']}; padding-bottom: 10px;">
                    {status_info['icon']} Industry Request Update
                </h2>
                
                <p>Hello {industry_request.user.get_full_name() or industry_request.user.username},</p>
                
                <p>{status_info['message']}</p>
                
                <div style="background: #f8f9fa; padding: 20px; border-radius: 8px; margin: 20px 0;">
                    <h3 style="margin-top: 0;">Your Request:</h3>
                    <p><strong>Industry Name:</strong> {industry_request.industry_name}</p>
                    <p><strong>Status:</strong> <span style="color: {status_info['color']}; font-weight: bold;">{industry_request.get_status_display()}</span></p>
                    <p><strong>Submitted:</strong> {industry_request.created_at.strftime('%Y-%m-%d')}</p>
                </div>
                
                {f'''
                <div style="background: #fff3cd; padding: 15px; border-radius: 8px; margin: 20px 0; border-left: 4px solid #ffc107;">
                    <h4 style="margin-top: 0; color: #856404;">Admin Notes:</h4>
                    <p style="margin-bottom: 0;">{industry_request.admin_notes}</p>
                </div>
                ''' if industry_request.admin_notes else ''}
                
                <hr style="border: none; border-top: 1px solid #e0e0e0; margin: 30px 0;">
                <p style="font-size: 12px; color: #666; text-align: center;">
                    Thank you for using Academia Carbon Tracker
                </p>
            </div>
        </body>
        </html>
        """
        
        # Plain text version
        plain_message = f"""
Industry Request Update

Hello {industry_request.user.get_full_name() or industry_request.user.username},

{status_info['message']}

Your Request:
- Industry Name: {industry_request.industry_name}
- Status: {industry_request.get_status_display()}
- Submitted: {industry_request.created_at.strftime('%Y-%m-%d')}

{f'Admin Notes: {industry_request.admin_notes}' if industry_request.admin_notes else ''}

Thank you for using Academia Carbon Tracker
        """
        
        # Send email
        send_mail(
            subject=status_info['subject'],
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[industry_request.user.email],
            html_message=html_message,
            fail_silently=False,
        )
        
        logger.info(f"Status notification sent to {industry_request.user.email} for industry: {industry_request.industry_name}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to send status notification: {str(e)}")
        return False