from django.contrib import admin
from django.urls import path, include

# Registrando as rotas da app
urlpatterns = [
    path('api/v1/', include('customers.urls')),

    path('admin/', admin.site.urls),
]
