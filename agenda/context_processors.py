from django.conf import settings

def export_settings(request):
    return {
        'ENABLE_SILK': getattr(settings, 'ENABLE_SILK', False)
    }
