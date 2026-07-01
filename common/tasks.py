# from celery import shared_task
# from django.core.mail import EmailMessage
# from django.template.loader import render_to_string

# EMAIL_FROM = "noreply@kayes.com"

# @shared_task
# def send_email(subject, template_name, context, recipient_list):
#     """
#     subject: str
#     template_name: str
#     context: dict
#     recipient_list: list of emails
#     """
#     message = render_to_string(template_name, context)
    
#     email = EmailMessage(
#         subject=subject,
#         body=message,
#         from_email=EMAIL_FROM,
#         to=recipient_list,
#     )
#     email.content_subtype = "html"
#     email.send()
#     return "Email sent successfully"

from celery import shared_task
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

@shared_task
def send_email(subject, template_name, context, recipient_list):
    html_message = render_to_string(template_name, context)
    plain_message = strip_tags(html_message)
    from_email = 'noreply@example.com'

    send_mail(
        subject,
        plain_message,
        from_email,
        recipient_list,
        html_message=html_message
    )

