from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from rest_framework.authtoken import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("user/", include("user.urls")),
    path("anbar/", include("anbar.urls")),
    path("product/", include("product.urls")),
    path("all_data/", include("all_data.urls")),
    path("user_scince/", include("user_scince.urls")),
    path("production/", include("production.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


admin.site.site_header = "Himan Delbina (09183739816)"
