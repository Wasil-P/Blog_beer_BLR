from django.shortcuts import render, redirect, reverse

from django.views import View
from .models import User
from .forms import UserRegisterForm
from .email import RegisterConfirmEmailSender


from django.shortcuts import render, redirect, reverse, get_object_or_404

from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model
from django.http import HttpResponse


class Register(View):
    def get(self, request):
        return render(
            request, "registration/register.html", {"form": UserRegisterForm()}
        )

    def post(self, request):
        form = UserRegisterForm(request.POST)

        if not form.is_valid():
            return render(request, "registration/register.html", {"form": form})

        user = form.save(commit=False)
        user.is_active = False
        user.save()

        email_sender = RegisterConfirmEmailSender(request, user)
        email_sender.send_email()

        return redirect(reverse("accounts:login"))


class ConfirmRegisterView(View):
    def get(self, request, uidb64: str, token: str):
        uid = force_str(
            urlsafe_base64_decode(uidb64)
        )
        user = get_object_or_404(get_user_model(), id=uid)

        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return redirect(reverse("accounts:login"))

        return HttpResponse("<h1>Спасылка нядзейсная</h1>")


