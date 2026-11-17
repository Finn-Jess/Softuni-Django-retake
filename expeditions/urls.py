from django.urls import path
from . import views

app_name = 'expeditions'

urlpatterns = [
    path('', views.ExpeditionListView.as_view(), name='expedition_list'),
    path('create/', views.ExpeditionCreateView.as_view(), name='expedition_create'),
    path('<int:pk>/', views.ExpeditionDetailView.as_view(), name='expedition_detail'),
    path('<int:pk>/edit/', views.ExpeditionUpdateView.as_view(), name='expedition_edit'),
    path('<int:pk>/delete/', views.ExpeditionDeleteView.as_view(), name='expedition_delete'),
]