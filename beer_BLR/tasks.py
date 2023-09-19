import textwrap
from celery import shared_task
from django.contrib.auth import get_user_model
from django.core.mail import EmailMultiAlternatives



@shared_task(ignore_result=True)
def send_new_news(id, user_id, name, description):
    description = textwrap.wrap(description, 50)[0] + "..."
    name_short = textwrap.wrap(name, 25)[0] + "..."
    link = f'http://127.0.0.1:8000/blog/news/{id}'
    user = get_user_model().objects.filter(id=user_id)

    email = EmailMultiAlternatives(
        subject=f"З'явілася новая навіна: {name_short}",
        to=[user.email],
    )
    email.attach_alternative(
        f"З'явілася новая навіна: {name}.<br>"
        f"Змест: {description}.<br>"
        f"Падрабязней тут: {link}"
        "text/html",)
    email.send()

@shared_task(ignore_result=True)
def send_new_experience(id, user_id, name, description):
    description = textwrap.wrap(description, 50)[0] + "..."
    link = f'http://127.0.0.1:8000/blog/my_experience/{id}'
    user = get_user_model().objects.filter(id=user_id)

    email = EmailMultiAlternatives(
        subject=f"З'явілася новая навіна: {name}",
        to=[user.email],
    )
    email.attach_alternative(
        f"З'явіўся новы эксперымент: {name}.<br>"
        f"Змест: {description}.<br>"
        f"Падрабязней тут: {link}"
        "text/html", )
    email.send()

