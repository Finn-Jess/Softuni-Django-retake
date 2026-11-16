from django import template

register = template.Library()


@register.filter(name='currency')
def currency(value):
    try:
        return f"€{float(value):.2f}/day"
    except (ValueError, TypeError):
        return "€0.00/day"


@register.simple_tag(takes_context=True)
def active_nav(context, url_name):
    request = context.get('request')
    if not request or not getattr(request, 'resolver_match', None):
        return ''
    current = f"{request.resolver_match.app_name}:{request.resolver_match.url_name}"
    return 'active fw-semibold' if current == url_name else ''