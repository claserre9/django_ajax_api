from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic

from app_base.models import Hall


def home(request):
    return render(request, 'app_base/home.html')


@login_required
def dashboard(request):
    return render(request, 'halls/dashboard.html')


class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('home')
    template_name = 'registration/signup.html'

    def form_valid(self, form):
        view = super(SignUpView, self).form_valid(form)
        username, password = form.cleaned_data.get('username'), form.cleaned_data.get('password1')
        user = authenticate(username=username, password=password)
        login(self.request, user)
        return view


# CRUD
class CreateHallView(generic.CreateView):
    model = Hall
    fields = ('title',)
    template_name = 'halls/create.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.instance.user = self.request.user
        super(CreateHallView, self).form_valid(form)
        return redirect('home')


class DetailHallView(generic.DetailView):
    model = Hall
    template_name = 'halls/detail_hall.html'


class UpdateHallView(generic.UpdateView):
    model = Hall
    template_name = 'halls/update_hall.html'
    fields = ('title',)
    success_url = reverse_lazy('dashboard')


class DeleteHallView(generic.DeleteView):
    model = Hall
    template_name = 'halls/delete_hall.html'
    success_url = reverse_lazy('dashboard')
