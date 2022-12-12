import re
import os
import mimetypes
from django.utils.timezone import datetime
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import View, DetailView, ListView, CreateView, UpdateView
from django.shortcuts import redirect
from .forms import TaskForm, EmployeeForm, LoginUserForm, RegisterUserForm, TaskUpdateForm
from .models import Task, Client, Employee
from django.db.models import Q
from django import forms
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.db import connection
from django.http import StreamingHttpResponse
from wsgiref.util import FileWrapper

# def home(request):
#     error2= ''
#     if request.method == 'POST':
#         form2 = LoginForm(request.POST)
#         if form2.is_valid():
#             return redirect('choice')
#         else:
#             error2 = 'Неправильный логин и/или пароль'


#     form2 = LoginForm()

#     data1 = {
#         'form': form2,
#         'error': error2
#     }

#     return render(request, "hello/home.html",{'form':form2, 'error': error2})


def choice(request):
    return render(request, "hello/choice.html")

def tasks(request):
    manager =  False
    if request.user.is_authenticated:
        employee = Employee.objects.filter(position = 3)
        if employee:
            for el in employee:
                if el.USERNAME_FIELD == request.user.username:
                    manager = True

                    
    return render(request, "hello/tasks.html", {'manager': manager})

def task_date(request):
    notify = ''
    task_id = request.GET.get('task_id', '')
    new_date = request.GET.get('new_date', '')
    if task_id and new_date:
        if request.user.is_authenticated:
            employee = Employee.objects.all()
            if employee:
                for el in employee:
                    if el.USERNAME_FIELD == request.user.username:
                            cr1 = Q(executor = el.employee_id)
                            cr2 = Q(author = el.employee_id)
                            cr3 = Q(task_id = task_id)
                            task = Task.objects.get((cr1 | cr2) & cr3)
                            task.end_date = new_date
                            task.save()
                            notify = 'Дата сохранена' 


    return render(request, "hello/task_date.html", {'notify': notify})

# class TaskUpdateView(UpdateView):
#     model = Task
#     template_name = "hello/task_date.html"

#     form_class = TaskForm


def clients(request):
    search_query = request.GET.get('search', '')
    if search_query:
        client = Client.objects.filter(client_name__contains=search_query)
    else:
        client = Client.objects.all()

    return render(request, "hello/clients.html",{'client': client})

def new_emp(request, commit=True):
    error1= ''
    if request.method == 'POST':
        form1 = EmployeeForm(request.POST)
        if form1.is_valid():
            form1.save()
            return redirect('register')
        else:
            error1 = 'Форма неверно заполенна'

    admin =  False
    if request.user.is_authenticated:
        employee = Employee.objects.filter(position = 0)
        if employee:
            for el in employee:
                if el.USERNAME_FIELD == request.user.username:
                    admin = True


    form1 = EmployeeForm()

    data1 = {
        'form': form1,
        'error': error1
    }
    if admin == True:
        return render(request, "hello/new_emp.html", data1 )
    else:
        return render(request, "hello/permission.html")


def register(request):
    error = ''
    if request.method == 'POST':
        form2 = RegisterUserForm(request.POST)
        if form2.is_valid():
            new_user = form2.save(commit=False)
            # Set the chosen password
            new_user.set_password(form2.cleaned_data['password1'])
            # Save the User object
            new_user.save()
            return redirect('new_emp')
        else:
            form2 = RegisterUserForm()
            error = 'Пароли не совпадают'

    form2 = RegisterUserForm()

    

    data = {
        'form2': form2,
        'error': error
    }
    return render(request, "hello/register.html", data)


def new_task(request):
    error= ''
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('choice')
        else:
            error = 'Форма неверно заполенна'

    manager =  False
    if request.user.is_authenticated:
        employee = Employee.objects.filter(position = 3)
        if employee:
            for el in employee:
                if el.USERNAME_FIELD == request.user.username:
                    manager = True


    form = TaskForm()

    data = {
        'form': form,
        'error': error
    }
    if manager == True:
        return render(request, "hello/new_task.html", data)
    else:
        return render(request, "hello/permission.html")

def all_tasks(request):
    search_query = request.GET.get('search', '')
    c = 0
    if search_query:
        if request.user.is_authenticated:
            employee = Employee.objects.all()
            if employee:
                for el in employee:
                    if el.USERNAME_FIELD == request.user.username:
                        cr1 = Q(executor = el.employee_id)
                        cr2 = Q(author = el.employee_id)
                        cr3 = Q(task_name__contains=search_query)
                        task = Task.objects.filter((cr1 | cr2) & cr3)
                        for el in task:
                            c += 1
    else:
        if request.user.is_authenticated:
            employee = Employee.objects.all()
            if employee:
                for el in employee:
                    if el.USERNAME_FIELD == request.user.username:
                        cr1 = Q(executor = el.employee_id)
                        cr2 = Q(author = el.employee_id)
                        task = Task.objects.filter(cr1 | cr2)
                        for el in task:
                            c += 1
        else:
            return redirect('home')



    return render(request, "hello/all_tasks.html", {'task': task, 'employee': employee, 'c': c})


def hello_there(request):
    return render(
        request,
        'hello/hello_there.html',
    )

def detail_view(request):
    error1 = ''
    if request.method == "GET":
        query = request.GET.get('search')
        if query == '':
            query = 'None'
    error1 = 'Неверный запрос'
    return render(request, "hello/detail_view.html", {'query': query, 'tasks': tasks})

class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name= 'hello/home.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        return dict(list(context.items()))
    def get_success_url(self):
        return reverse_lazy('tasks')

def report(request):
    manager =  False
    if request.user.is_authenticated:
        employee = Employee.objects.filter(position = 3)
        if employee:
            for el in employee:
                if el.USERNAME_FIELD == request.user.username:
                    manager = True
    date1 = request.GET.get('date1', '')
    date2 = request.GET.get('date2', '')
    emp_id = request.GET.get('emp_id', '')
    if date1 and date2 and emp_id:
        if request.user.is_authenticated:
            employee = Employee.objects.all()
            if employee:
                for el in employee:
                    if el.USERNAME_FIELD == request.user.username:
                        cr1 = emp_id
                        cr2 = f"'{date1}'"
                        cr3 = f"'{date2}'"
                        cr4 = "'C:/Important/Studing1.3/DB/Practice2-5/report.csv'"
                        # criteries = ((cr1,), (cr2,), (cr3,), (cr4,))
                        with connection.cursor() as cursor:
                            cursor.execute(f"CALL export_to_csv({cr1},{cr2},{cr3},{cr4})")
    if manager == True:
        return render(request, "hello/report.html", {'date1': date1, 'date2': date2, })
    else:
        return render(request, "hello/permission.html")

    
def download_file(request, filename=''):
    file = 'C:/Important/Studing1.3/DB/Practice2-5/report.csv'
    filename = os.path.basename(file)
    chunk_size = 8192
    response = StreamingHttpResponse(FileWrapper(open(file, 'rb'), chunk_size),
                        content_type=mimetypes.guess_type(file)[0])
    response['Content-Length'] = os.path.getsize(file)    
    response['Content-Disposition'] = "attachment; filename=%s" % filename
    return response


# class RegisterUser(CreateView):
#     form_class = EmployeeForm
#     template_name = 'hello/new_emp.html'
#     success_url = reverse_lazy('tasks')

#     def get_context_data(self, *, object_list=None, **kwargs):
#         context = super().get_context_data(**kwargs)
#         return dict(list(context.items()))

#     def get_success_url(self):
#         return reverse_lazy('tasks')
    
#     def save(self, commit=True):
#     user = E
#     user.set_password(self.cleaned_data["password1"])
#     if commit:
#         user.save()
#     return user