from django.conf.urls import url
from django.views.generic import DetailView

from .models import Archive
from .views import (ArchiveDelete, ArchiveUpdate, stats, tags, list_archives,
                    upload_archive, tag_detail)


detail_view = DetailView.as_view(model=Archive)

urlpatterns = [
    url(r'^uploadpdf$', upload_archive, name='uploadpdf'),
    url(r'^list_uploads$', list_archives, name='list_uploads'),
    url(r'^tag/(?P<slug>[-\w]+)/$', tag_detail, name='tag_detail'),
    url(r'^archive_detail/(?P<pk>[a-z\d]+)$', detail_view,
        name='archive_detail'),
    url(r'^archive_delete/(?P<pk>[a-z\d]+)$', ArchiveDelete.as_view(),
        name='delete_archive'),
    url(r'^archive_edit/(?P<pk>[a-z\d]+)$', ArchiveUpdate.as_view(),
        name='edit_archive'),
    url(r'^stats$', stats, name='stats'),
    url(r'^tags$', tags, name='tags_url'),
]
