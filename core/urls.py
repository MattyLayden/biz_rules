from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from . import views
from .views import ObjectListAPIView
from .views import CustomerAPI

urlpatterns = [
    path("", csrf_exempt(views.CustomerAPI.as_view()), name="customer_api"),
    path("objects/", ObjectListAPIView.as_view(), name="object-list")
]
