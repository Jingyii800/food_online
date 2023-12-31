from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage

def detectUser(user):
    if user.role == 1:
        redirectUrl = 'vendorDashboard'
        return redirectUrl
    elif user.role == 2:
        redirectUrl = 'custDashboard'
        return redirectUrl
    elif user.role == None and user.is_superadmin:
        redirectUrl = '/admin'
        return redirectUrl

def send_verification_email(request, user, mail_subject, email_template):
    from_email = settings.DEFAULT_FROM_EMAIL
    current_site = get_current_site(request)
    message = render_to_string(email_template, {
        # data in email body
        'user': user,
        'domain': current_site,
        # encode user's primary key and send in email body
        'uid': urlsafe_base64_encode(force_bytes(user.pk)) ,
        # make token will take the user and generate its token
        'token': default_token_generator.make_token(user),
    })
    to_email = user.email
    mail = EmailMessage(mail_subject, message, from_email=from_email,to=[to_email])
    # open email with html code
    mail.cotent_subtype = 'html'
    mail.send()

def send_notification(mail_subject, mail_template, context):
    from_email = settings.DEFAULT_FROM_EMAIL
    message = render_to_string(mail_template, context)
    # check if it's a kist or a str
    if isinstance(context['to_email'], str): # in customer email
        to_email = []
        to_email.append(context['to_email'])
    else: # in vendor email (already a list)
        to_email = context['to_email']
    
    mail.cotent_subtype = 'html'
    # do not change this sequence of EmailMessage !!! follow this sequence 
    mail = EmailMessage(mail_subject, message, from_email=from_email, to=to_email)
    mail.send()