# apps/pins/urls.py
from django.urls import path
from . import views

app_name = 'pins'

urlpatterns = [
    # path('<str:username>/pins/', views.my_pins, name='my_pins'),
    path('<int:post_id>/toggle/', views.post_pin_toggle, name='post_pin_toggle'),
]
