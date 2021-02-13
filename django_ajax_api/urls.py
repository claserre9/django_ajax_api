"""django_ajax_api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin, auth
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.urls import path

from app_base import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    # Auth
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('login/', views.MyLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    # Hall CRUD operations
    path('halloffame/create/', login_required(views.CreateHallView.as_view()), name='create_hall'),
    path('halloffame/', login_required(views.ListHallView.as_view()), name='list_hall'),
    path('halloffame/<int:pk>', login_required(views.DetailHallView.as_view()), name='detail_hall'),
    path('halloffame/<int:pk>/update', login_required(views.UpdateHallView.as_view()), name='update_hall'),
    path('halloffame/<int:pk>/delete', login_required(views.DeleteHallView.as_view()), name='delete_hall'),
    # Video
    path('halloffame/<int:pk>/addvideo', login_required(views.add_video), name='add_video'),
    path('video/search/', views.video_search, name='video_search'),
    path('ajax/add/video/', views.ajax_add_video, name='ajax_add_video'),
    path('halloffame/<int:pk>/deletevideo', login_required(views.DeleteVideo.as_view()), name='delete_video'),

]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
