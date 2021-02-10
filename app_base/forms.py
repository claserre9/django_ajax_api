from django import forms

from app_base.models import Video


class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ('title', 'url', 'youtube_id')
        labels = {'youtube_id': 'Youtube ID', 'url': 'URL'}
