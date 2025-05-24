from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.permissions import AllowAny
from .models import *
from .serializers import *
from django.dispatch import receiver
from django.db.models.signals import post_save
from rest_framework.decorators import permission_classes, api_view, throttle_classes
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import CityModel
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


@api_view(["POST"])
@permission_classes([AllowAny])
def create_tolid(request):
    s_data = request.data
    data_serializers = TolidSerializers(data=s_data)
    if data_serializers.is_valid():
        data_serializers.save()
        return Response(data_serializers.data, status=status.HTTP_201_CREATED)
    return Response(data_serializers.errors, status=status.HTTP_400_BAD_REQUEST)
