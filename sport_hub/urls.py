from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('sport_app.urls')),
    path('users/', include('users_app.urls')),  # Лучше использовать 'users/' вместо 'users_app/'
]

# Добавляем обработку медиафайлов только в режиме разработки
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)