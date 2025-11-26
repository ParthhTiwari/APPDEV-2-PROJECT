from celery import Celery

def make_celery(flask_app):
    """Create Celery instance bound to Flask app."""
    celery = Celery(
        flask_app.import_name,
        backend=flask_app.config.get('CELERY_RESULT_BACKEND', 'redis://localhost:6379/0'),
        broker=flask_app.config.get('CELERY_BROKER_URL', 'redis://localhost:6379/0')
    )

    celery.conf.update(
        task_serializer='json',
        accept_content=['json'],
        result_serializer='json',
        timezone='UTC',
        enable_utc=True,
    )

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with flask_app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery