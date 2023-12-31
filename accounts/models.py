from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.gis.db import models as gismodels
from django.contrib.gis.geos import Point

# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self, first_name, last_name, username, email, password=None):
        if not email:
            raise ValueError('User must have an email address')
        
        if not username:
            raise ValueError('User must have a username')
        
        user = self.model(
            email = self.normalize_email(email), #normalize the email address
            username = username,
            first_name = first_name,
            last_name = last_name,
        )

        user.set_password(password)
        user.save(using=self._db) #define the default database to save the info
        return user

    def create_superuser(self, first_name, last_name, username, email, password=None):
        # create a user first
        user = self.create_user(
            email = self.normalize_email(email),
            username = username,
            password = password,
            first_name = first_name,
            last_name = last_name,
        )
        # set it to superuser
        # user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser): # will get full control of this user model
    # role to choose
    VENDOR = 1
    CUSTOMER = 2

    ROLE_CHOICE = (
        (VENDOR, 'Vendor'),
        (CUSTOMER, 'Customer')
    )

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    phone_number = models.CharField(max_length=12, blank=True)
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICE, blank=True, null=True)

    #required fields
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    # is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    objects = UserManager()

    #use email to list the items in model
    def __str__(self) -> str:
        return self.email
    
    def has_perm(self, perm, obj=None):
        return self.is_superadmin

    def has_module_perms(self, app_label):
        return True
    
    def get_role(self): # get the role of the user
        if self.role == 1:
            user_role = 'Vendor'
        elif self.role == 2:
            user_role = "Customer"
        return user_role

class UserProfile(models.Model):
    # based on the class User before to create user profile
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    # ForeignField when one user can have several profiles
    profile_picture = models.ImageField(upload_to='users/profile_pictures', blank=True, null=True)
    cover_picture = models.ImageField(upload_to='users/cover_pictures', blank=True, null=True)
    address = models.CharField(max_length=250, blank=True, null=True)
    country = models.CharField(max_length=15, blank=True, null=True)
    state = models.CharField(max_length=15, blank=True, null=True)
    city = models.CharField(max_length=15, blank=True, null=True)
    zip_code = models.CharField(max_length=6, blank=True, null=True)
    lattitude = models.CharField(max_length=20, blank=True, null=True)
    longtitude = models.CharField(max_length=20, blank=True, null=True)
    # get location point from gis django
    location = gismodels.PointField(blank=True, null=True, srid=4326) #4326 is default
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    # def full_address(self):
    #     return f"{self.address_line1}, {self.address_line2}"

    def __str__(self) -> str:
        return self.user.email # email is from class User

    def save(self, *args, **kwargs):
        if self.lattitude and self.longtitude:
            # must pass longtitude first
            self.location = Point(float(self.longtitude), float(self.lattitude))
            return super(UserProfile, self).save(*args, **kwargs)
        return super(UserProfile, self).save(*args, **kwargs) 
        # run method without lat and long, too