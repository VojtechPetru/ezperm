try:
    import django
except ModuleNotFoundError:
    raise ModuleNotFoundError("Can't use `ezperm.django` module without Django installed in your environment.")

from .models import *
