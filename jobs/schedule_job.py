"""
This module defines and starts job scheduling using AsyncIOScheduler
from APScheduler. It includes jobs for scraping and sending notifications.
"""

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from scraper.scraper import scrape_job
from jobs.notify_job import notify_job


# 爬蟲執行的時間
def get_scrape_times() -> list:
    """
    Define the schedule for scrape jobs to run every hour at 55 minutes.
    """
    scrape_times = []
    for hour in range(24):
        scrape_times.append((hour, 55))
    return scrape_times


# 發送訊息的時間
def get_notify_times() -> list:
    """
    Define the schedule for notification jobs.
    """    
    return [
        (0, 0)
    ]

# 設置爬蟲的排程
def schedule_scrape_jobs(scheduler: AsyncIOScheduler):
    """
    Schedule the scraping jobs.
    """    
    scrape_times = get_scrape_times()
    for hour, minute in scrape_times:
        scheduler.add_job(
            scrape_job,
            CronTrigger(hour=hour, minute=minute),
            misfire_grace_time=60
        )

# 設置發送訊息的排程
def schedule_notify_jobs(scheduler: AsyncIOScheduler):
    """
    Schedule the notification jobs.
    """    
    notify_times = get_notify_times()
    for hour, minute in notify_times:
        scheduler.add_job(
            notify_job,
            CronTrigger(hour=hour, minute=minute),
            misfire_grace_time=60
        )

def start_scheduler():
    """
    Start the scheduler with scraping and notification jobs.
    """    
    scheduler = AsyncIOScheduler()
    schedule_scrape_jobs(scheduler)
    schedule_notify_jobs(scheduler)
    scheduler.start()
