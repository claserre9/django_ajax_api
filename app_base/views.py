from urllib import parse


from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.forms.utils import ErrorList

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.http import Http404, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic

from app_base.forms import VideoForm, VideoSearchForm
from app_base.models import Hall, Video
import requests

YOUTUBE_API_KEY = 'AIzaSyAxQRR4U1uOPw_17Uc94YWcfF0eISHiKf4'


class MyLoginView(SuccessMessageMixin, LoginView):
    template_name = 'registration/login.html'
    success_message = 'Welcome to your profile'


def home(request):
    # # Flash message
    # messages.add_message(request, messages.SUCCESS, 'Hello world.')
    return render(request, 'app_base/home.html')


@login_required
def dashboard(request):
    halls = Hall.objects.filter(user=request.user)
    return render(request, 'halls/dashboard.html', context=dict(halls=halls))


@login_required
def add_video(request, pk):
    form = VideoForm()
    video_search_form = VideoSearchForm()
    hall = Hall.objects.get(pk=pk)
    if not hall.user == request.user:
        raise Http404
    if request.method == 'POST':
        form = VideoForm(request.POST)
        if form.is_valid():
            url = form.cleaned_data['url']

            video = Video()
            video.hall = hall
            video.url = url
            parsed_url = parse.urlparse(url)

            video_id = parse.parse_qs(parsed_url.query).get("v")
            print(video_id)
            if video_id:
                video.youtube_id = video_id[0]
                response = requests.get(
                    f'https://youtube.googleapis.com/youtube/v3/videos?part=snippet'
                    f'&id={video_id[0]}'
                    f'&key={YOUTUBE_API_KEY}')
                json = response.json()
                title = json['items'][0]['snippet']['title']
                print(title)
                video.title = title
                video.save()
                return redirect("detail_hall", pk)
            else:
                errors = form.errors.setdefault('url', ErrorList())
                errors.append('Need to be a youtube url')

    return render(request, 'halls/add_video.html',
                  dict(form=form, video_search_form=video_search_form, hall=hall))


def video_search(request):
    search_form = VideoSearchForm(request.GET)
    if search_form.is_valid():
        data = search_form.cleaned_data
        response = requests.get(f'https://youtube.googleapis.com/youtube/v3/'
                                f'search?part=snippet'
                                f'&maxResults=6'
                                f'&q={data["search_term"]}&key={YOUTUBE_API_KEY}')

        return JsonResponse(data=response.json())
    return JsonResponse(data={'error': 'Not able to validate form'})


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

class ListHallView(generic.ListView):
    model = Hall
    template_name = 'halls/list.html'
    context_object_name = 'halls'

    def get_queryset(self, **kwargs):
        qs = super(ListHallView, self).get_queryset()
        return qs.filter(user=self.request.user)


class CreateHallView(generic.CreateView):
    model = Hall
    fields = ('title',)
    template_name = 'halls/create.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.instance.user = self.request.user
        super(CreateHallView, self).form_valid(form)
        return redirect('dashboard')


class DetailHallView(generic.DetailView, PermissionRequiredMixin):
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


def ajax_add_video(request):
    if request.is_ajax() and request.method == 'POST':
        print("So far , so good")
        q_dict = request.POST.dict()
        print(q_dict)
        youtube_id = q_dict.get('id')
        pk = q_dict.get('pk')
        url = q_dict.get('url')
        title = q_dict.get('title')
        hall = Hall.objects.get(pk=pk)

        video = Video()
        video.hall = hall
        video.url = url
        video.youtube_id = youtube_id
        video.title = title

        video.save()
        return JsonResponse({})


class DeleteVideo(generic.DeleteView):
    model = Video
    template_name = 'video/delete_video.html'
    success_url = reverse_lazy('dashboard')
