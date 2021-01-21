
from .views import cartCount


def cartCountVariable(request):
    return {
        'cartCount': cartCount(request)
    }