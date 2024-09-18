from __future__ import annotations

from django import forms
from django.forms.widgets import Input
from django.shortcuts import render
from django.views.generic import FormView


class ColorInput(Input):
    input_type = "color"


class SearchInput(Input):
    input_type = "search"


class TelInput(Input):
    input_type = "tel"


class Level1Form(forms.Form):
    text = forms.CharField(widget=forms.TextInput)
    number = forms.CharField(widget=forms.NumberInput)
    email = forms.CharField(widget=forms.EmailInput)
    url = forms.CharField(widget=forms.URLInput)
    color = forms.CharField(widget=ColorInput)
    search = forms.CharField(widget=SearchInput)
    tel = forms.CharField(widget=TelInput)
    password = forms.CharField(widget=forms.PasswordInput)


class Level1FormView(FormView):
    form_class = Level1Form
    template_name = "talks/dcus2024/level1.html"


class DateInput(forms.DateInput):
    input_type = "date"


class DateTimeInput(forms.DateTimeInput):
    input_type = "datetime-local"


class DateForm(forms.Form):
    date = forms.DateField(widget=DateInput)
    datetime = forms.DateTimeField(widget=DateTimeInput)


class DateFormView(FormView):
    form_class = DateForm
    template_name = "talks/dcus2024/date.html"
    success_template_name = (
        "talks/dcus2024/date_success.html"  # New template for success
    )

    def form_valid(self, form):
        date = form.cleaned_data["date"]
        datetime = form.cleaned_data["datetime"]

        context = self.get_context_data(form=form)
        context.update(
            {
                "date": date,
                "datetime": datetime,
            }
        )

        return render(self.request, self.success_template_name, context)


class PasswordResetForm(forms.Form):
    current_password = forms.CharField(widget=forms.PasswordInput)
    new_password1 = forms.CharField(widget=forms.PasswordInput)
    new_password2 = forms.CharField(widget=forms.PasswordInput)


class PasswordResetFormView(FormView):
    form_class = PasswordResetForm
    template_name = "talks/dcus2024/password_reset_form.html"
