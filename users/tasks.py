from celery import shared_task
from django.core.mail import send_mail

@shared_task
def send_welcome_email_task(user_email):
    send_mail(
        'Welcome to InstaApp!',
        'Your account is successfully created and ready to go.',
        'amitbju4@gmail.com',
        [user_email],
        fail_silently=False,
    )
    return f"Welcome email sent to {user_email}"