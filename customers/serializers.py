from rest_framework import serializers
from django.contrib.auth.models import User
from .models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields =  "__all__"


class DeliveryModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryModel
        fields = "__all__"

class CartModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartModel
        fields = "__all__"


class CompletedOrderModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompletedOrderModel
        fields = "__all__"


class WalletModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = WalletModel
        fields = "__all__"