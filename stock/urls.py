from django.urls import path

from . import views

urlpatterns = [
    path("in/", views.stock_in, name="stock_in"),
    path("adjust/", views.stock_adjustment, name="stock_adjustment"),
    path("movements/", views.stock_movements, name="stock_movements"),
    path("low/", views.low_stock, name="low_stock"),
]
