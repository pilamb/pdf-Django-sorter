from django.conf.urls import url
from django.views.generic import DetailView
from .models import Archive
from . import views
from .views import ArchiveDelete, ArchiveUpdate


detail_view = DetailView.as_view(model=Archive)

urlpatterns = [
    url(r'^uploadpdf$', views.uploadpdf, name='uploadpdf'),

    url(r'^list_uploads$', views.listArchives, name='list_uploads'),

    url(r'^stats$', views.stats, name='stats'),

    url(r'^tags$', views.tags, name='etiquetas'),

    url(r'^tag/(?P<slug>[-\w]+)/$', views.tag_detail, name='tag_detail'),

    url(r'^archive_detail/(?P<pk>[a-z\d]+)$', detail_view,
        name='archive_detail'),

    url(r'^archive_delete/(?P<pk>[a-z\d]+)$', ArchiveDelete.as_view(),
        name='delete_archive'),

    url(r'^archive_edit/(?P<pk>[a-z\d]+)$', ArchiveUpdate.as_view(),
        name='edit_archive'),
]
