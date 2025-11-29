import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from backend_app import create_app
from backend_app.celery import celery_app

flask_app = create_app()
app = celery_app    # Celery CLI yahi app use karega
