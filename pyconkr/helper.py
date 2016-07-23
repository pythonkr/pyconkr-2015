# -*- coding: utf-8 -*-
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.http import HttpResponse
from django.template import Context
from django.template.loader import render_to_string, get_template
import json
from .models import Product


def sendEmailToken(request, token):
    variables = Context({
        'request': request,
        'token': token,
    })
    html = get_template('mail/token_html.html').render(variables)
    text = get_template('mail/token_text.html').render(variables)

    msg = EmailMultiAlternatives(
        settings.EMAIL_LOGIN_TITLE,
        text,
        settings.EMAIL_SENDER,
        [token.email])
    msg.attach_alternative(html, "text/html")
    msg.send(fail_silently=False)


def render_json(data_dict):
    return HttpResponse(json.dumps(data_dict),
                        'application/javascript')


def render_template_json(template, context):
    return HttpResponse(render_to_string(template, context),
                        'application/javascript')

def send_email_ticket_confirm(request, payment_info):
    """
    :param request Django request object
    :param payment_info Registration object
    """
    mail_title = u"PyCon Korea 2015 등록확인 안내(Registration confirmation)"
    product = Product()
    variables = Context({
        'request': request,
        'payment_info': payment_info,
        'amount': product.price
    })
    html = get_template('mail/ticket_registered_html.html').render(variables)
    text = get_template('mail/ticket_registered_text.html').render(variables)
    
    msg = EmailMultiAlternatives(
        mail_title,
        text,
        settings.EMAIL_SENDER,
        [payment_info.email])
    msg.attach_alternative(html, "text/html")
    msg.send(fail_silently=False)

def render_io_error(reason):
    response = HttpResponse(reason)
    response.status_code = 406
    return response
