from __future__ import unicode_literals

from django.db import models
from datetime import datetime, date
import bcrypt
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')

# Create your models here.
class UserManager(models.Manager):
    def login(self, postData):
        email = postData['email']
        password = postData['password']

        alerts = []

        if len(email) < 1:
            alerts.append('Please enter email address.')
        try:
            user = User.objects.get(email=email)
        except:
            print ('Email NOT REGISTERED')
            alerts.append('The email "{}" is either incorrect or has not been registered.'.format(email))
            return (False, alerts)
        else:
            if email == user.email:
                if bcrypt.hashpw(password.encode(), user.pw_hashed.encode()) == user.pw_hashed:
                    # print ('it matches', user.id)
                    return (True, 'back, {}!'.format(user.name), user.id)
                else:
                    # print ('no pw match')
                    alerts.append('The password entered is incorrect. Please try again.')

            if alerts:
                return (False, alerts)


    def register(self, postData):
        # grabs user input from registration form
        name = postData['name']
        alias = postData['alias']
        email = postData['email']
        dob = postData['dob']
        password = postData['password']
        pw_verify = postData['pw_verify']

        alerts = []

        if len(postData['name']) < 1:
            alerts.append('Name cannot be left blank.')

        if len(postData['alias']) < 1:
            alerts.append('Alias cannot be left blank.')

        if len(postData['email']) < 1:
            alerts.append('Email cannot be left blank.')
        elif not EMAIL_REGEX.match(email):
            alerts.append('Invalid email address.')

        if len(password) < 8:
            alerts.append('Password must be at least 8 characters in length.')
        elif password != pw_verify:
            alerts.append('Passwords do not match.')

        if len(postData['dob']) < 1:
            alerts.append('Date of birth cannot be left blank.')
        else:
            dob = datetime.strptime(postData['dob'], '%Y-%m-%d')
            if dob > datetime.today():
                print ('DOB IN FUTURE')
                alerts.append('Date of birth cannot be in the future.')

        if alerts:
            return (False, alerts)
        # else:
        #     try:
        #         User.objects.get(name=name)
        #     except:
        #         print ('USER ALREADY EXISTS')
        #         alerts.append('The name "{}" has already been registered.'.format(name))
        #         return (False, alerts)
        else:
            pw_hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
            user = User.objects.create(name=name, alias=alias, email=email, dob=postData['dob'], pw_hashed=pw_hashed)
            return (True, 'aboard, {}!'.format(name), user.id)


class User(models.Model):
    name = models.CharField(max_length=255, default=1)
    alias = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    dob = models.DateField(auto_now=False)
    pw_hashed = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    userManager = UserManager()
    objects = models.Manager()
