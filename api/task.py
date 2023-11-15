# tasks.py
from celery import shared_task
from django.core.mail import send_mail
from django.contrib.auth.models import User
from .models import StoreModel
from rest_framework.response import Response
from django.core.mail import send_mail

@shared_task
def send_offer_notification():
    stores_with_offers = StoreModel.objects.filter(hasOffer=True)
    if stores_with_offers:
        store_names = [store.name for store in stores_with_offers]
        subject = "Grand Offer"
        message = f"These stores have ongoing offers now: {', '.join(store_names)}"
        allmails = User.objects.values_list('email', flat=True)
        if allmails:
            from_email = "mforsapmers@gmail.com"
            send_mail(subject, message, from_email, allmails)
            return {"message": "Offer notifications sent successfully."}
    
    return {"message": "No stores with offers found."}
