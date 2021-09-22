from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from ordermanager import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('ordermanager/', include('ordermanager.urls')),
    path('common/', include('common.urls')),
    path('', views.manage_index, name='index'),
]

# + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
