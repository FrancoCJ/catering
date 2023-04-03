from django.db import models
from django.contrib.auth.models import User



class formularios(models.Model):
    Nombre = models.CharField(max_length=50)
    Lunes= models.CharField(max_length=50)
    Martes= models.CharField(max_length=50)
    Miercoles= models.CharField(max_length=50)
    Jueves= models.CharField(max_length=50)
    Viernes = models.CharField(max_length=50)


class SubirMenu(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='menu_images/')

    def __str__(self):
        return self.name
    
#class User(models.Model):
#    username = models.CharField(max_length=50)
#    password = models.CharField(max_length=50)
    
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)