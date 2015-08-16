from django.conf import settings
from django.contrib.flatpages.models import FlatPage
from django.db.models import Count
from django.utils.translation import ugettext_lazy as _
from collections import OrderedDict
from .models import SponsorLevel, Speaker


def default(request):
    title = None
    url = request.path
    if settings.FORCE_SCRIPT_NAME:
        url = url[len(settings.FORCE_SCRIPT_NAME):]
    base_content = FlatPage.objects.filter(url=url).first()

    menu = OrderedDict([
        ('about', {
            'title': _('About'),
            'icon': 'python',
            'dropdown': OrderedDict([
                ('pyconkr', {'title': _('About PyCon Korea 2015')}),
                ('coc', {'title': _('Code of Conduct')}),
                ('announcements', {'title': _('Announcements')}),
                ('sponsors', {'title': _('Sponsors')}),
                ('staff', {'title': _('Staff')}),
                ('contact', {'title': _('Contact')}),
            ]),
        }),
        ('programs', {
            'title': _('Programs'),
            'icon': 'calendar',
            'dropdown': OrderedDict([
                ('cfp', {'title': _('Call for proposals')}),
                ('schedule', {'title': _('Schedule')}),
                ('list', {'title': _('Program list')}),
                ('speakers', {'title': _('Speakers')}),
                ('ost', {'title': _('Open Spaces')}),
            ]),
        }),
        ('venue', {
            'title': _('Getting here'),
            'icon': 'map-marker',
            'dropdown': OrderedDict([
                ('map', {'title': _('Venue Map')}),
                ('transportation', {'title': _('Transportation')}),
                ('hotels', {'title': _('Hotels')}),
                ('restaurants', {'title': _('Restaurants')}),
            ]),
        }),
        ('registration', {
            'title': _('Registration'),
            'icon': 'pencil',
        }),
    ])

    for k, v in menu.iteritems():
        path = '/{}/'.format(k)

        if request.path.endswith(path):
            v['active'] = True
            title = v['title']

        if 'dropdown' in v:
            for sk, sv in v['dropdown'].iteritems():
                subpath = '{}{}/'.format(path, sk)

                if request.path.endswith(subpath):
                    sv['active'] = True
                    title = sv['title']

    return {
        'menu': menu,
        'title': title,
        'domain': settings.DOMAIN,
        'base_content': base_content.content if base_content else '',
    }


def profile(request):
    speaker = None
    programs = None

    if request.user.is_authenticated():
        speaker = Speaker.objects.filter(email=request.user.email).first()
        if speaker:
            programs = speaker.program_set.all()

    return {
        'my_speaker': speaker,
        'my_programs': programs,
    }


def sponsors(request):
    levels = SponsorLevel.objects.annotate(
        num_sponsors=Count('sponsor')).filter(num_sponsors__gt=0)

    return {
        'levels': levels,
    }
