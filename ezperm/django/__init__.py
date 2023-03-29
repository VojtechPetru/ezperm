try:
    import django
except ModuleNotFoundError:
    raise ModuleNotFoundError(
        "Attempted import of `django` failed. Please specify `django` as an extra dependency of ezperm package.",
    )

from .models import *
