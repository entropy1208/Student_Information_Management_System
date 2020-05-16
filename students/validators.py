#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
from django.core.exceptions import ValidationError


from .models import Admin


def validate_email_auth(value):
    email = value
    try:
        Admin.objects.get(email=email)
    except:
        raise ValidationError("The email is incorrect!")
