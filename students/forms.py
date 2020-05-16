#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8

from django import forms


from core.utils import check_password


from .models import Admin, Student
from .validators import validate_email_auth


class AdminForm(forms.Form):
    email = forms.EmailField(widget=forms.TextInput, required=True,
                             validators=[validate_email_auth])
    passwd = forms.CharField(widget=forms.PasswordInput, required=True)

    def clean(self):
        passwd = self.cleaned_data["passwd"]
        email = self.cleaned_data["email"]
        admin = Admin.objects.get(email=email)
        if not check_password(admin.passwd, passwd):
            raise forms.ValidationError("Password Incorrect!")
        return self.cleaned_data


class StudentForm(forms.ModelForm):

    class Meta:
        model = Student
        fields = ['name', 'email', 'state', 'city',
                  'gender', 'ph_no']