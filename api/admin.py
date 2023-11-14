from django.contrib import admin
from .models import *

admin.site.register(StoreModel)

class FoodAdmin(admin.ModelAdmin):
    list_display = ('store',"price",'food')
admin.site.register(FoodModel,FoodAdmin)

class DineInAdmin(admin.ModelAdmin):
    list_display=('store','Morning_available_table', 'Afternoon_available_table', 'Evening_available_table')
admin.site.register(DineInModel,DineInAdmin)