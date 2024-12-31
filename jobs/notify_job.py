"""
This module defines a job for sending notifications.
"""

from messages.sender import send_notifications

async def notify_job():
    """
    Asynchronous job to send notifications.
    """    
    await send_notifications()
