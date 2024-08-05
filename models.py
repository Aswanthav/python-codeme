from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Blog(models.Model):
    cat_choice = (("Education","Education"),
                  ("sports","sports"),
                  ("Food","food"),
                  ("Bussiness","Bussiness"),
                  ("movie","movie"),
                  ("Entertainment","Entertainment"),
                  ("Technology","Tecnology"),
                  ("Fasion","Fasion"),
                 )
    fk_user = models.ForeignKey(User,on_delete=models.CASCADE)
    title = models.CharField(max_length=30,null = True)
    context = models.TextField(null=True)
    image =models.ImageField(upload_to='image/',null=True)
    category = models.CharField(max_length=20,choices=cat_choice,default="movie")
    created_date =models.DateTimeField(auto_now= True)
    update_date = models.DateTimeField(auto_now_add=True)
    is_published = models.BooleanField(default=False)

    def _str_(self):
        return self.title
    
    

class Comment(models.Model):
    comment = models.TextField(null=True)
    fk_user = models.ForeignKey(User,on_delete=models.CASCADE)
    fk_blog = models.ForeignKey(Blog,on_delete=models.CASCADE)
    created_date =models.DateTimeField(auto_now= True)
    update_date = models.DateTimeField(auto_now_add=True)


class Profile(models.Model):
    gender_choice = (("male","male"),
                     ("female","female"),
                     ("other","other"),
    )
    name = models.OneToOneField(User,on_delete=models.CASCADE,related_name="profile")
    address = models.TextField(null=True)
    phone = models.IntegerField(null=True)
    email = models.EmailField(null=True)
    gender = models.CharField(choices=gender_choice,default="male",max_length=150)
    image = models.ImageField(upload_to='image/') 
    date_of_birth = models.DateField(null=True,blank=True)
    created_date =models.DateTimeField(auto_now= True)
    update_date = models.DateTimeField(auto_now_add=True)  

    def __str__(self):
        return self.name.username
    

class UserOTP(models.Model):
    otp = models.CharField(max_length=5)
    fk_user = models.OneToOneField(User,on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now= True)
    update_date = models.DateTimeField(auto_now_add=True)


class Sample(models.Model):
    title = models.CharField(max_length=10)
    description = models.TextField()

