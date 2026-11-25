from django.contrib import messages
from django.shortcuts import redirect, render
from django.contrib.auth import login
from .forms import RegistrationForm

def register(request):
    if request.user.is_authenticated:
        return redirect("tasks:list")
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Добро пожаловать! Аккаунт создан.")
            return redirect("tasks:list")
    else:
        form = RegistrationForm()
    return render(request, "users/register.html", {"form": form})
