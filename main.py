"""
Main module to start the scheduler and run the application.
"""

import asyncio
from jobs.schedule_job import start_scheduler
# from scraper.scraper import scrape_job  # For testing
# from jobs.notify_job import notify_job # For testing


async def main():
    """
    Main asynchronous entry point for the application.
    Starts the scheduler and waits indefinitely.
    """
    start_scheduler()     # Starts the scheduler for the application
    # await scrape_job()  # For testing: triggers the scrape job manually
    # await notify_job()  # For testing: triggers the notify job manually
    await asyncio.Event().wait()    # to keep the program running

if __name__ == "__main__":
    asyncio.run(main())

