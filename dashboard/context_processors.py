def display_name(request):
    if not request.user.is_authenticated:
        return {"display_name": "Admin DM"}

    if request.user.username == "admin":
        return {"display_name": "Admin DM"}

    name = request.user.get_full_name() or request.user.username or "Admin DM"
    return {"display_name": name.title()}
