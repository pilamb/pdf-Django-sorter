# -*- encoding: utf-8 -*-
from django import forms
from .models import Archive


class uploadArchiveForm(forms.Form):
    """View for handling PDFs upload, decoupling it from the view"""
    file = forms.FileField()

    class Meta:
        model = Archive
