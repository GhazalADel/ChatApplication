from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager

# for create super users and noraml users
class MyAccountManager(BaseUserManager):
      
      def create_user(self,phone,username,password=None):
            if not phone:
                  raise ValueError("Users must have a phone number!")
            if not username:
                  raise ValueError("Users must have a username!")
            user=self.model(phone=phone,username=username)
            user.set_password(password)
            user.save(using=self._db)
            return user
      def create_superuser(self,phone,username,password):
            user=self.create_user(phone=phone,username=username,password=password)
            #make user `super`
            user.is_admin=True
            user.is_staff=True
            user.is_superuser=True
            user.is_active=True
            user.save(using=self._db)
            return user

def get_profile_image_path(self):
	return 'profile_images/' + str(self.pk) + '/profile_image.png'
def get_default_profile_image_path():
      return 'defaultPro.png'
      

class Account(AbstractBaseUser):
    username=models.CharField(max_length=25,unique=True)
    phone=models.CharField(max_length=11,unique=True)
    date_joined=models.DateTimeField(verbose_name="date joined",auto_now_add=True)
    last_login=models.DateTimeField(auto_now=True)
    profile_image=models.ImageField(max_length=255,upload_to=get_profile_image_path,null=True,blank=True,default=get_default_profile_image_path)
    hide_phone=models.BooleanField(default=True)
    #for personalizing django user mode
    is_admin=models.BooleanField(default=False)
    is_active=models.BooleanField(default=True)
    is_staff=models.BooleanField(default=False)
    is_superuser=models.BooleanField(default=False)

    #set manager to model
    objects=MyAccountManager()
    
    USERNAME_FIELD='phone'
    REQUIRED_FIELDS=['username']
    
    def __str__(self):
          return self.username
    
    def has_perm(self,perm,obj=None):
          return self.is_admin
    
    def has_module_perms(self,app_label):
          return True
    
    def get_profile_image_name(self):
          comp_path=str(self.profile_image)
          return comp_path[str(self.profile_image).index(f'profile_images/f{self.pk}/'):]
          
    
