from django.core.mail import send_mail
from celery import shared_task
from django.utils.html import strip_tags
from django.template.loader import render_to_string


@shared_task(bind=True)
def send_blog_mail_celery_task(self, name, email, currentUrl):
    message = f"Hello {name}, below is the latest link to my new blog post:"
    html_message = render_to_string('app/blog_link_mail.html', {'currentUrl': currentUrl,'message':message})
    plain_message = strip_tags(html_message)
    
    send_mail(
        "Blog share",
        plain_message,
        "from@example.com",
        [email],
        html_message=html_message,
        fail_silently=False,
    ) 
      
