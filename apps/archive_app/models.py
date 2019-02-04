from __future__ import unicode_literals
import re
from django.db import models
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        if (len(postData['first_name']) < 1) or (len(postData['last_name'])
                < 1) or (len(postData['email']) < 1):
            errors["blank"] = "All fields are required and must not be blank."
        if not (postData['first_name'].isalpha() and postData['last_name'].isalpha()):
            errors["alpha"] = "First and Last Name cannot contain any numbers."
        if not EMAIL_REGEX.match(postData['email']):
            errors["email"] = "Invalid Email Address."
        if not (postData['password'] == postData['password_confirm']):
            errors["password"] = "Password and Password Confirmation do not match."
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()

class Archive(models.Model):
    title = models.CharField(max_length=255)
    img = models.ImageField(blank=True, null=True, upload_to='images/%Y/%m/$D/')
    audio = models.FileField(blank=True, null=True, upload_to='audio/%Y/%m/$D/')
    # img = models.ImageField()
    # audio = models.FileField()
    user = models.ForeignKey(User, related_name='uploads', on_delete=models.CASCADE)
    favorited_users = models.ManyToManyField(User, related_name = "favorite_archives")
    created_at = models.DateTimeField(auto_now_add=True) 
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

