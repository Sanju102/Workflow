from apscheduler.schedulers.background import BackgroundScheduler
from django.conf import settings
from task.utils import check_overdue_tasks
import logging

logger = logging.getLogger(__name__)

def start():
    logger.info("Starting scheduler")
    scheduler = BackgroundScheduler(timezone=settings.TIME_ZONE)
    scheduler.add_job(check_overdue_tasks, 'interval', minutes=1)  # Run every minute for testing
    scheduler.start()
    logger.info("Scheduler started")