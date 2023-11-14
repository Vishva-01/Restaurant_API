from django.shortcuts import render
from .models import *
from .serializers import *
from django.core.mail import send_mail

from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status,filters,generics,mixins
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework.authentication import TokenAuthentication

@api_view(["GET"])
def sample(request):
    return Response({"message" : " This is the msg"},status=status.HTTP_200_OK)


class StoreListCreate(generics.ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    queryset  = StoreModel.objects.all()
    serializer_class = StoreModelSerializer

class StoreRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = StoreModel.objects.all()
    serializer_class = StoreModelSerializer


class FoodListCreate(generics.ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = FoodModelSerializer

    def get_queryset(self):
        user_stores = StoreModel.objects.filter(user=self.request.user)
        return FoodModel.objects.filter(store__in=user_stores)


class FoodRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = FoodModelSerializer

    def get_queryset(self):
        user_store = StoreModel.objects.get(user=self.request.user)
        return FoodModel.objects.filter(store=user_store)
    
    def get_object(self):
        # Override get_object to filter based on the user's store
        queryset = self.get_queryset()
        obj = generics.get_object_or_404(queryset, pk=self.kwargs['pk'])
        self.check_object_permissions(self.request, obj)
        return obj


class DineInListCreate(generics.ListCreateAPIView):
    queryset  = DineInModel.objects.all()
    serializer_class = DineInModelSerializer

class DineInRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = DineInModel.objects.all()
    serializer_class = DineInModelSerializer


# Offer Notifiction via Mail
@api_view(["GET"])
def offer_Notification(request):
    stores_with_offers = StoreModel.objects.filter(hasOffer=True)
    if stores_with_offers:
        store_names = [store.name for store in stores_with_offers]
        subject = "Grand Offer"
        message = f"These stores have ongoing offers now: {', '.join(store_names)}"
        allmails = User.objects.values_list('email', flat=True)
        if allmails:
            from_email = "mforsapmers@gmail.com"
            send_mail(subject, message, from_email, allmails)
            return Response({"message": "Offer notifications sent successfully."}, status=200)
    
    return Response({"message": "No stores with offers found."}, status=200)

@api_view(["PATCH"])
def New_offer(request,pk):
    store = StoreModel.objects.get(id = pk)
    
    data={
        "hasOffer": True
    }

    serializer = StoreModelSerializer(store,data = data,partial = True)
    if serializer.is_valid():
        serializer.save()
        subject = "Grand Offer"
        message = f"These stores have ongoing offers now: {store}"
        allmails = User.objects.values_list('email', flat=True)
        if allmails:
            from_email = "mforsapmers@gmail.com"
            send_mail(subject, message, from_email, allmails)
        return Response(serializer.data,status=status.HTTP_202_ACCEPTED)
    return Response(serializer.errors,status=status.HTTP_404_NOT_FOUND)
  



class DineIn_Book(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def patch(self, request, pk, select_time, table_count):
        try:
            email = request.user.email
            store = StoreModel.objects.get(id=pk)
            booking = DineInModel.objects.get(store=pk)
            
            if select_time == 1:
                available = booking.Morning_available_table
                if table_count <= available:
                    booking.Morning_available_table = available - table_count
            elif select_time == 2:
                available = booking.Afternoon_available_table
                if table_count <= available:
                    booking.Afternoon_available_table = available - table_count
            else:
                available = booking.Evening_available_table
                if table_count <= available:
                    booking.Evening_available_table = available - table_count


            booking.save()

            if select_time in [1, 2, 3]:
                time = {
                    1: "Morning",
                    2: "Afternoon",
                    3: "Evening",
                }
                subject = "Table Booking"
                message = f"{table_count} tables were booked in {store.name} on {time[select_time]}"
                sender = "mforspamers@gmail.com"
                receiver = [email, store.user.email]
                send_mail(subject, message, sender, receiver)

            return Response(DineInModelSerializer(booking).data, status=status.HTTP_200_OK)
        except StoreModel.DoesNotExist:
            return Response({"detail": "Store not found"}, status=status.HTTP_404_NOT_FOUND)













