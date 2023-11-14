from django.db import models
from django.contrib.auth.models import User
from api.models import *

class CartModel(models.Model):
    user = models.OneToOneField(User,on_delete= models.CASCADE)
    store = models.ForeignKey(StoreModel, on_delete= models.CASCADE)
    food = models.ManyToManyField(FoodModel)


class CompletedOrderModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    store = models.ForeignKey(StoreModel, on_delete=models.CASCADE)
    food = models.ManyToManyField(FoodModel)

class DeliveryModel(models.Model):
    user = models.OneToOneField(User,on_delete= models.CASCADE)
    home = models.TextField()
    office = models.TextField()

class WalletModel(models.Model):
    user = models.OneToOneField(User,on_delete= models.CASCADE)
    money = models.IntegerField()

