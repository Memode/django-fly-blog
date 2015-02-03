from django.conf.urls import patterns, include, url
from blog import views
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^$', views.IndexView.as_view(), name='home'),
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^(?P<slug>[\w|\-|\d|\W]+?).html$',
                           views.PostDetailView.as_view(), name='detail'),
                       url(r'^category/(?P<alias>\w+)/',
                           views.CategoryListView.as_view()),
                       url(r'^tag/(?P<tag>[\w|\.|\-]+)/',
                           views.TagsListView.as_view()),
                       url(r'^(?P<slug>[\w|\-|\d]+)/$',
                           views.PageDetailView.as_view()),
                       url(r'^ueditor/',include('DjangoUeditor.urls' )),
                       )
from django.conf import settings

if settings.DEBUG:
    urlpatterns += patterns('',
                            url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
                                {'document_root': settings.MEDIA_ROOT}),
                            )
