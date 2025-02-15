from application.workers import celery
from celery.schedules import crontab
from application.models import *
from application.household_email_config import send_email


@celery.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        # crontab(minute=0, hour=16),
        crontab(),
        daily_reminder.s(),
        name="daily reminder"
    )

    sender.add_periodic_task(
        crontab(0,0,day_of_month=1),
        monthly_report.s(),
        name="monthly report"
    )





@celery.task()
def daily_reminder():
    professionals = Professional.query.all()
    for professional in professionals:
        message = "Hello, this is a daily reminder to check in with your professional."
        username = professional.professional_name  # Assuming this is the username without email domain
        to_email = f"{username}@gmail.com"
        send_email(to=to_email, sub="Daily Reminder", message=message)
        print("Daily reminder sent to", to_email)
   
    return( "Daily reminders sent successfully")




@celery.task()
def monthly_report():
    professionals = Professional.query.all()
    for professional in professionals:
        message = "Hello, this is a monthly report to check in with your professional."
        username = professional.professional_name  # Assuming this is the username without email domain
        to_email = f"{username}@gmail.com"
        send_email(to=to_email, sub="monthly report", message=message)
        print("monthly report sent to", to_email)

    return "monthly reports sent successfully"
