from __future__ import annotations

from celery import Celery

from core.settings import env


DJANGO_SETTINGS_MODULE = env("DJANGO_SETTINGS_MODULE", default="core.settings")

celery_app = Celery("core")
celery_app.config_from_object("django.conf:settings", namespace="CELERY")

celery_app.autodiscover_tasks()


@celery_app.task(bind=True)
def debug_task(self):
    print(f"Request: {self.request!r}")
