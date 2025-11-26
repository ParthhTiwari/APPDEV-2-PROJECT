import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('FLASK_ENV', 'development')

from backend_app import create_app
flask_app = create_app()
celery = flask_app.celery
app = celery