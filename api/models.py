from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

class AccountManager(BaseUserManager):

    def create_superuser(self, email, username, name, password, **other_fields):

        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)
        other_fields.setdefault('role', 'Administrator')

        if other_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must be assigned to is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must be assigned to is_superuser=True.')

        return self.create_user(email, username, name, password, **other_fields)

    def create_user(self, email, username, name, password, **other_fields):

        if not email:
            raise ValueError('You must provide an email address')

        email = self.normalize_email(email)
        user = self.model(email=email, username=username,
                          name=name, **other_fields)
        user.set_password(password)
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):
    def defaultPermission():
        default = Permissions.objects.filter(id=1)
        return default
    
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, unique=True)
    name = models.CharField(max_length=150)
    avatar = models.ImageField(null=True, blank=True)
    
    SPONSOR = 'sponsor'
    BENEFICIARY = 'Beneficiary'
    ADMINISTRATOR = 'Administrator'
    Role = [
		(SPONSOR, 'Sponsor'),
		(BENEFICIARY, 'Beneficiary'),
		(ADMINISTRATOR, 'Administrator'),
	]

    role = models.CharField(max_length=200, choices=Role, blank=True, null=True)

    address = models.TextField(null=True, blank=True)
    last_login = models.CharField(default='Yesterday', null=True, blank=True, max_length=200)    
    

    # projects = models.ManyToManyField('Project', blank=True)
    permissions = models.ManyToManyField('Permissions', default=defaultPermission, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True,null=True, blank=True)
	
    objects = AccountManager()
	
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['name','email']

    def __str__(self):
    	return self.name

class Permissions(models.Model):
	name = models.CharField(max_length=200)
	guard_name = models.CharField(max_length=200,null=True,blank=True)
	created_at = models.DateTimeField(auto_now_add=True,null=True)
	updated_at = models.DateTimeField(auto_now=True,null=True,blank=True)

	class Meta:
		verbose_name_plural = 'Permissions'

	def __str__(self):
		return self.name


class Sponsor(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
         return self.user.name

class Beneficiary(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
         verbose_name_plural = 'Beneficiaries'

    def __str__(self):
         return self.user.name
     
class Project(models.Model):
    name = models.CharField(max_length=200,null=True)
    avatar = models.ImageField(null=True, blank=True, max_length=200)
    orders = models.ManyToManyField('Order',blank=True)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    sponsors = models.ManyToManyField(Sponsor, blank=True)
    description = models.TextField(null=True, blank=True)
    budget = models.FloatField(null=True)
    earnings = models.FloatField(null=True)
    tasks = models.ManyToManyField('Task', blank=True)
    start_date = models.DateTimeField(null=True)
    due_date = models.DateTimeField(null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
         return self.name

class Order(models.Model):
    pass

class Task(models.Model):
    name = models.CharField(max_length=200)
    completed = models.BooleanField(default=False)
    due_date = models.DateTimeField()

    def __str__(self):
        return self.name

