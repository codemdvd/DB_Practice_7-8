from django.urls import path
from hello import views
from .views import LoginUser

urlpatterns = [
    path("", LoginUser.as_view(), name="home"),
    path("hello/<name>", views.hello_there, name="hello_there"),
    path("choice/", views.choice, name ="choice"),
    path("tasks/", views.tasks, name ="tasks"),
    path("task_date/", views.task_date, name ="task_date"),
    path("clients/", views.clients, name ="clients"),
    path("new_emp/", views.new_emp, name ="new_emp"),
    path("register/", views.register, name="register"),
    path("report/", views.report, name ="report"),
    path("new_task/", views.new_task, name="new_task"),
    path("all_tasks/", views.all_tasks, name="all_tasks"),
    path("detail_view/", views.detail_view, name="detail_view"),
    path("permission/", views.new_task, name="permision"),
    path("download_file/", views.download_file, name="download_file")


]