from django.urls import path
from .views import *

urlpatterns = [
    path('customer/',Cutomers.as_view()),
    path('cart/',Cart.as_view()),

    path("pay/",Cartpay.as_view()),
    path('get/', TotalAmount.as_view()),

    path('select/<str:type>',Address.as_view()),
]
