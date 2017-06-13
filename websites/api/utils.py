# -*- coding: utf-8 -*-
import re
from StringIO import StringIO
from django.utils.translation import ugettext as _
from django.core.mail import EmailMultiAlternatives
from html2text import html2text as html2text_orig
from django.conf import settings
from django.template import Context
from django.template.loader import get_template
from django.contrib.sites.models import Site
import helper


LINK_RE = re.compile(r"https?://([^ \n]+\n)+[^ \n]+", re.MULTILINE)
def html2text(html):
    """Use html2text but repair newlines cutting urls.
    Need to use this hack until
    https://github.com/aaronsw/html2text/issues/#issue/7 is not fixed"""
    txt = html2text_orig(html)
    links = list(LINK_RE.finditer(txt))
    out = StringIO()
    pos = 0
    for l in links:
        out.write(txt[pos:l.start()])
        out.write(l.group().replace('\n', ''))
        pos = l.end()
    out.write(txt[pos:])
    return out.getvalue()

def send_mail(subject, message_plain, message_html, email_from, email_to,
              data, custom_headers={}, attachments=()):

    print "send mail"
    """
    Build the email as a multipart message containing
    a multipart alternative for text (plain, HTML) plus
    all the attached files.
    """
    try:
        if not message_plain and not message_html:
            raise ValueError(_("Either message_plain or message_html should be not None"))

        if not message_plain:
            message_plain = html2text(message_html)

        if not email_from:
            email_from = settings.DEFAULT_FROM_EMAIL
        
        cxt = Context(data)
        """ bind data to html template """
        text_content = get_template(message_plain).render(cxt)
        html_content = get_template(message_html).render(cxt)
        message = {}

        message['subject'] = subject
        message['body'] = text_content
        message['from_email'] = email_from
        message['to'] = email_to 
        
        # custom_headers['Reply-To'] = email_from
        if custom_headers:
            message['headers'] = custom_headers

        msg = EmailMultiAlternatives(**message)
        """ attach file in email """
        if attachments:
            try:
                for img in attachments:
                    msg.attach_file(settings.PROJECT_ROOT + '/public' + img)
            except:
                pass
        
        if message_html:
            msg.attach_alternative(html_content, "text/html")
        msg.send()
    except Exception, e:
        raise e


def card_information_mapper(item):
    card_information = {}
    if item:
        card_information["active_date"] = item[0] # Card_Added
        card_information["membership"] = 'Member Card' if item[1] == 1 else ('Gold Card' if item[1] == 6 else 'Normal Card') # Card_Status
        card_information["card_status"] = helper.get_card_status(item[2], item[14]) # Card_State
        card_information["play_value"] = item[3] # Cash_Balance
        card_information["bonus_value"] = item[4] # Bonus_Balance
        card_information["ticket"] = item[5] # ETickets
        card_information["first_name"] = item[6] # Firstname
        card_information["surname"] = item[7] # Surname
        card_information["birthday"] = item[8] # DOB
        card_information["peronal_id"] = item[9] # PostCode
        card_information["address"] = item[10] # Address1
        card_information["email"] = item[11] # EMail
        card_information["phone"] = item[12] # Phone
        card_information["upgraded_date"] = item[13] # upgraded_date
    return card_information


def play_transactions_mapper(list_items):
    list_transactions = []
    if list_items:
        for item in list_items:
            transaction = {}
            transaction["date"] = item[0] # Transaction_DateTime
            transaction["amount"] = item[1] # Transaction_Amount
            transaction["name"] = item[2] # Game_Description
            transaction["type"] = item[3] # transaction_type
            list_transactions.append(transaction)

    return list_transactions

def card_transactions_mapper(list_items):
    list_transactions = []
    if list_items:
        for item in list_items:
            transaction = {}
            transaction["date"] = item[0] # Transaction_DateTime
            transaction["amount"] = item[1] # Transaction_Amount
            transaction["name"] = "Reload amount " + '{:,.0f}'.format(float(item[1])) # Game_Description
            transaction["type"] = "Reload" # transaction_type
            list_transactions.append(transaction)

    return list_transactions

def reissue_history_mapper(list_items):
    list_reissues = []
    if list_items:
        for item in list_items:
            reissue = {}
            reissue["date"] = item[0] # Transaction_DateTime
            reissue["old_id"] = item[2] if item[4] == 500 else item[1] # Card_Barcode
            reissue["new_id"] = item[1] if item[4] == 500 else item[2] # Transfer_Card_Barcode
            reissue["type"] = item[3] # Card_Barcode
            list_reissues.append(reissue)

    return list_reissues