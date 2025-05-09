from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.permissions import AllowAny
from user.models import *
from user.serializers import *
from django.dispatch import receiver
from django.db.models.signals import post_save
from rest_framework.decorators import permission_classes, api_view, throttle_classes
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
import pandas as pd
import os
import logging
from django.db.models import Q, Count
from django.contrib.auth.hashers import make_password, check_password
from django.shortcuts import get_object_or_404
from django.db import transaction
from django.views.decorators.cache import cache_page
from rest_framework.throttling import UserRateThrottle
from datetime import datetime
import io
import openpyxl
from collections import Counter
import jdatetime


# class AgeDistributionView(APIView):
#     def get(self, request, *args, **kwargs):
#         # محاسبه سن پرسنل‌ها
#         today = datetime.today()
#         age_groups = {}

#         for person in PersonelModel.objects.all():
#             if person.birthday:
#                 # تبدیل تاریخ تولد از jdatetime.date به رشته شمسی
#                 birthday_jalali_str = person.birthday.strftime("%Y-%m-%d")
#                 # تبدیل تاریخ شمسی به jdatetime.date
#                 birthday_jalali = jdatetime.datetime.strptime(
#                     birthday_jalali_str, "%Y-%m-%d"
#                 ).date()
#                 # تبدیل تاریخ شمسی به میلادی
#                 birthday_gregorian = birthday_jalali.togregorian()

#                 # محاسبه سن
#                 age = today.year - birthday_gregorian.year
#                 if today.month < birthday_gregorian.month or (
#                     today.month == birthday_gregorian.month
#                     and today.day < birthday_gregorian.day
#                 ):
#                     age -= 1

#                 # تقسیم‌بندی سنی به هر ۵ سال
#                 start_age = (age // 5) * 5
#                 end_age = start_age + 4
#                 age_range = f"{start_age}-{end_age}"

#                 if age_range not in age_groups:
#                     age_groups[age_range] = 0
#                 age_groups[age_range] += 1

#         return Response(age_groups)


# تعریف مقادیر تحصیلی به صورت دیکشنری
EDUCATION_DICT = {
    "DE": "ابتدایی",
    "DR": "راهنمایی",
    "DS": "سیکل",
    "DD": "دبیرستان",
    "DI": "دیپلم",
    "FD": "کاردانی",
    "LI": "کارشناسی",
    "FL": "کارشناسی ارشد",
    "PD": "دکترا",
    "DA": "دانشجو",
}


class PersonelAnalysisView(APIView):
    def get(self, request, *args, **kwargs):
        # تحلیل سن
        today = datetime.today()
        age_groups = {}
        age_scores = {}  # برای تحلیل نمره‌دهی رده سنی
        total_age = 0  # جمع سن‌ها
        total_people = 0  # تعداد افراد

        for person in PersonelModel.objects.all():
            if person.birthday:
                birthday_jalali_str = person.birthday.strftime("%Y-%m-%d")
                birthday_jalali = jdatetime.datetime.strptime(
                    birthday_jalali_str, "%Y-%m-%d"
                ).date()
                birthday_gregorian = birthday_jalali.togregorian()

                age = today.year - birthday_gregorian.year
                if today.month < birthday_gregorian.month or (
                    today.month == birthday_gregorian.month
                    and today.day < birthday_gregorian.day
                ):
                    age -= 1

                start_age = (age // 5) * 5
                end_age = start_age + 4
                age_range = f"{start_age}-{end_age}"

                if age_range not in age_groups:
                    age_groups[age_range] = 0
                age_groups[age_range] += 1

                # تحلیل نمره‌دهی رده سنی
                if 20 <= age <= 24:
                    age_score = 1
                elif 25 <= age <= 29:
                    age_score = 2
                elif 30 <= age <= 34:
                    age_score = 3
                elif 35 <= age <= 39:
                    age_score = 4
                else:
                    age_score = 5

                if age_range not in age_scores:
                    age_scores[age_range] = {"total_score": 0, "total_people": 0}
                age_scores[age_range]["total_score"] += age_score
                age_scores[age_range]["total_people"] += 1

                # جمع سن‌ها برای محاسبه میانگین سنی
                total_age += age
                total_people += 1

        # تحلیل وضعیت تأهل
        marital_status = {"married": 0, "single": 0}
        for person in PersonelModel.objects.all():
            if person.is_marid:
                marital_status["married"] += 1
            else:
                marital_status["single"] += 1

        # تحلیل تحصیلات
        education_distribution = {}
        total_score = 0
        total_people_education = 0
        for person in PersonelModel.objects.all():
            education = person.education
            if education:
                # تبدیل کد تحصیلی به نام فارسی
                education_name = EDUCATION_DICT.get(education, "نامشخص")
                if education_name in education_distribution:
                    education_distribution[education_name] += 1
                else:
                    education_distribution[education_name] = 1

                # محاسبه مجموع نمرات تحصیلات
                education_levels = {
                    "DE": 1,  # ابتدایی
                    "DR": 1,  # راهنمایی
                    "DS": 2,  # سیکل
                    "DD": 2,  # دبیرستان
                    "DI": 3,  # دیپلم
                    "FD": 3,  # کاردانی
                    "LI": 4,  # کارشناسی
                    "FL": 5,  # کارشناسی ارشد
                    "PD": 6,  # دکترا
                    "DA": 2,  # دانشجو
                }

                if education in education_levels:
                    total_score += education_levels[education]
                    total_people_education += 1

        # تحلیل سطح سواد
        if total_people_education > 0:
            average_education_level = total_score / total_people_education
        else:
            average_education_level = 0

        # تحلیل سواد
        if average_education_level <= 2:
            education_level_analysis = "سواد پایین"
        elif average_education_level <= 3:
            education_level_analysis = "سواد متوسط"
        elif average_education_level <= 4:
            education_level_analysis = "سواد خوب"
        elif average_education_level <= 5:
            education_level_analysis = "سواد عالی"
        else:
            education_level_analysis = "سواد بسیار عالی"

        # تحلیل تعداد فرزندان
        child_distribution = {
            "total_children": 0,
            "boy_children": 0,
            "girl_children": 0,
        }
        child_impact_analysis = {"positive_impact": 0, "negative_impact": 0}
        high_child_count_threshold = (
            3  # فرض می‌کنیم که اگر تعداد بچه‌ها بیشتر از 3 باشد، اثر منفی دارد
        )

        good_individuals = []
        bad_individuals = []
        total_good = 0
        total_bad = 0

        for person in PersonelModel.objects.all():
            child_distribution["total_children"] += person.child_count
            child_distribution["boy_children"] += person.boy_child_count
            child_distribution["girl_children"] += person.girl_child_count

            # تحلیل وضعیت اثر تعداد بچه‌ها
            if person.child_count > high_child_count_threshold:
                child_impact_analysis["negative_impact"] += 1
                bad_individuals.append(person)  # فرد با تعداد بچه زیاد
                total_bad += 1
            elif person.child_count > 0:
                child_impact_analysis["positive_impact"] += 1
                good_individuals.append(person)  # فرد با تعداد بچه کم یا متوسط
                total_good += 1

        # تحلیل وضعیت شغلی
        job_distribution = {}
        for person in PersonelModel.objects.all():
            job_position = person.work_type
            if job_position:
                if job_position.name in job_distribution:
                    job_distribution[job_position.name] += 1
                else:
                    job_distribution[job_position.name] = 1

        # محاسبه میانگین سنی
        if total_people > 0:
            average_age = total_age / total_people
        else:
            average_age = 0

        # تحلیل میانگین سنی
        if average_age < 30:
            age_analysis = "میانگین سنی پایین است"
        elif 30 <= average_age <= 40:
            age_analysis = "میانگین سنی مناسب است"
        else:
            age_analysis = "میانگین سنی بالا است"

        # محاسبه میانگین نمره‌دهی رده سنی
        age_group_analysis = {}
        for age_range, values in age_scores.items():
            if values["total_people"] > 0:
                average_age_score = values["total_score"] / values["total_people"]
                if average_age_score <= 2:
                    age_group_analysis[age_range] = "گروه سنی با وضعیت متوسط"
                elif average_age_score <= 3:
                    age_group_analysis[age_range] = "گروه سنی با وضعیت خوب"
                elif average_age_score <= 4:
                    age_group_analysis[age_range] = "گروه سنی با وضعیت عالی"
                else:
                    age_group_analysis[age_range] = "گروه سنی با وضعیت بسیار عالی"

        # تحلیل کلی شرایط فرزندی برای شرکت
        if total_bad > total_good:
            company_child_condition = "شرایط فرزندی برای شرکت بد است"
        else:
            company_child_condition = "شرایط فرزندی برای شرکت خوب است"

        # جمع‌بندی تمام تحلیل‌ها
        analysis_results = {
            "age_distribution": age_groups,
            "age_group_analysis": age_group_analysis,  # اضافه کردن تحلیل رده سنی
            "age_analysis": age_analysis,  # اضافه کردن تحلیل میانگین سنی
            "marital_status": marital_status,
            "education_distribution": education_distribution,
            "education_level_analysis": education_level_analysis,
            "child_distribution": child_distribution,
            "child_impact_analysis": child_impact_analysis,  # اضافه کردن تحلیل تاثیر بچه‌ها
            "company_child_condition": company_child_condition,  # تحلیل شرایط فرزندی کلی
            "good_individuals": [
                {
                    "first_name": person.first_name,
                    "last_name": person.last_name,
                    "person_code": person.person_code,
                }
                for person in good_individuals
            ],
            "bad_individuals": [
                {
                    "first_name": person.first_name,
                    "last_name": person.last_name,
                    "person_code": person.person_code,
                }
                for person in bad_individuals
            ],
            "job_distribution": job_distribution,
        }

        return Response(analysis_results)
