from django.urls import path
from . import views

app_name = 'equipment'

urlpatterns = [
    path('', views.GearListView.as_view(), name='gear_list'),
    path('create/', views.GearCreateView.as_view(), name='gear_create'),
    path('<int:pk>/', views.GearDetailView.as_view(), name='gear_detail'),
    path('<int:pk>/edit/', views.GearUpdateView.as_view(), name='gear_edit'),
    path('<int:pk>/delete/', views.GearDeleteView.as_view(), name='gear_delete'),
    path('categories/', views.CategoryListView.as_view(), name='category_list'),
    path('categories/create/', views.CategoryCreateView.as_view(), name='category_create'),
]