from django.shortcuts import render
from .models import *
from .serializers import *


from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import filters,generics,status,mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated,IsAdminUser

class Cutomers(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class Cart(generics.ListCreateAPIView):
    queryset = CartModel.objects.all()
    serializer_class= CartModelSerializer 


      

# Payment
# Mail the Bill to the user (need to add) 

class Cartpay(generics.RetrieveAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes=[IsAuthenticated]

    queryset = CartModel.objects.all()
    serializer_class = CartModelSerializer
    queryset = WalletModel.objects.all()
    serializer_class = WalletModelSerializer

    def retrieve(self, request):
        try:
            # pdb.set_trace()

            current_user = request.user.id

            # user's cart
            cart = CartModel.objects.get(user=current_user)
            foods = cart.food.all()
            total = sum(food.price for food in foods)

            #past_order
            past_order = CompletedOrderModel(user=cart.user, store=cart.store)
            past_order.save()
            for food in foods:
                past_order.food.add(food)

            # Clear the cart
            cart.food.clear()
            cart.clean()

            # user's wallet
            wallet = WalletModel.objects.get(user=current_user)
            balance = wallet.money

            if balance >= total:
                balance -= total
                wallet.money = balance
                wallet.save()
                return Response({"balance in wallet": balance})
            
            return Response({'message': "Don't have enough money"})
        
        except CartModel.DoesNotExist:
            return Response({'message': "Purchase failed"})
        


class TotalAmount(generics.RetrieveAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = CartModelSerializer

    def retrieve(self, request):
        try:
            current_user = request.user.id
            cart = CartModel.objects.get(user=current_user)
            foods = cart.food.all()
            total = sum(food.price for food in foods)
            return Response({"total_amount": total})
        except CartModel.DoesNotExist:
            return Response({'message': "Cart not found"})


class Address(generics.RetrieveAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = DeliveryModelSerializer
    def get(self, request,type):
        try:
            current_user = request.user
            address = DeliveryModel.objects.get(user=current_user)
            serializer = self.serializer_class(address)
            if type == "home":
                return Response({
                    'home_address': address.home,
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    'office_address': address.office,
                }, status=status.HTTP_200_OK)
        except DeliveryModel.DoesNotExist:
            return Response({"detail": "User address not found"}, status=status.HTTP_404_NOT_FOUND)
        
