from django.urls import path
from .views import *

urlpatterns = [

    path('',sample),
    path('store/',StoreListCreate.as_view()),
    path('store/<int:pk>/',StoreRetrieveUpdateDestroy.as_view()),
    path('food/',FoodListCreate.as_view()),
    path('food/<int:pk>/',FoodRetrieveUpdateDestroy.as_view()),
    path('dinein/',DineInListCreate.as_view()),
    path('dinein/<int:pk>/',DineInRetrieveUpdateDestroy.as_view()),

    path("mail/",offer_Notification),
    path("offer/<int:pk>",New_offer),

    path('book/<int:pk>/<int:select_time>/<int:table_count>',DineIn_Book.as_view()),


]
