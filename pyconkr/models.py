# -*- coding: utf-8 -*-
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.core.urlresolvers import reverse
from django.db import models
from django.template.defaultfilters import date as _date
from django.utils.translation import ugettext_lazy as _
from jsonfield import JSONField
from uuid import uuid4


class Room(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=255, null=True, blank=True)
    desc = models.TextField(null=True, blank=True)

    def get_absolute_url(self):
        return reverse('room', args=[self.id])

    def __unicode__(self):
        return self.name


class ProgramDate(models.Model):
    day = models.DateField()

    def __unicode__(self):
        return _date(self.day, "Y-m-d (D)")


class ProgramTime(models.Model):
    name = models.CharField(max_length=100)
    begin = models.TimeField()
    end = models.TimeField()

    def __unicode__(self):
        return '%s - %s / %s' % (self.begin, self.end, self.name)


class ProgramCategory(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=100, unique=True)

    def __unicode__(self):
        return self.name


class SponsorLevelManager(models.Manager):
    def get_queryset(self):
        return super(SponsorLevelManager, self).get_queryset().all().order_by('order')


class SponsorLevel(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=100, unique=True)
    desc = models.TextField(null=True, blank=True)
    order = models.IntegerField(default=1)

    objects = SponsorLevelManager()

    def __unicode__(self):
        return self.name


class Sponsor(models.Model):
    slug = models.SlugField(max_length=100, unique=True)
    name = models.CharField(max_length=100, db_index=True)
    image = models.ImageField(upload_to='sponsor', null=True, blank=True)
    url = models.CharField(max_length=255, null=True, blank=True)
    desc = models.TextField(null=True, blank=True)
    level = models.ForeignKey(SponsorLevel, null=True, blank=True)

    class Meta:
        ordering = ['id']

    def get_absolute_url(self):
        return reverse('sponsor', args=[self.slug])

    def __unicode__(self):
        return self.name


class Speaker(models.Model):
    slug = models.SlugField(max_length=100, unique=True)
    name = models.CharField(max_length=100, db_index=True)
    email = models.EmailField(max_length=255, db_index=True,
                              null=True, blank=True)
    image = models.ImageField(upload_to='speaker', null=True, blank=True)
    desc = models.TextField(null=True, blank=True)
    info = JSONField(blank=True, help_text=_('help-text-for-speaker-info'))

    class Meta:
        ordering = ['name']

    def get_badges(self, size_class=""):
        badge = \
            '<a class="btn btn-social btn-social-default {} btn-{}" href="{}" target="_blank">' \
            '<i class="fa fa-external-link fa-{}"></i>{}</a>'
        fa_replacement = {
            "homepage": "home",
            "blog": "pencil",
        }
        result = []
        for site, url in self.info.iteritems():
            result.append(badge.format(
                size_class,
                site, url,
                fa_replacement.get(site, site), site.capitalize()
            ))
        return '<div class="badges">{}</div>'.format(' '.join(result))

    def get_badges_xs(self):
        return self.get_badges("btn-xs")

    def get_absolute_url(self):
        return reverse('speaker', args=[self.slug])

    def get_image_url(self):
        if self.image:
            return self.image.url

        return static('image/anonymous.png')

    def __unicode__(self):
        return '%s / %s' % (self.name, self.slug)


class Program(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    desc = models.TextField(null=True, blank=True)
    slide_url = models.CharField(max_length=255, null=True, blank=True)
    pdf_url = models.CharField(max_length=255, null=True, blank=True)
    video_url = models.CharField(max_length=255, null=True, blank=True)
    speakers = models.ManyToManyField(Speaker, blank=True)
    language = models.CharField(max_length=2,
                                choices=settings.LANGUAGES,
                                default='ko')

    date = models.ForeignKey(ProgramDate, null=True, blank=True)
    rooms = models.ManyToManyField(Room, blank=True)
    times = models.ManyToManyField(ProgramTime, blank=True)
    category = models.ForeignKey(ProgramCategory, null=True, blank=True)

    is_recordable = models.BooleanField(default=True)

    def get_absolute_url(self):
        return reverse('program', args=[self.id])

    def room(self):
        rooms = self.rooms.all()

        if rooms.count() == Room.objects.all().count():
            return ''

        return ', '.join([_.name for _ in self.rooms.all()])

    def begin_time(self):
        return self.times.all()[0].begin.strftime("%H:%M")

    def get_speakers(self):
        return ', '.join([_.name for _ in self.speakers.all()])
    get_speakers.short_description = u'Speakers'

    def get_times(self):
        times = self.times.all()

        if times:
            return '%s - %s' % (times[0].begin.strftime("%H:%M"),
                                times[len(times) - 1].end.strftime("%H:%M"))
        else:
            return _("Not arranged yet")

    def __unicode__(self):
        return self.name


class Announcement(models.Model):
    title = models.CharField(max_length=100, db_index=True)
    desc = models.TextField(null=True, blank=True)

    announce_after = models.DateTimeField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-id']

    def at(self):
        return self.announce_after if self.announce_after else self.created

    def __unicode__(self):
        return self.title


class Jobfair(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    location = models.CharField(max_length=255, null=True, blank=True)
    sponsor = models.ForeignKey(Sponsor, null=True)
    desc = models.TextField(null=True, blank=True)

    def __unicode__(self):
        return self.name


class EmailToken(models.Model):
    email = models.EmailField(max_length=255)
    token = models.CharField(max_length=64, unique=True)
    created = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.token = str(uuid4())
        super(EmailToken, self).save(*args, **kwargs)


class Profile(models.Model):
    pass


class Product(object):  # product is not django model now.
    @property
    def price(self):
        return 15000

    @property
    def name(self):
        return 'PyCon Korea 2015'


class Registration(models.Model):
    user = models.ForeignKey(User)
    merchant_uid = models.CharField(max_length=32)
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=255)
    company = models.CharField(max_length=100, blank=True)
    phone_number = models.CharField(max_length=20)
    transaction_code = models.CharField(max_length=36)
    payment_method = models.CharField(
        max_length=20,
        default='card',
        choices=(
            ('card', u'신용카드'),
            #('vbank', _('Bank Transfer')),
        )
    )
    payment_status = models.CharField(
        max_length=10,
        # choices=(
        #     ('ready', _('Not Paid')),
        #     ('failed', _('Failed')),
        #     ('canceled', _('Canceled')),
        #     ('paid', _('Paid')),
        # )
    )
    payment_message = models.CharField(max_length=255, null=True)
    vbank_num = models.CharField(max_length=255, null=True, blank=True)
    vbank_name = models.CharField(max_length=20, null=True, blank=True)
    vbank_date = models.CharField(max_length=50, null=True, blank=True)
    vbank_holder = models.CharField(max_length=20, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
