from django.urls import path, include

urlpatterns = [
    path('', include('core.urls')),
    path('equipment/', include('equipment.urls')),
    path('expeditions/', include('expeditions.urls')),
]

handler404 = 'core.views.custom_404_view'