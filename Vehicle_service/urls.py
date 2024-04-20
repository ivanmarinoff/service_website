"""
vehicle
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .admin_user import views
from .admin_user.views import LogoutUserView

# from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home_view, name='home'),
    path('', include('Vehicle_service.mechanic.urls')),
    path('', include('Vehicle_service.customer.urls')),
    path('', include('Vehicle_service.admin_user.urls')),
    path('afterlogin', views.afterlogin_view, name='afterlogin'),
    path('logout', LogoutUserView.as_view(template_name='vehicle/index.html'), name='logout'),
    path('aboutus', views.aboutus_view),
    path('contactus', views.contactus_view),
    path('schema/', include('schema_viewer.urls')),
]

if settings.DEBUG:
    from django.conf.urls.static import static

    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
