
from .views import cartCount, categoryDropdown


def cartCountVariable(request):
    return {
        'cartCount': cartCount(request)
    }

def categoryDropdownMenu(request):
    return {
        'categoryDropdown': categoryDropdown(request)
    }