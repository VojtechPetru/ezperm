import typing

import ezperm
import django.contrib.auth.mixins


class PermissionRequiredMixin(django.contrib.auth.mixins.PermissionRequiredMixin):
    """Django's view PermissionRequiredMixin with support for ezperm permissions."""

    permission_required: typing.Optional[ezperm.PermissionInterface] = NotImplemented

    def get_permission_required(self) -> typing.Optional[ezperm.PermissionInterface]:
        if self.permission_required is NotImplemented:
            raise ValueError(
                f"`{self.__class__.__name__}` is missing a permission."
                f"Define {self.__class__.__name__}.permission_required, or override"
                f" {self.__class__.__name__}.get_permission_required() method."
            )
        if self.permission_required is None:
            return

        # Handle common errors
        if isinstance(self.permission_required, (tuple, list, set)):
            raise ValueError(
                f"Multiple permissions specified in `{self.__class__.__name__}` view."
                f" Please use & and | operators to combine them into single one."
            )
        if not isinstance(self.permission_required, ezperm.PermissionInterface):
            raise ValueError(
                f"Permission specified in `{self.__class__.__name__}` view is not "
                f"a `{ezperm.PermissionInterface.__name__}` instance."
            )
        return self.permission_required
