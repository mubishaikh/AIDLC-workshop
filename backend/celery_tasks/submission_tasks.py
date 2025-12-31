"""
Celery tasks for idea submission processing.
"""

from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from ideas.models import Idea
import logging

logger = logging.getLogger(__name__)


@shared_task(bind=True, max_retries=3)
def process_idea_submission(self, idea_id):
    """Process idea submission asynchronously."""
    try:
        idea = Idea.objects.get(id=idea_id)
        
        # Log submission
        logger.info(f"Processing idea submission: {idea.id}")
        
        # Send confirmation email
        send_submission_confirmation_email(idea)
        
        # Update idea status
        idea.status = 'SUBMITTED'
        idea.save()
        
        logger.info(f"Idea submission processed: {idea.id}")
        return f"Idea {idea.id} submitted successfully"
    
    except Idea.DoesNotExist:
        logger.error(f"Idea not found: {idea_id}")
        return f"Idea {idea_id} not found"
    
    except Exception as exc:
        logger.error(f"Error processing idea submission: {str(exc)}")
        # Retry with exponential backoff
        raise self.retry(exc=exc, countdown=60 * (2 ** self.request.retries))


@shared_task
def send_submission_confirmation_email(idea):
    """Send confirmation email to submitter."""
    try:
        subject = f"Idea Submitted: {idea.title}"
        message = f"""
        Dear {idea.submitter.first_name},
        
        Your idea "{idea.title}" has been successfully submitted for evaluation.
        
        Idea ID: {idea.id}
        Campaign: {idea.campaign.name}
        
        You can track the status of your idea in the dashboard.
        
        Best regards,
        Ideation Portal Team
        """
        
        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [idea.submitter.email],
            fail_silently=False,
        )
        
        logger.info(f"Confirmation email sent to {idea.submitter.email}")
    
    except Exception as e:
        logger.error(f"Failed to send confirmation email: {str(e)}")


@shared_task
def send_contributor_notification(idea_id, contributor_id):
    """Send notification to new contributor."""
    try:
        from django.contrib.auth.models import User
        
        idea = Idea.objects.get(id=idea_id)
        contributor = User.objects.get(id=contributor_id)
        
        subject = f"You've been added as a contributor to: {idea.title}"
        message = f"""
        Dear {contributor.first_name},
        
        You have been added as a contributor to the idea "{idea.title}".
        
        Idea ID: {idea.id}
        Campaign: {idea.campaign.name}
        
        You can now collaborate on this idea in the dashboard.
        
        Best regards,
        Ideation Portal Team
        """
        
        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [contributor.email],
            fail_silently=False,
        )
        
        logger.info(f"Contributor notification sent to {contributor.email}")
    
    except Exception as e:
        logger.error(f"Failed to send contributor notification: {str(e)}")
