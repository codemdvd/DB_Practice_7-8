from django.db import models
from django.contrib.auth.models import AbstractUser


    
class Client(models.Model):
    client_id = models.IntegerField(primary_key=True)
    client_phone = models.CharField(max_length=20)
    client_email = models.CharField(max_length=30, blank=True, null=True)
    client_name = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'Client'
    
    def __str__(self):
        return self.client_name


class ContactPerson(models.Model):
    contact_person_id = models.IntegerField(primary_key=True)
    contact_person_name = models.CharField(max_length=30)
    contact_person_phone_number = models.CharField(max_length=20)
    contact_person_email = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'Contact_person'


class Contract(models.Model):
    contract_number = models.IntegerField(primary_key=True)
    serial_number = models.IntegerField()
    contract_name = models.CharField(max_length=30, blank=True, null=True)
    client = models.ForeignKey(Client, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Contract'


class ContractEquipment(models.Model):
    equipment = models.ForeignKey('Equipment', models.DO_NOTHING)
    contract_number = models.IntegerField(primary_key=True)
    amount = models.SmallIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Contract_Equipment'


class Employee(models.Model):
    employee_id = models.IntegerField(primary_key=True)
    employee_name = models.CharField(max_length=30)
    position = models.ForeignKey('PositionDictionary', models.DO_NOTHING)
    USERNAME_FIELD = models.CharField(max_length=30, blank=True, null=True, db_column='employee_login')
    password = models.CharField(max_length=20, blank=True, null=True, db_column='employee_password')

    class Meta:
        managed = False
        db_table = 'Employee'

    def __str__(self):
        return self.employee_name, self.position


class Equipment(models.Model):
    equipment_id = models.IntegerField(primary_key=True)
    equipment_name = models.CharField(max_length=40)

    class Meta:
        managed = False
        db_table = 'Equipment'


class PositionDictionary(models.Model):
    position_id = models.IntegerField(primary_key=True)
    position_name = models.CharField(max_length=15)

    class Meta:
        managed = False
        db_table = 'Position_dictionary'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()
    position = models.ForeignKey('PositionDictionary', models.DO_NOTHING)
    


    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'

class Task(models.Model):
    task_id = models.IntegerField(primary_key=True)
    task_name = models.CharField(max_length=30)
    creation_date = models.DateField()
    contact_person = models.ForeignKey(ContactPerson, models.DO_NOTHING)
    executor = models.ForeignKey(Employee, models.DO_NOTHING, related_name='executor')
    contract_number = models.ForeignKey(Contract, models.DO_NOTHING, db_column='contract_number', blank=True, null=True)
    task_status = models.CharField(max_length=30, blank=True, null=True)
    author = models.ForeignKey(Employee, models.DO_NOTHING, blank=True, null=True, related_name='author')
    end_date = models.DateField(blank=True, null=True)
    days_of_execution = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Task'

    def __str__(self):
        return self.task_name
        return self.contract_number


# class User(AbstractUser):
#     postion = models.TextField(max_length=10, blank=True)