#! /home/underproof/myvenv/bin python
# -*- coding:utf-8 -*-
"""
Custom signals sent during the registration and activation processes.

"""

from django.dispatch import Signal


# A new user has registered.
user_registered = Signal(providing_args=["user", "request"])

# A user has activated his or her account.
user_activated = Signal(providing_args=["user", "request"])

# signal sent when users successfully recover their passwords
user_recovers_password = Signal(
    providing_args=['user', 'request']
)
