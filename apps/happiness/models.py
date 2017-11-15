# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import bcrypt
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
from django.db import models

class UserManager(models.Manager):
    
    def login(self, POST):
        errors = []
        if len(POST['email']) == 0:
            errors.append('Please enter a valid email')
        if len(POST['password']) == 0:
            errors.append('Please enter a valid password')
        if len(User.objects.filter(email = POST['email'])) < 1 or not bcrypt.checkpw(POST['password'].encode(), User.objects.get(email = POST['email']).password.encode()):
            errors.append('wrong email and password combo')
        if len(errors) > 0:
            return (False, errors) # return the list of errors
        else:
            user = User.objects.get(email = POST['email'])
            return (True, user)

    def validate(self, POST):
        errors = []
        if len(POST['name']) == 0:
            errors.append('First Name is required')
        if len(POST['alias']) == 0:
            errors.append('Alias is required')
        if len(User.objects.filter(alias = POST['alias'])) > 0:
            errors.append('Alias already in use')
        if len(POST['email']) == 0:
            errors.append('Email is required')
        if len(POST['password']) == 0:
            errors.append('Password is required')
        if POST['password'] != POST['confirm_password']:
            errors.append('Passwords do not match')
        # user_check = User.objects.get(email = POST['email'])
        if len(User.objects.filter(email = POST['email'])) > 0:
            errors.append('duplicate email')
        # if len(user_check) == 0:
        if len(errors) > 0:
            return (False, errors) # return the list of errors
        else:
            # save the information
            new_user = User.objects.create(
                name = POST['name'],
                alias = POST['alias'],
                email = POST['email'],
                password = bcrypt.hashpw(POST['password'].encode(), bcrypt.gensalt()),
            )
            # then what?
            return (True, new_user)

class QuoteManager(models.Manager):
    
    def validate(self, POST):
        # print request.session.user
        errors = []
        # print POST['author']
        if len(POST['author']) < 4:
            errors.append('Need a Valid Author Man')
        if len(POST['message']) < 11:
            errors.append("Please enter a valid message kind sir and or mad'am")
        if len(errors) > 0:
            return (False, errors) # return the list of errors
        else:
            # save the information
            new_quote = Quote.objects.create(
                posted_by = User.objects.get(id =POST['user'][0]),
                author = POST['author'],
                message = POST['message'],
            )
            # then what?
            return (True, new_quote)

    def addtolist(self, POST):      
        this_quote = Quote.objects.get(id = POST['id'])
        this_user = User.objects.get(id = '2')
        print this_quote.id
        print this_user.id
        new_favorite = this_quote.favorite.add(this_user)
        # print new_favorite
        return(True, new_favorite)


class User(models.Model):
    name = models.CharField(max_length=255)
    alias = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    objects = UserManager()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    def __repr__(self):
        return '<User object: {} {} {} {}>'.format(self.name, self.id, self.email, self.password)

class Quote(models.Model):
    author = models.CharField(max_length=255)
    message = models.TextField()
    posted_by = models.ForeignKey(User, related_name='quotes')
    favorite = models.ManyToManyField(User, related_name='favoritesfrom')
    objects = QuoteManager()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    def __repr__(self):
        return '<User object: {} {} {} {}>'.format(self.author, self.id, self.posted_by, self.favorite)
