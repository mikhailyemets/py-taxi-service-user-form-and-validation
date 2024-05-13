from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms
from taxi.models import Driver, Car


def validate_license_number(license_number):
    if len(license_number) != 8:
        raise forms.ValidationError(
            "License number MUST consist of 8 characters"
        )
    if not license_number[:3].isalpha() or not license_number[:3].isupper():
        raise forms.ValidationError(
            "License number MUST start with 3 uppercase letters"
        )
    if not license_number[3:].isdigit():
        raise forms.ValidationError(
            "Last 5 characters MUST be digits"
        )
    return license_number


class DriverUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "license_number",
        )

    def clean_license_number(self) -> str:
        return validate_license_number(self.cleaned_data["license_number"])


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ["license_number"]

    def clean_license_number(self) -> str:
        return validate_license_number(self.cleaned_data["license_number"])


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = Car
        fields = "__all__"
