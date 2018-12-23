# -*- coding: utf-8 -*-
import os
from django.core.exceptions import ValidationError


def validate_file_ext(value):
    """Allows only PDF extension or raises an error"""
    ext = os.path.splitext(value.name)[1]
    valid_extensions = ['.pdf']
    if not ext.lower() in valid_extensions:
        raise ValidationError(u'File type not supported, please use PDF.')
