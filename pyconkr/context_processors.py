from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.db.models import Count
from collections import OrderedDict
from .models import SponsorLevel, Speaker


def menu(request):
    title = None
    menu = OrderedDict([
        ('about', {
            'title': _('About'),
            'icon': 'python',
            'dropdown': OrderedDict([
                ('pyconkr', {'title': _('About PyCon Korea 2015')}),
                ('coc', {'title': _('Code of Conduct')}),
                ('detail', {'title': _('Conference detail')}),
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
                ('cfp', {'title': _('Call for proposal')}),
                ('schedule', {'title': _('Schedule')}),
                ('list', {'title': _('Program list')}),
                ('speakers', {'title': _('Speakers')}),
                ('jobfair', {'title': _('Jobfair')}),
                ('bof', {'title': _('BOF')}),
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
                ('weather', {'title': _('Weather')}),
                ('international', {'title': _('International Attendees')}),
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
