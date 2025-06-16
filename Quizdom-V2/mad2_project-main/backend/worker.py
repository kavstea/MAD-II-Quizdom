from celery import Celery, Task
from flask import Flask
from celery.schedules import crontab

# ------------------------------
# Celery Configuration Settings
# ------------------------------
class CeleryConfig:
    broker_url = "redis://localhost:6379/0"      # Redis as message broker (queue)
    result_backend = "redis://localhost:6379/1"  # Redis for storing task results
    timezone = "Asia/Kolkata"                    # Timezone for scheduled tasks
    enable_utc = True                            # Use UTC time internally
    
    # Scheduled tasks configuration
    beat_schedule = {
        # Test task: runs every 10 seconds
        "add-every-10-seconds": {
            "task": "backend.task.daily_reminder",  # Task to execute
            "schedule": 10.0,                      # Run every 10 seconds
            #"schedule": crontab(minute=0, hour=8),  # Prod: 8 AM daily
        },
        # Monthly report task (currently set to test mode)
        "send-monthly-report": {
            "task": "backend.task.send_monthly_report",
            "schedule": crontab(minute='*'),        # Run every minute (testing)
            #"schedule": crontab(minute=0, hour=8, day_of_month=1),  # Prod: 8 AM on 1st of month
        },
    }

# ------------------------------
# Celery Application Factory
# ------------------------------
def celery_init_app(app: Flask) -> Celery:
    # Custom task class to ensure Flask app context
    class FlaskTask(Task):
        def __call__(self, *args: object, **kwargs: object) -> object:
            with app.app_context():  # Run tasks within Flask context
                return self.run(*args, **kwargs)

    # Create Celery instance with Flask integration
    celery_app = Celery(app.name, task_cls=FlaskTask)
    celery_app.config_from_object(CeleryConfig)  # Apply configuration
    celery_app.set_default()
    app.extensions["celery"] = celery_app  # Attach Celery to Flask app
    return celery_app

