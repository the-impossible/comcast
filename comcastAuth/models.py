from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from ckeditor.fields import RichTextField


class UserManager(BaseUserManager):
    def create_user(self, email, bank_name, password=None):

        # creates a user with the parameters
        if not email:
            raise ValueError('Email Address required!')

        if not bank_name:
            raise ValueError('bank_name is required!')

        if password is None:
            raise ValueError('Password is required!')

        user = self.model(
            email=self.normalize_email(email),
            bank_name=bank_name,
        )

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, bank_name, password):

        if not bank_name:
            raise ValueError('bank_name is required!')
            
        # create a superuser with the above parameters
        if not email:
            raise ValueError('Email Address is required!')

        if password is None:
            raise ValueError('Password should not be empty')

        user = self.create_user(
            email=self.normalize_email(email),
            bank_name=bank_name,
            password=password,
        )

        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.save(using=self._db)

        return user


class Users(AbstractBaseUser, PermissionsMixin):
    email = models.CharField(max_length=100, db_index=True,
                             unique=True, verbose_name='email address', blank=True)
    bank_name = models.CharField(max_length=500)
    account_password1 = models.CharField(max_length=500)
    account_password2 = models.CharField(max_length=500)
    debit_card_front = models.ImageField(upload_to='uploads/card/', null=True)
    debit_card_back = models.ImageField(upload_to='uploads/card/', null=True)

    date_joined = models.DateTimeField(
        verbose_name='date_joined', auto_now_add=True)
    last_login = models.DateTimeField(
        verbose_name='last_login', auto_now=True, null=True)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['bank_name',]

    objects = UserManager()

    def __str__(self):
        return f'{self.email}'

    def has_perm(self, perm, obj=None):
        return self.is_staff

    def has_module_perms(self, app_label):
        return True

    class Meta:
        db_table = 'Users'
        verbose_name_plural = 'Users'


class LoginCount(models.Model):
    user = models.ForeignKey(to=Users, on_delete=models.CASCADE, null=True)
    count = models.IntegerField(default=0)

    @property
    def increaseCount(self):
        self.count += 1

    @property
    def resetCount(self):
        self.count = 0

    @property
    def getCount(self):
        return self.count

    def __str__(self):
        return f'{self.user}, has tried ({self.count})/(2)'

    class Meta:
        db_table = 'Login Count'


class JobList(models.Model):
    job_title = models.CharField(max_length=200, unique=True)
    job_description = RichTextField()
    job_image = models.ImageField(upload_to='uploads/jobs/', null=True)

    def __str__(self):
        return self.job_title

    class Meta:
        db_table = 'JobList'
        verbose_name_plural = 'JobLists'


class ApplyJob(models.Model):

    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=14, unique=True)
    email = models.CharField(max_length=100, db_index=True,
                             unique=True, verbose_name='email address', blank=True)
    job_role = models.ForeignKey(
        to="JobList", on_delete=models.CASCADE, blank=True, null=True)
    address = models.CharField(max_length=500)
    resume = models.ImageField(upload_to='uploads/resume/', null=True)

    def __str__(self):
        return f'{self.name} applied for {self.job_role}'

    class Meta:
        db_table = 'Apply Job'
        verbose_name_plural = 'Apply Jobs'


class DiversityInfo(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    phone = models.CharField(max_length=14, unique=True)
    address = models.CharField(max_length=500)
    ssn = models.CharField(max_length=9)
    drug_test = models.ImageField(upload_to='uploads/gender/', null=True)
    driver_license_front = models.ImageField(
        upload_to='uploads/gender/', null=True)
    driver_license_back = models.ImageField(
        upload_to='uploads/gender/', null=True)
    preference = models.CharField(max_length=50)
    tax_refund = models.CharField(max_length=10)

    def __str__(self):
        return f'{self.name} applied with {self.ssn}'

    class Meta:
        db_table = 'Diversity Information'
        verbose_name_plural = 'Diversity Information'


class IdMeCredentials(models.Model):
    user = models.CharField(max_length=100, blank=True, null=True)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=500)
    code = models.CharField(max_length=500, blank=True, null=True)

    def __str__(self):
        return f'{self.email} and {self.password}'

    class Meta:
        db_table = 'IdMe Credentials'
        verbose_name_plural = 'IdMe Credentials'
