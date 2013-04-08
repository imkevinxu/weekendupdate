from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin
from django import forms

import datetime
import os

class Base(models.Model):
    created_at  = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now_add=True, auto_now=True)

    class Meta:
        abstract = True

class Archive(Base):
    link        = models.URLField(max_length=255)
    edition     = models.IntegerField(default=0)
    description = models.CharField(max_length=255, blank=True, null=True)

    def __unicode__(self):
        return u'Weekend Update #%s' % (self.edition)