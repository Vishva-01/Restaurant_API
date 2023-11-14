from django.contrib import admin
from .models import *

class CartAdmin(admin.ModelAdmin):
    list_display = ('user',)
admin.site.register(CartModel, CartAdmin)

class DeliveryAdmin(admin.ModelAdmin):
    list_display = ('user', 'home', 'office')
admin.site.register(DeliveryModel,DeliveryAdmin)


class WalletAdmin(admin.ModelAdmin):
    list_display=('user','money')
admin.site.register(WalletModel,WalletAdmin)


admin.site.register(CompletedOrderModel)