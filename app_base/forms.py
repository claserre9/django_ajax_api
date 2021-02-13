from django import forms

from app_base.models import Video


class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ('url', )
        labels = {'url': 'Youtube URL'}


class VideoSearchForm(forms.Form):
    search_term = forms.CharField(max_length=255, label='Search for videos')
