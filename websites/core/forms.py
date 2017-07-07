from django import forms
from models import Contact
import api.utils as utils
from captcha.fields import ReCaptchaField
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.utils.translation import ugettext_lazy
from django.contrib.auth.forms import AuthenticationForm


class SecureAdminLoginForm(AuthenticationForm):
    captcha = ReCaptchaField(required=True)


class ContactForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput())
    email = forms.CharField(widget=forms.TextInput())
    phone = forms.CharField(widget=forms.TextInput())
    subject = forms.CharField(widget=forms.TextInput())
    message = forms.CharField(widget=forms.TextInput(), required=False)
    captcha = ReCaptchaField(required=True)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(ContactForm, self).__init__(*args, **kwargs)
        self.fields['captcha'].error_messages = {
            'required': ugettext_lazy("This field is required.")}

    def save(self, commit=True):
        name = self.cleaned_data['name']
        email = self.cleaned_data['email']
        phone = self.cleaned_data['phone']
        subject = self.cleaned_data['subject']
        message = self.cleaned_data['message']

        if commit:
            try:
                contact = Contact()
                contact.name = name
                contact.email = email
                contact.phone = phone
                contact.subject = subject
                contact.message = message
                contact.save()

                message_plain = "websites/email/contact_email.txt"
                message_html = "websites/email/contact_email.html"

                data_render = {
                    "name": name,
                    "email": email,
                    "phone": phone,
                    "subject": subject,
                    "message": message,
                    'site': get_current_site(self.request),

                }

                utils.send_mail(subject=subject, message_plain=message_plain, message_html=message_html,
                                email_from=settings.DEFAULT_FROM_EMAIL, email_to=[settings.DEFAULT_TO_ADMIN_EMAIL], data=data_render)
            except Exception, e:
                print 'Error ', e
                raise Exception(
                    "ERROR : Internal Server Error .Please contact administrator.")
