from django.db.models import Count, Sum
from django.shortcuts import render

from equipment.models import Category, GearItem
from expeditions.models import Expedition


def home_view(request):
    total_gear = GearItem.objects.count()
    available_gear = GearItem.objects.filter(is_available=True).count()
    total_categories = Category.objects.count()
    active_expeditions = Expedition.objects.count()
    total_daily_value = (
        GearItem.objects.aggregate(total=Sum('daily_rate'))['total'] or 0
    )

    featured_gear = GearItem.objects.select_related('category').order_by('-created_at')[:4]
    upcoming_expeditions = (
        Expedition.objects.annotate(gear_count=Count('assigned_gear'))
        .order_by('start_date')[:3]
    )

    context = {
        'total_gear': total_gear,
        'available_gear': available_gear,
        'total_categories': total_categories,
        'active_expeditions': active_expeditions,
        'total_daily_value': total_daily_value,
        'featured_gear': featured_gear,
        'upcoming_expeditions': upcoming_expeditions,
    }
    return render(request, 'core/home.html', context)


def about_view(request):
    return render(request, 'core/about.html')


def custom_404_view(request, exception=None):
    return render(request, '404.html', status=404)