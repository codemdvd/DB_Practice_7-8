# Generated by Django 4.0.5 on 2022-12-01 22:31

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task_id', models.IntegerField(verbose_name='Номер задания')),
                ('task_name', models.CharField(max_length=30, verbose_name='Название')),
                ('creation_date', models.DateField(verbose_name='Дата создания')),
                ('period_of_execution', models.CharField(max_length=20, verbose_name='Продолжительность')),
                ('contact_person_id', models.IntegerField(verbose_name='Контакт')),
                ('executor_id', models.IntegerField(verbose_name='ID исполнителя')),
                ('contract_number', models.IntegerField(verbose_name='Номер контракта')),
                ('task_status', models.CharField(max_length=30, verbose_name='Статус')),
                ('author_id', models.IntegerField(verbose_name='ID исполнителя')),
                ('end_date', models.DateField(verbose_name='Дата окончания')),
            ],
        ),
    ]
