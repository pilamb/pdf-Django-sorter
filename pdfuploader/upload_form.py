# -*- coding: utf-8 -*-
from django import forms
from django.forms import ModelForm
from django.shortcuts import render
from .models import Archive


class UploadFileForm(ModelForm):
    """
    Custom form handling file upload
    """

    class Meta:
        model = Archive
        exclude = [
            'title', 'creationdate', 'uploader', 'locked',
            'tags', 'hash_data', 'author', 'produced_by', 'url', 'pages',
            'size', 'isbn', 'creator', 'producer']

    def __init__(self, *args, **kwargs):
        self.title = kwargs.pop('title', None)
        super(UploadFileForm, self).__init__(*args, **kwargs)


def page(request):
    if request.POST:
        pass
    else:
        form = UploadFileForm()
        return render(request, '', {'form': form})
