import dataclasses
import typing


class PermissionInterface:
    def _has_perm(self, obj: typing.Any, /) -> bool:
        """Check if the object has this permission. To be overriden in subclasses."""
        raise NotImplementedError

    def __call__(self, obj: typing.Any) -> bool:
        """Check if the object has this permission."""
        return self._has_perm(obj)

    def __or__(self, other: 'PermissionInterface') -> 'PermissionInterface':
        """
        Return a new permission that is a combination of this and other.
        This allows for the use of the | operator -> if one of the permissions is true, the whole expression is true.
        Example:
            permission_required = Perm1 | Perm2 | Perm3
        """
        @dataclasses.dataclass
        class OrPerm(PermissionInterface):
            perm1: 'PermissionInterface'
            perm2: 'PermissionInterface'

            def _has_perm(self, obj: typing.Any) -> bool:
                return self.perm1(obj) or self.perm2(obj)

        return OrPerm(self, other)

    def __and__(self, other: 'PermissionInterface') -> 'PermissionInterface':
        """
        Return a new permission that is a combination of this and other.
        This allows for the use of the & operator -> if both of the permissions are true, the whole expression is true.
        Example:
            permission_required = Perm1 & Perm2 & Perm3
        """
        @dataclasses.dataclass
        class AndPerm(PermissionInterface):
            perm1: 'PermissionInterface'
            perm2: 'PermissionInterface'

            def _has_perm(self, obj: typing.Any) -> bool:
                return self.perm1(obj) and self.perm2(obj)

        return AndPerm(self, other)

    def __invert__(self) -> 'PermissionInterface':
        """
        Return a new permission that is a negation of this permission.
        This allows for the use of the ~ operator -> if the permission is true, the whole expression is false.
        Example:
            permission_required = ~Perm1
        """
        @dataclasses.dataclass
        class NotPerm(PermissionInterface):
            perm: 'PermissionInterface'

            def _has_perm(self, obj: typing.Any) -> bool:
                return not self.perm(obj)

        return NotPerm(self)
