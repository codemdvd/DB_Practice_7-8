from .models import Task, Employee
from django.forms import ModelForm, TextInput, DateInput, EmailField, PasswordInput
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django import forms


class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = ['task_id',
                 'task_name',
                 'creation_date',
                 'end_date',
                 'contact_person',
                 'executor',
                 'contract_number',
                 'task_status',
                 'author']
        widgets = {
            "task_id": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Номер задания'
            }),
             "task_name": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Название задания'
            }),
             "creation_date": DateInput(attrs={
                'class': 'form-control',
                'placeholder': 'Дата создания задания'
            }),
             "end_date": DateInput(attrs={
                'class': 'form-control',
                'placeholder': 'Дата создания задания'
            }),
             "contact_person": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'ID контактного лица'
            }),
             "executor": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'ID исполнителя'
            }),
             "contract_number": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Номер контракта'
            }),
             "task_status": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Статус'
            }),
             "author": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'ID автора'
            })
                }
class EmployeeForm(ModelForm):
    class Meta:
        model = Employee
        fields = [
            'employee_id',
            'employee_name',
            'position',
            'USERNAME_FIELD',
            'password'
        ]
        widgets = {
            "employee_id": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'ID сотрудника'
            }),
            "employee_name": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Имя сотрудника'
            }),
            "position": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Номер должность'
            }),
            "USERNAME_FIELD": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Логин'
            }),
            "password": PasswordInput(attrs={
                'class': 'form-control',
                'placeholder': 'Пароль'
            }),

        }
class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('username',)

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password1'] != cd['password2']:
            raise forms.ValidationError('Пароли не совпадают')
        return cd['password2']

class TaskUpdateForm(ModelForm):
    class Meta:
        model = Task
        fields = [
            'end_date'
        ]
        widgets = {
            "end_date": DateInput(attrs={
                'class' : 'form-control',
                'placeholder' : 'Дата завершения'
            })
        }




        