# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import *

def index(request):
    return redirect('/main')

def main(request):
    return render(request, 'happiness/index.html')

def register(request):
    result = User.objects.validate(request.POST)
    if result[0]:
        request.session['user'] = result[1].id
        request.session['name'] = result[1].name
        request.session['email'] = result[1].email
        request.session['alias'] = result[1].alias
        print request.session['user']
        print request.session['name']
        print request.session['email']
        print request.session['alias']
        print result[1]
        return redirect('/quotes')
    else:
        for error in result[1]:
            messages.add_message(request,messages.INFO, error)
        return redirect('/main')

def login(request):
    result = User.objects.login(request.POST)
    if result[0]:
        request.session['user'] = result[1].id
        request.session['name'] = result[1].name
        request.session['email'] = result[1].email
        request.session['alias'] = result[1].alias
        return redirect('/quotes')
    else:
        for error in result[1]:
            messages.add_message(request,messages.INFO, error)
            return redirect('/main')

def quotes(request):
    print User.objects.get(id = request.session['user']).favoritesfrom.all()
    context = {
        'quotes': Quote.objects.all(),
        'list': User.objects.get(id = request.session['user']).favoritesfrom.all()
    }

    return render(request, 'happiness/quotes.html', context)

def logout(request):
    request.session['user'] = 0
    request.session['name'] = 0
    request.session['email'] = 0
    request.session['alias'] = 0
    return redirect('/main')

def add(request):
    
    
    result = Quote.objects.validate(request.POST)
    if result[0]:
        return redirect('/quotes')
    else:
        for error in result[1]:
            messages.add_message(request,messages.INFO, error)
        return redirect('/quotes')

def users(request, id):
    quote = Quote.objects.filter(posted_by = User.objects.get(id = id))
    # print Quote.objects.filter(posted_by = User.objects.get(id = id)).id
    count = Quote.objects.filter(posted_by = User.objects.get(id = id)).count()
    
    # print quote.author.name
    # print quote.author.id
    context = {
        'quotes': quote,
        'counter': count
    }
    return render(request,'happiness/users.html', context)

def addtolist(request):
    print '***'
    print request.POST
    result = Quote.objects.addtolist(request.POST)
    
    return redirect('/quotes')

    # the hidden value is tripping me up. It'' add to the favorite if you add a comment but it keps the hidden value at the high number
    
    
