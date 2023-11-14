from django.db import models
from django.contrib.auth.models import User

class StoreModel(models.Model):
    name = models.CharField(max_length=30)
    address = models.TextField()
    location = models.CharField(max_length=20)
    isOpen = models.BooleanField(default=True)
    hasOffer = models.BooleanField(default=False)
    user = models.ForeignKey(User,on_delete= models.CASCADE)

    def __str__(self):
        return self.name
    

class FoodModel(models.Model):
    store = models.ForeignKey(StoreModel,on_delete= models.CASCADE)
    food = models.CharField(max_length=20)
    price = models.IntegerField()

    def __str__(self):
        return self.food
    
class DineInModel(models.Model):
    store = models.OneToOneField(StoreModel,on_delete= models.CASCADE)
    Morning_available_table = models.IntegerField()
    Afternoon_available_table = models.IntegerField()
    Evening_available_table = models.IntegerField()

