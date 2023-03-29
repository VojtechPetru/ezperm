import typing
import ezperm

if typing.TYPE_CHECKING:
    from django.contrib.auth.models import AbstractUser


# TODO write tests for these


DjangoAdminSitePerms = typing.Union[list[str], str]  # permission types used by the Django admin site


class PermissionsMixin:
    """Django's PermissionsMixin with support for ezperm permissions and admin-compliant permissions."""

    def has_perm(
            self: 'AbstractUser',
            perm: typing.Union[ezperm.PermissionInterface, DjangoAdminSitePerms],
            obj=None,
    ) -> bool:
        """Check if the user has the permission."""
        if not isinstance(perm, ezperm.PermissionInterface):  # handle default Django perms (used in admin)
            return super().has_perm(perm, obj=obj)
        return self.has_perms(perm)

    def has_perms(
            self: 'AbstractUser',
            perms: typing.Optional[typing.Union[ezperm.PermissionInterface, DjangoAdminSitePerms]],
            obj=None,
    ) -> bool:
        """Check if the user has the permission."""
        if not self.is_active:
            return False
        if perms is None:
            return True

        # handle default Django perms (used in admin)
        if not isinstance(perms, ezperm.PermissionInterface):
            if type(perms) is str:
                perms = [perms]
            return super().has_perms(perms, obj=obj)

        if self.is_superuser:
            return True
        return perms(self)
