"""
Celery tasks for file processing.
"""

from celery import shared_task
from django.conf import settings
from ideas.models import Document
import logging
import pyclamav

logger = logging.getLogger(__name__)


@shared_task(bind=True, max_retries=3)
def scan_uploaded_file(self, document_id):
    """Scan uploaded file for viruses."""
    try:
        document = Document.objects.get(id=document_id)
        
        logger.info(f"Scanning file: {document.file_name}")
        
        # Initialize ClamAV
        clam = pyclamav.ClamAV(
            settings.CLAMAV_HOST,
            settings.CLAMAV_PORT
        )
        
        # Scan file
        result = clam.scan_file(document.file_path)
        
        if result[0] == 1:  # Virus found
            logger.warning(f"Virus detected in file: {document.file_name}")
            document.virus_scan_status = 'INFECTED'
            document.save()
            
            # Delete infected file
            from common.utils import delete_file_from_s3
            delete_file_from_s3(document.file_path)
            
            return f"Virus detected in {document.file_name}"
        
        else:  # File is clean
            logger.info(f"File is clean: {document.file_name}")
            document.virus_scan_status = 'CLEAN'
            document.save()
            
            return f"File {document.file_name} is clean"
    
    except Document.DoesNotExist:
        logger.error(f"Document not found: {document_id}")
        return f"Document {document_id} not found"
    
    except Exception as exc:
        logger.error(f"Error scanning file: {str(exc)}")
        # Retry with exponential backoff
        raise self.retry(exc=exc, countdown=60 * (2 ** self.request.retries))


@shared_task
def process_file_upload(document_id):
    """Process uploaded file."""
    try:
        document = Document.objects.get(id=document_id)
        
        logger.info(f"Processing file upload: {document.file_name}")
        
        # Scan file for viruses
        scan_uploaded_file.delay(document_id)
        
        logger.info(f"File upload processed: {document.file_name}")
    
    except Document.DoesNotExist:
        logger.error(f"Document not found: {document_id}")
    
    except Exception as e:
        logger.error(f"Error processing file upload: {str(e)}")


@shared_task
def cleanup_old_files():
    """Clean up old uploaded files."""
    try:
        from datetime import timedelta
        from django.utils import timezone
        
        # Delete files older than 30 days
        cutoff_date = timezone.now() - timedelta(days=30)
        old_documents = Document.objects.filter(uploaded_at__lt=cutoff_date)
        
        for document in old_documents:
            from common.utils import delete_file_from_s3
            delete_file_from_s3(document.file_path)
            document.delete()
        
        logger.info(f"Cleaned up {old_documents.count()} old files")
    
    except Exception as e:
        logger.error(f"Error cleaning up old files: {str(e)}")
