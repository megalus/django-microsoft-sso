from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse


@login_required
def secret_page(request) -> HttpResponse:
    logout_url = reverse("logout")
    return render(
        request,
        "secret_page.html",
        {"logout_url": logout_url},
    )


def index(request) -> HttpResponse:
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse("secret"))
    return render(request, "login.html", {})
