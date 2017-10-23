#! /home/underproof/myvenv/bin python
# -*- coding:utf-8 -*-
"""Django Models for SocialProfile App"""

# pylint: disable=C0111,E0202,W0613,W0141

from django.db.models.signals import post_save
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

import os
#from django.contrib.auth import get_user_model
#User = get_user_model()

import logging

LOGGER = logging.getLogger(name='socialprofile.models')

def avatar_upload_to(instance, filename):
    #return 'user_{0}/{1}'.format(instance.user.id, filename)
    return os.path.join('uploads', instance.user.username + os.path.splitext(filename)[1])


class SocialProfile(models.Model):
    """Main SocialProfile Object - Holds extra profile data retrieved from auth providers"""
    GENDER_CHOICES = (
        (_('male'), _('Мужской')),
        (_('female'), _('Женский')),
        (_('other'), _('Другой')),
        
    )
    user = models.OneToOneField(User, related_name='social_profile', verbose_name=_("Social Profile"))
    gender = models.CharField(max_length=10, blank=True, null=True, choices=GENDER_CHOICES, verbose_name=_("Пол"))
    url = models.URLField(blank=True, null=True, verbose_name=_("Домашняя страница"), help_text=_("Где мы можем найти больше о Вас?"), max_length=500)
    image_url = models.URLField(blank=True, null=True, verbose_name=_("Ссылка на аватар"), max_length=500)
    description = models.TextField(blank=True, null=True, verbose_name=_("Описание"), help_text=_("Расскажите о себе!"))
    manually_edited = models.BooleanField(default=False)
    avatar = models.ImageField(upload_to=avatar_upload_to, blank=True, null=True, verbose_name=_("Загрузка аватара"))
    uploaded_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    
    
    class Meta(object):
        verbose_name = _("Social Profile")
        verbose_name_plural = _("Social Profiles")
        ordering = ['user__username']

    def __str__(self):
        return self.user.username

    @models.permalink
    def get_absolute_url(self):
        return 'sp_profile_other_view_page', [self.user.username]


def create_user_profile(sender, instance, created, **kwargs):
    """Creates a UserProfile Object Whenever a User Object is Created"""
    if created:
        SocialProfile.objects.create(user=instance)


post_save.connect(create_user_profile, sender=User)


