from celery import Celery

celery_app = Celery(
    "mad_project",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0",
)

# Celery configuration 
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
)

from flask import Flask

class ContextTask(celery_app.Task):
    def __call__(self, *args, **kwargs):
        # Flask app context  dynamically import 
        # circular import avoid

        from backend_app import create_app
        app = create_app()
        with app.app_context():
            return self.run(*args, **kwargs)

celery_app.Task = ContextTask
