from __future__ import annotations

from django import forms
from django.contrib.auth.password_validation import password_validators_help_texts
from django.contrib.auth.password_validation import validate_password
from django.forms.widgets import Input
from django.http import HttpResponse
from django.shortcuts import render
from django.utils.html import format_html
from django.utils.html import format_html_join
from django.views.generic import FormView


class Level1Form(forms.Form):
    number = forms.CharField(widget=forms.NumberInput)
    email = forms.CharField(widget=forms.EmailInput)
    url = forms.CharField(widget=forms.URLInput)
    password = forms.CharField(widget=forms.PasswordInput)


class Level1FormView(FormView):
    form_class = Level1Form
    template_name = "talks/dcus2024/level1.html"


class ColorInput(Input):
    input_type = "color"


class SearchInput(Input):
    input_type = "search"


class TelInput(Input):
    input_type = "tel"


class ComingInDjango52Form(forms.Form):
    color = forms.CharField(widget=ColorInput)
    search = forms.CharField(widget=SearchInput)
    tel = forms.CharField(widget=TelInput)


class ComingInDjango52FormView(FormView):
    form_class = ComingInDjango52Form
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
    success_template_name = "talks/dcus2024/date_success.html"

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


class PasswordResetForm1(forms.Form):
    current_password = forms.CharField()
    new_password1 = forms.CharField()
    new_password2 = forms.CharField()


class PasswordResetFormView1(FormView):
    form_class = PasswordResetForm1
    template_name = "talks/dcus2024/password_reset_form.html"


class PasswordResetForm2(forms.Form):
    current_password = forms.CharField(widget=forms.PasswordInput)
    new_password1 = forms.CharField(widget=forms.PasswordInput)
    new_password2 = forms.CharField(widget=forms.PasswordInput)


class PasswordResetFormView2(FormView):
    form_class = PasswordResetForm2
    template_name = "talks/dcus2024/password_reset_form.html"


class PasswordField(forms.CharField):
    widget = forms.PasswordInput

    def __init__(self, *args, **kwargs):
        if kwargs.get("template_name") is None:
            kwargs["template_name"] = "talks/dcus2024/password_field.html"
        super().__init__(*args, **kwargs)


class PasswordResetForm3(forms.Form):
    current_password = PasswordField()
    new_password1 = PasswordField()
    new_password2 = PasswordField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update(
                {
                    "class": "w-full border rounded-lg text-sm h-10 leading-6 px-3 bg-white text-gray-700 placeholder-gray-400 shadow-sm border-gray-300 border-b-gray-400/80 focus:border-blue-500"
                }
            )


class PasswordResetFormView3(FormView):
    form_class = PasswordResetForm3
    template_name = "talks/dcus2024/password_reset_form_styled.html"


class PasswordResetForm4(forms.Form):
    current_password = PasswordField()
    new_password1 = PasswordField(label="")
    new_password2 = PasswordField(label="")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update(
                {
                    "class": "w-full border rounded-lg text-sm h-10 leading-6 px-3 bg-white text-gray-700 placeholder-gray-400 shadow-sm border-gray-300 border-b-gray-400/80 focus:border-blue-500"
                }
            )
            # if field.startswith("new_password"):
            #     self.fields[field].label = ""


class PasswordResetFormView4(FormView):
    form_class = PasswordResetForm4
    template_name = "talks/dcus2024/password_reset_form4.html"


class PasswordResetForm5(forms.Form):
    current_password = PasswordField()
    new_password1 = PasswordField(label="")
    new_password2 = PasswordField(label="")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[
                field
            ].widget.template_name = "talks/dcus2024/password_input.html"


class PasswordResetFormView5(FormView):
    form_class = PasswordResetForm5
    template_name = "talks/dcus2024/password_reset_form4.html"


class PasswordResetForm6(forms.Form):
    current_password = PasswordField()
    new_password1 = PasswordField(label="")
    new_password2 = PasswordField(label="")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[
                field
            ].widget.template_name = "talks/dcus2024/password_input.html"


class PasswordResetFormView6(FormView):
    form_class = PasswordResetForm6
    template_name = "talks/dcus2024/password_reset_form6.html"

    def get(self, request, *args, **kwargs):
        if request.htmx and (
            htmx_validation_field := request.GET.get("_validate_field", None)
        ):
            form = self.form_class(request.GET)
            form.is_valid()
            bound_field = form[htmx_validation_field]
            rendered = form.render(
                context={
                    "field": bound_field,
                    "errors": form.error_class(
                        bound_field.errors, renderer=form.renderer
                    ),
                },
                template_name=f"{self.template_name}#field-partial",
            )
            return HttpResponse(rendered)
        return super().get(request, *args, **kwargs)


class PasswordField7(forms.CharField):
    widget = forms.PasswordInput

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.template_name = "talks/dcus2024/password_field7.html"


class PasswordResetForm7(forms.Form):
    current_password = PasswordField7()
    new_password1 = PasswordField(label="")
    new_password2 = PasswordField(label="")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[
                field
            ].widget.template_name = "talks/dcus2024/password_input.html"

    def clean_current_password(self):
        data = self.cleaned_data["current_password"]
        if data != "dcus2024":
            raise forms.ValidationError("Does not match current password")
        return data


class PasswordResetFormView7(FormView):
    form_class = PasswordResetForm7
    template_name = "talks/dcus2024/password_reset_form7.html"

    def get(self, request, *args, **kwargs):
        if request.htmx and (
            htmx_validation_field := request.GET.get("_validate_field", None)
        ):
            form = self.form_class(request.GET)
            form.is_valid()
            bound_field = form[htmx_validation_field]
            rendered = form.render(
                context={
                    "field": bound_field,
                    "errors": form.error_class(
                        bound_field.errors, renderer=form.renderer
                    ),
                },
                template_name=f"{self.template_name}#field-partial",
            )
            return HttpResponse(rendered)
        return super().get(request, *args, **kwargs)


def password_validators_help_text_html():
    help_texts = password_validators_help_texts()
    help_items = format_html_join(
        "", "<li>{}</li>", ((help_text,) for help_text in help_texts)
    )
    return format_html("<ul>{}</ul>", help_items) if help_items else ""


class PasswordResetForm8(forms.Form):
    current_password = PasswordField7()
    new_password1 = PasswordField7(
        label="", help_text=password_validators_help_text_html()
    )
    new_password2 = PasswordField7(label="")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[
                field
            ].widget.template_name = "talks/dcus2024/password_input.html"

    def clean_current_password(self):
        data = self.cleaned_data["current_password"]
        if data != "dcus2024":
            raise forms.ValidationError("Does not match current password")
        return data

    def clean_new_password1(self):
        data = self.cleaned_data["new_password1"]
        validate_password(data)
        return data


class PasswordResetFormView8(FormView):
    form_class = PasswordResetForm8
    template_name = "talks/dcus2024/password_reset_form8.html"

    def get(self, request, *args, **kwargs):
        if request.htmx and (
            htmx_validation_field := request.GET.get("_validate_field", None)
        ):
            form = self.form_class(request.GET)
            form.is_valid()
            bound_field = form[htmx_validation_field]
            rendered = form.render(
                context={
                    "field": bound_field,
                    "errors": form.error_class(
                        bound_field.errors, renderer=form.renderer
                    ),
                },
                template_name=f"{self.template_name}#field-partial",
            )
            return HttpResponse(rendered)
        return super().get(request, *args, **kwargs)
