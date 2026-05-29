from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .services import calculate_dashboard_metrics


def home(request):
    return render(request, "dashboard/home.html")


@login_required
def dashboard(request):
    context = calculate_dashboard_metrics()
    context["can_view_profit"] = request.user.is_superuser or request.user.groups.filter(name__in=["Owner", "Manager"]).exists()
    return render(request, "dashboard/dashboard.html", context)
