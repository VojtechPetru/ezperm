import typing
from .interfaces import PermissionInterface


def permission(func: typing.Callable[[typing.Any], bool]) -> 'PermissionInterface':
    """
    Decorator to create a PermissionInterface from a method/function.

    Example:
        class Permissions(ezperm.PermissionEnum):
            PERM1 = 'PERM1', 'Perm 1'
            PERM2 = 'PERM2', 'Perm 2'
            ...

            # ↓ HERE ↓ #
            @ezperm.permission
            def is_mage(obj: 'Hero') -> bool:
                return obj.type == 'mage'

    """
    class PermWrap(PermissionInterface):
        def _has_perm(self, obj: typing.Any) -> bool:
            return func(obj)
    return typing.cast(PermissionInterface, staticmethod(PermWrap()))
