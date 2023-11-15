from rest_framework import serializers   
from .models import *


class StoreModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoreModel
        fields = "__all__"

class FoodModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodModel
        fields = "__all__"

class DineInModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = DineInModel
        fields = "__all__"


