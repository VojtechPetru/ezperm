import enum
import typing

from . import interfaces


class PermissionEnum(interfaces.PermissionInterface, enum.Enum):
    def _has_perm(self, obj: typing.Any) -> bool:
        """Check if the object has this permission."""
        raise NotImplementedError
