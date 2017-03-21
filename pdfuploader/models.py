# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.core.urlresolvers import reverse
from .validators import validate_file_ext
#  TODO: from django.utils.encoding import python_2_unicode_compatible
import tagulous
from tagulous.models import TagField


class Archive(models.Model):
    """
    Represents an archive uploaded to the website. Its fields will be scrapped.
    First design is inteded to be with only pdfs
    Represents an archive uploaded to the website. Its fields will be scrapped.
    First design is inteded to be with only pdfs.
    Why there are produder, produced_by and creator?
    Some pdfs did have these different properties and to catch all them this 
    fields are required.
    """
    class Meta:
        #  TODO: unique_together
        verbose_name = "Archives"

    file = models.FileField(upload_to='PDFSuploads/%Y/%m/%d/',
                            validators=[validate_file_ext],
                            verbose_name="File"
                            )

    title = models.CharField(max_length=200,
                             verbose_name="Title"
                             )

    upload_date = models.DateTimeField(auto_now_add=True,
                                       verbose_name="Upload date-time"
                                       )

    creationdate = models.DateTimeField(null=True,
                                        blank=True,
                                        verbose_name="Creation date"
                                        )

    uploader = models.TextField(blank=True,
                                max_length=25,
                                null=True,
                                verbose_name="Uploading user"
                                )

    locked = models.BooleanField(
                                default=False,
                                verbose_name="Password protected"
                                )

    tags = tagulous.models.TagField(  # Tag system
                                get_absolute_url=lambda tag:
                                reverse(
                                        'pdfuploader.views.by_tag', kwargs={'tag_slug': tag.slug}
                                       ),
                                verbose_name="Tags",
                                blank=True,
                                force_lowercase=True,
                                max_count=5,
                                help_text="Enter comma separated words",
                                )
    hash_data = models.TextField(  # self generated: see views
                                unique=True,
                                max_length=250,
                                verbose_name="Hash"
                                )

    author = models.TextField(
                            default="",
                            blank=True,
                            help_text="PDF author.",
                            verbose_name="Author"
                            )

    produced_by = models.TextField(
                                default="",
                                blank=True,
                                help_text="Software/company who made it.",
                                verbose_name="Done by "
                                )

    url = models.URLField(
                        default="",
                        blank=True,
                        help_text="Website",
                        verbose_name="URL"
                        )

    pages = models.PositiveIntegerField(
                                        default=0,
                                        null=True,
                                        blank=True,
                                        verbose_name="Pages"
                                        )

    size = models.PositiveIntegerField(  # bytes size
                                        verbose_name="Size",
                                        blank=True,
                                        default=0,
                                        null=True
                                        )
    isbn = models.TextField(
                            blank=True,
                            default="",
                            max_length=15,
                            verbose_name="Commercial code"
                           )

    producer = models.TextField(
                                blank=True,
                                default="",
                                max_length=50,
                                verbose_name="Software used"
                                )

    creator = models.TextField(
                                blank=True,
                                default="",
                                max_length=50,
                                verbose_name="Other software used"
                                )

    def __unicode__(self):
        return unicode(self.title)
