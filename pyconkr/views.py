# -*- coding: utf-8 -*-
from django.conf import settings
from django.contrib.auth import login as user_login, logout as user_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.flatpages.models import FlatPage
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.shortcuts import render, redirect
from django.utils.translation import ugettext as _
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, DetailView, UpdateView
from datetime import datetime, timedelta
from uuid import uuid4
from .forms import EmailLoginForm, SpeakerForm, ProgramForm, RegistrationForm
from .helper import sendEmailToken, render_json, sendEmailTicketConfirm
from .models import (Room,
                     Program, ProgramDate, ProgramTime, ProgramCategory,
                     Speaker, Sponsor, Jobfair, Announcement,
                     EmailToken, Registration, Product)
from iamporter import get_access_token, Iamporter, IamporterError


def index(request):
    return render(request, 'index.html', {
        'base_content': FlatPage.objects.get(url='/index/').content,
        'recent_announcements': Announcement.objects.all()[:3],
    })


def schedule(request):
    dates = ProgramDate.objects.all()
    times = ProgramTime.objects.all()
    rooms = Room.objects.all()

    wide = {}
    narrow = {}
    processed = set()
    for d in dates:
        wide[d] = {}
        narrow[d] = {}
        for t in times:
            wide[d][t] = {}
            narrow[d][t] = {}
            for r in rooms:
                s = Program.objects.filter(date=d, times=t, rooms=r)
                if s:
                    if s[0].times.all()[0] == t and s[0].id not in processed:
                        wide[d][t][r] = s[0]
                        narrow[d][t][r] = s[0]
                        processed.add(s[0].id)
                else:
                    wide[d][t][r] = None

            if len(narrow[d][t]) == 0:
                del(narrow[d][t])

    contexts = {
        'wide': wide,
        'narrow': narrow,
        'rooms': rooms,
    }
    return render(request, 'schedule.html', contexts)


class RoomDetail(DetailView):
    model = Room


class SponsorList(ListView):
    model = Sponsor


class SponsorDetail(DetailView):
    model = Sponsor


class SpeakerList(ListView):
    model = Speaker


class SpeakerDetail(DetailView):
    model = Speaker

    def get_context_data(self, **kwargs):
        context = super(SpeakerDetail, self).get_context_data(**kwargs)

        if self.request.user.is_authenticated():
            if self.request.user.email == self.object.email:
                context['editable'] = True

        return context


class SpeakerUpdate(UpdateView):
    model = Speaker
    form_class = SpeakerForm

    def get_queryset(self):
        queryset = super(SpeakerUpdate, self).get_queryset()
        return queryset.filter(email=self.request.user.email)


class ProgramList(ListView):
    model = ProgramCategory
    template_name = "pyconkr/program_list.html"


class ProgramDetail(DetailView):
    model = Program

    def get_context_data(self, **kwargs):
        context = super(ProgramDetail, self).get_context_data(**kwargs)

        if self.request.user.is_authenticated():
            for speaker in self.object.speakers.all():
                if self.request.user.email == speaker.email:
                    context['editable'] = True

        return context


class ProgramUpdate(UpdateView):
    model = Program
    form_class = ProgramForm

    def get_queryset(self):
        queryset = super(ProgramUpdate, self).get_queryset()
        return queryset.filter(speakers__email=self.request.user.email)


class JobfairList(ListView):
    model = Jobfair


class AnnouncementList(ListView):
    model = Announcement

    def get_queryset(self):
        now = datetime.now()
        queryset = super(AnnouncementList, self).get_queryset()
        return queryset.filter(Q(announce_after__isnull=True) | Q(announce_after__lt=now))


class AnnouncementDetail(DetailView):
    model = Announcement


def robots(request):
    return render(request, 'robots.txt', content_type='text/plain')


def login(request):
    form = EmailLoginForm()

    if request.method == 'POST':
        form = EmailLoginForm(request.POST)
        if form.is_valid():
            # Remove previous tokens
            email = form.cleaned_data['email']
            EmailToken.objects.filter(email=email).delete()

            # Create new
            token = EmailToken(email=email)
            token.save()

            sendEmailToken(request, token)
            return redirect(reverse('login_mailsent'))

    return render(request, 'login.html', {
        'form': form,
        'title': _('Login'),
    })


@never_cache
def login_req(request, token):
    time_threshold = datetime.now() - timedelta(hours=1)

    try:
        token = EmailToken.objects.get(token=token,
                                       created__gte=time_threshold)
    except ObjectDoesNotExist:
        return render(request, 'login_notvalidtoken.html',
                      {'title': _('Not valid token')})
    email = token.email

    # Create user automatically by email as id, token as password
    try:
        user = User.objects.get(email=email)
    except ObjectDoesNotExist:
        user = User.objects.create_user(email, email, token)
        user.save()

    token.delete()

    # Set backend manually
    user.backend = 'django.contrib.auth.backends.ModelBackend'
    user_login(request, user)

    return redirect(reverse('index'))


@never_cache
def login_mailsent(request):
    return render(request, 'login_mailsent.html', {
        'title': _('Mail sent'),
    })


def logout(request):
    user_logout(request)
    return redirect(reverse('index'))


@login_required
def profile(request):
    return render(request, 'profile.html')


@login_required
def registration_info(request):
    is_ticket_open = allow_ticket_open()
    return render(request, 'pyconkr/registration/info.html', {
            "is_ticket_open" : is_ticket_open
        })


@login_required
def registration_status(request):
    try:
        registration = Registration.objects.filter(user=request.user).get()
    except Registration.DoesNotExist:
        registration = None

    return render(request, 'pyconkr/registration/status.html', {
        'title': _('Registration'),
        'registration': registration,
    })


@login_required
def registration_payment(request):
    max_ticket_limit = settings.MAX_TICKET_NUM

    if not allow_ticket_open():
        return redirect('registration_info')

    if request.method == 'GET':
        product = Product()

        registered = Registration.objects.filter(
            user=request.user,
            payment_status__in=['paid', 'ready']
        ).exists()

        if registered:
            return redirect('registration_status')

        uid = str(uuid4()).replace('-', '')
        form = RegistrationForm()

        return render(request, 'pyconkr/registration/payment.html', {
            'title': _('Registration'),
            'IMP_USER_CODE': settings.IMP_USER_CODE,  # TODO : Move to 'settings context processor'
            'form': form,
            'uid': uid,
            'product_name': product.name,
            'amount': product.price,
            'vat': 0,
        })
    elif request.method == 'POST':
        form = RegistrationForm(request.POST)

        # TODO : more form validation
        # eg) merchant_uid
        if not form.is_valid():
            return render_json({
                'success': False,
                'message': str(form.errors),  # TODO : ...
            })

        remain_ticket_count = (settings.MAX_TICKET_NUM - Registration.objects.filter(payment_status__in=['paid', 'ready']).count())

        # sold out
        if remain_ticket_count <= 0:
            return render_json({
                'success': False,
                'message': _(u'티켓이 매진 되었습니다'),
            })

        registration, created = Registration.objects.get_or_create(user=request.user)
        registration.name = form.cleaned_data.get('name')
        registration.email = form.cleaned_data.get('email')
        registration.company = form.cleaned_data.get('company', '')
        registration.phone_number = form.cleaned_data.get('phone_number', '')
        registration.merchant_uid = request.POST.get('merchant_uid')
        registration.save()  # TODO : use form.save()

        try:
            product = Product()
            access_token = get_access_token(settings.IMP_API_KEY, settings.IMP_API_SECRET)
            imp_client = Iamporter(access_token)

            if request.POST.get('payment_method') == 'card':
                # TODO : use validated and cleaned data
                imp_client.onetime(
                    token=request.POST.get('token'),
                    merchant_uid=request.POST.get('merchant_uid'),
                    amount=request.POST.get('amount'),
                    # vat=request.POST.get('vat'),
                    card_number=request.POST.get('card_number'),
                    expiry=request.POST.get('expiry'),
                    birth=request.POST.get('birth'),
                    pwd_2digit=request.POST.get('pwd_2digit'),
                    customer_uid=form.cleaned_data.get('email'),
                )

            confirm = imp_client.find_by_merchant_uid(request.POST.get('merchant_uid'))

            if confirm['amount'] != product.price:
                # TODO : cancel
                raise IOError  # TODO : -_-+++

            registration.payment_method = confirm.get('pay_method')
            registration.payment_status = confirm.get('status')
            registration.payment_message = confirm.get('fail_reason')
            registration.vbank_name = confirm.get('vbank_name', None)
            registration.vbank_num = confirm.get('vbank_num', None)
            registration.vbank_date = confirm.get('vbank_date', None)
            registration.vbank_holder = confirm.get('vbank_holder', None)
            registration.save()

            # send mail
            sendEmailTicketConfirm(request, registration)
        except IamporterError as e:
            # TODO : other status code
            return render_json({
                'success': False,
                'code': e.code,
                'message': e.message,
            })
        else:
            return render_json({
                'success': True,
            })


@csrf_exempt
def registration_payment_callback(request):
    merchant_uid = request.POST.get('merchant_uid', None)
    if not merchant_uid:
        raise IOError

    product = Product()

    # TODO : check stock

    access_token = get_access_token(settings.IMP_API_KEY, settings.IMP_API_SECRET)
    imp_client = Iamporter(access_token)

    confirm = imp_client.find_by_merchant_uid(merchant_uid)
    if confirm['amount'] != product.price:
        # TODO : cancel
        raise IOError  # TODO : -_-+++

    remain_ticket_count = (settings.MAX_TICKET_NUM - Registration.objects.filter(payment_status='paid').count())
    if  remain_ticket_count <= 0:
        # Cancel
        return render_json({
            'success': False,
            'message': _(u"티켓이 매진 되었습니다")
        })
    registration = Registration.objects.filter(merchant_uid=merchant_uid).get()
    registration.payment_status = 'paid'
    registration.save()
    
    # send mail
    sendEmailTicketConfirm(request, registration)

    return render_json({
        'success': True
    })


def allow_ticket_open():
    ticket_open_date = datetime.strptime(settings.TICKET_OPEN_DATETIME, '%Y-%m-%d %H:%M:%S')
    ticket_close_date = datetime.strptime(settings.TICKET_CLOSE_DATETIME, '%Y-%m-%d %H:%M:%S')
    cur = datetime.now()

    if ticket_open_date <= cur and ticket_close_date >= cur:
        return True
    else:
        return False
