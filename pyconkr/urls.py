from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib.flatpages import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from .views import index, schedule, setlang, robots
from .views import RoomDetail, JobfairList
from .views import AnnouncementList, AnnouncementDetail
from .views import SpeakerList, SpeakerDetail, SpeakerUpdate
from .views import SponsorList, SponsorDetail
from .views import ProgramList, ProgramDetail, ProgramUpdate
from .views import login, login_req, login_mailsent, logout

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^$', index, name='index'),

    url(r'^room/(?P<pk>\d+)$',
        RoomDetail.as_view(), name='room'),
    url(r'^about/announcements/$',
        AnnouncementList.as_view(), name='announcements'),
    url(r'^about/announcement/(?P<pk>\d+)$',
        AnnouncementDetail.as_view(), name='announcement'),
    url(r'^about/sponsors/$',
        SponsorList.as_view(), name='sponsors'),
    url(r'^about/sponsor/(?P<slug>\w+)$',
        SponsorDetail.as_view(), name='sponsor'),
    url(r'^programs/list/$',
        ProgramList.as_view(), name='programs'),
    url(r'^program/(?P<pk>\d+)$',
        ProgramDetail.as_view(), name='program'),
    url(r'^program/(?P<pk>\d+)/edit$',
        ProgramUpdate.as_view(), name='program_edit'),
    url(r'^programs/speakers/$',
        SpeakerList.as_view(), name='speakers'),
    url(r'^programs/speaker/(?P<slug>\w+)$',
        SpeakerDetail.as_view(), name='speaker'),
    url(r'^programs/speaker/(?P<slug>\w+)/edit$',
        SpeakerUpdate.as_view(), name='speaker_edit'),
    url(r'^programs/schedule/$',
        schedule, name='schedule'),
    url(r'^programs/jobfair/$',
        JobfairList.as_view(), name='jobfair'),

    url(r'^login/$', login, name='login'),
    url(r'^login/req/(?P<token>[a-z0-9\-]+)$', login_req, name='login_req'),
    url(r'^login/mailsent/$', login_mailsent, name='login_mailsent'),
    url(r'^logout/$', logout, name='logout'),

    url(r'^lang/(?P<lang_code>.*)/$', setlang, name='setlang'),
    url(r'^robots.txt$', robots, name='robots'),
    url(r'^summernote/', include('django_summernote.urls')),
    url(r'^admin/', include(admin.site.urls)),
)

# for development
if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += [
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT})
    ]

# for rosetta
if 'rosetta' in settings.INSTALLED_APPS:
    urlpatterns += [
        url(r'^rosetta/', include('rosetta.urls')),
    ]

# for flatpages
urlpatterns += [
    url(r'^(?P<url>.*/)$', views.flatpage),
]
