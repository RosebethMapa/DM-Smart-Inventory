from django.urls import path

from . import views

urlpatterns = [
    path("orders/", views.order_menu, name="order_menu"),
    path("orders/history/", views.order_history, name="order_history"),
    path("orders/<int:pk>/<str:status>/", views.set_order_status, name="set_order_status"),
    path("pos/", views.pos, name="pos"),
    path("lookup/", views.product_lookup, name="product_lookup"),
    path("<int:pk>/receipt/", views.receipt, name="receipt"),
]
