# Ideation Portal Backend
__version__ = "1.0.0"

# Import Celery app for Django
from .celery import app as celery_app

__all__ = ['celery_app']
