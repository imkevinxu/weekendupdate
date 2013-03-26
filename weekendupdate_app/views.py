from django import forms
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core import serializers
from django.core.context_processors import csrf
from django.core.mail import send_mail
from django.http import HttpResponse, HttpResponseRedirect
from coffin.shortcuts import render_to_response, get_object_or_404, render, \
    redirect
from django.template import loader, RequestContext
from django.views.decorators.csrf import csrf_exempt

from weekendupdate_app.models import *
from weekendupdate_app.model_forms import *
from weekendupdate_app.forms import *

import mailchimp

try:
    import json
except ImportError:
    import simplejson as json

MAILCHIMP_LIST_ID = '46624a7987'

def index(request):
    return render(request, "index.html", locals())

def signup(request):
    if request.is_ajax() and 'email' in request.POST and \
    (('type' in request.POST and request.POST['type'] != '') or \
    ('type_other' in request.POST and request.POST['type_other'] != '')):
        try:
            email_address = request.POST['email']
            type_str = request.POST['type'] if 'type' in request.POST else request.POST['type_other']
            list = mailchimp.utils.get_connection().get_list_by_id(MAILCHIMP_LIST_ID)
            list.subscribe(email_address, {'EMAIL': email_address, 'TYPE': type_str}, email_type='html')

            results = json.dumps({ 'status' : 'success' }, ensure_ascii=False)
            return HttpResponse(results, mimetype='application/json')
        except Exception, e:
            print e

    results = json.dumps({ 'status' : 'failure' }, ensure_ascii=False)
    return HttpResponse(results, mimetype='application/json')