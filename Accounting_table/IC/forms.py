from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.forms import ClearableFileInput

from .models import *


# форма связанная с службой
class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['title', ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
        }


# форма связанная с отделом/группой
class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['title', 'PPRTD_weight', 'PFVIR_weight', 'service']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'PPRTD_weight': forms.NumberInput(attrs={'class': 'form-control'}),
            'PFVIR_weight': forms.NumberInput(attrs={'class': 'form-control'}),
            'service': forms.Select(attrs={'class': 'form-select'}),
        }


# форма для показателя
class IndicatorForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['department'].empty_label = "Отдел/группа не выбраны"

    class Meta:
        model = Indicator
        fields = ['id', 'title', 'units', 'comment', 'target_indicator', 'actual_indicator',
                  'Significance_of_indicator', 'Plan', 'department']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'units': forms.TextInput(attrs={'class': 'form-control'}),
            'comment': forms.Textarea(attrs={'class': 'form-control'}),
            'target_indicator': forms.NumberInput(attrs={'class': 'form-control'}),
            'actual_indicator': forms.NumberInput(attrs={'class': 'form-control'}),
            'Significance_of_indicator': forms.NumberInput(attrs={'class': 'form-control'}),
            'Plan': forms.NumberInput(attrs={'class': 'form-control'}),
            'department': forms.Select(attrs={'class': 'form-select'}),
            # 'Confirmation_document': forms.FileInput(attrs={'class':'form-control','type':'file', 'accept':'application/pdf'})
        }




class Indicator_input_actual_Form(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['department'].empty_label = "Отдел/группа не выбраны"

    class Meta:
        model = Indicator
        fields = ['id', 'title', 'units', 'comment', 'target_indicator', 'actual_indicator',
                  'Significance_of_indicator', 'Plan', 'department']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control-plaintext', 'disabled': 'disabled'}),
            'units': forms.TextInput(attrs={'class': 'form-control'}),
            'comment': forms.Textarea(attrs={'class': 'form-control'}),
            'target_indicator': forms.NumberInput(attrs={'class': 'form-control-plaintext', 'disabled': 'disabled'}),
            'actual_indicator': forms.NumberInput(attrs={'class': 'form-control'}),
            'Significance_of_indicator': forms.NumberInput(attrs={'class': 'form-control'}),
            'Plan': forms.NumberInput(attrs={'class': 'form-control'}),
            'department': forms.Select(attrs={'class': 'form-control-plaintext',  'id':"exampleDataList", 'disabled': 'disabled'}),
            # 'Confirmation_document': forms.FileInput(attrs={'class':'form-control','type':'file', 'accept':'application/pdf'})
        }







# форма связанная с файлам показателя
class Indicators_fileForm(forms.ModelForm):
    class Meta:
        model = Indicators_file
        fields = ['confirmation_document']
        widgets = {
            'confirmation_document': ClearableFileInput(
                attrs={'multiple': True, 'class': "form-control", 'type': "file", 'id': "formFile"})
        }


# форма связанная с критически важными сервисами/службами
class Crtitical_serviceForm(forms.ModelForm):
    class Meta:
        model = Critical_service
        fields = ['title', 'working_mode_days', 'working_mode_hours', 'working_days_period', 'Operating_time_actual',
                  'Service_ownership']

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'working_mode_days': forms.NumberInput(attrs={'class': 'form-control'}),
            'working_mode_hours': forms.NumberInput(attrs={'class': 'form-control'}),
            'working_days_period': forms.NumberInput(attrs={'class': 'form-control'}),
            'Operating_time_actual': forms.NumberInput(attrs={'class': 'form-control'}),
            'Service_ownership': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean_working_mode_days(self):
        buffer = self.cleaned_data['working_mode_days']
        if 1 > buffer > 7:
            raise ValidationError('Введите число меньше или равно 7')
        return buffer

    def clean_working_mode_hours(self):
        buffer = self.cleaned_data['working_mode_hours']
        if 1 > buffer > 24:
            raise ValidationError('Введите число меньше или равно 24')
        return buffer

        # а если человек введёт часов больше чем это вообще возможно?


# форма регистрации пользователя
class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Повтор пароля', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


# форма авторизации пользователя
class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
