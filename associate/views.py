from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from django.template import loader
from django.http import Http404
import json

from .models import Associate
from .models import Addresses
from .models import Settings


def offsetManagement(request):
    """Load offset from session, if not exists then load from DB. IF not exists in DB then insert to DB"""
    if 'off_set' in request.session:
        off_set = request.session['off_set']
    else:
        try:
            off_set = int(Settings.objects.get(name_text__exact="off_set").value_text)
        except Settings.DoesNotExist:
            off_set = 50
            Settings(name_text="off_set", value_text="50").save()

        request.session['off_set'] = off_set
    return off_set


def index(request):
    return redirect('/associates/')


def associates(request):
    off_set = offsetManagement(request)

    """Load associate list"""
    associate_list = Associate.objects.order_by('name_text')[0:off_set]

    context = {
        'associate_list': associate_list,
        'last_page': off_set
    }
    return render(request, 'associates/index.html', context)


def associatesNext(request, page):
    page_int = int(page)
    off_set = offsetManagement(request)

    """Load associate list"""
    associate_list = Associate.objects.order_by('name_text')[page_int:page_int + off_set]

    context = {
        'associate_list': list(associate_list.values()),
        'last_page': page_int + off_set
    }
    return HttpResponse(json.dumps(context), content_type="application/json")


def details(request, associate_id):
    try:
        associate_details = Associate.objects.get(pk=associate_id)
    except Associate.DoesNotExist:
        associate_details = list()

    addresses_details = Addresses.objects.filter(associate=associate_id)

    context = {
        'associate_details': associate_details,
        'addresses_details': addresses_details
    }

    return render(request, 'associates/details.html', context)
