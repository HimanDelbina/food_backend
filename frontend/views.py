from django.shortcuts import render, redirect
from django.contrib import messages
from user.models import *


def home(request):
    return render(request, "frontend/index.html")  # مسیر درست


def login_view(request):
    if request.method == "POST":
        person_code = request.POST.get("code")
        password = request.POST.get("password")

        try:
            user = PersonelModel.objects.get(person_code=person_code, password=password)
            if user.is_active:
                # ذخیره اطلاعات لاگین در session
                request.session["person_id"] = user.id
                request.session["person_name"] = f"{user.first_name} {user.last_name}"
                return redirect("/dashboard/")  # صفحه بعد از لاگین
            else:
                messages.error(request, "حساب کاربری شما غیرفعال است.")
        except PersonelModel.DoesNotExist:
            messages.error(request, "کد پرسنلی یا رمز عبور اشتباه است.")

    return render(request, "frontend/login.html")


def dashboard_view(request):
    if 'person_id' not in request.session:
        return redirect('/')
    name = request.session.get('person_name', 'کاربر')
    return render(request, 'frontend/dashboard.html', {'name': name})
