from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.urls import include, path, re_path
from django.views.static import serve
from sales import views as sales_views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/login/", auth_views.LoginView.as_view(template_name="registration/login.html"), name="login"),
    path("accounts/logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("customer/", sales_views.customer_order, name="customer_order"),
    path("customer/order/<int:pk>/", sales_views.customer_order_success, name="customer_order_success"),
    path("", include("dashboard.urls")),
    path("products/", include("products.urls")),
    path("stock/", include("stock.urls")),
    path("sales/", include("sales.urls")),
    path("reports/", include("reports.urls")),
    re_path(r"^media/(?P<path>.*)$", serve, {"document_root": settings.MEDIA_ROOT}),
]
