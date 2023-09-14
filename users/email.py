from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.models import AbstractUser
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string


class BaseEmailSender:
    template_name = ""
    user_field = "id"

    def __init__(self, request, user: AbstractUser):
        self.request = request
        self._user = user

    def get_template_name(self):
        if not self.template_name:
            raise NotImplemented("Шаблон для адпраўкі email адсутнічае")
        return self.template_name


    def get_uid_base64(self):
        user_field_data = getattr(self._user, self.user_field)
        return urlsafe_base64_encode(force_bytes(user_field_data))

    def get_user_token(self):
        return default_token_generator.make_token(self._user)

    def get_context(self):
        return {
            "user": self._user,
            "domain": self.request.get_host(),
            "uid": self.get_uid_base64(),
            "token": self.get_user_token(),
        }

    def get_message(self):
        return render_to_string(self.get_template_name(), self.get_context())

    def get_subject(self):
        return f"Падцвердзіця рэгістрацыю на сайце {self.request.get_host()}"

    def perform_send_email(self):
        message = self.get_message()
        email = EmailMultiAlternatives(
            subject=self.get_subject(),
            body=message,
            to=[self._user.email],
        )
        email.attach_alternative(message, "text/html")
        email.send()

    def send_email(self):
        return self.perform_send_email()


class RegisterConfirmEmailSender(BaseEmailSender):
    template_name = "registration/email_confirm.html"


