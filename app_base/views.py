from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from app_base.models import Hall


def home(request):
    return render(request, 'app_base/home.html')


class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('home')
    template_name = 'registration/signup.html'


class CreateHallView(generic.CreateView):
    model = Hall
    fields = '__all__'
    template_name = 'halls/create.html'
    success_url = reverse_lazy('home')
