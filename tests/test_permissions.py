import typing

import ezperm
if typing.TYPE_CHECKING:
    from tests.conftest import Hero


class Permissions(ezperm.PermissionEnum):
    PERM1 = 'PERM1', 'Perm 1'
    PERM2 = 'PERM2', 'Perm 2'
    PERM3 = 'PERM3', 'Perm 3'
    PERM4 = 'PERM4', 'Perm 4'

    def _has_perm(self, obj: 'Hero') -> bool:
        return self.value in obj.permissions

    @ezperm.permission
    def is_mage(obj: 'Hero') -> bool:
        return obj.type == 'mage'

    @ezperm.permission
    def is_warrior(obj: 'Hero') -> bool:
        return obj.type == 'warrior'

    @ezperm.permission
    def perms_1_and_2_combination(obj: 'Hero') -> bool:
        return (Permissions.PERM1 & Permissions.PERM2)(obj)

    @classmethod
    def perms_combination_classmethod(cls) -> ezperm.PermissionInterface:
        return cls.PERM1 & cls.PERM2


def check(
        superhero: 'Hero',
        perm: ezperm.PermissionInterface,
        superhero_perms: typing.List[ezperm.PermissionEnum],
        should_have_perm: bool,
):
    """
    Check if the hero has expected permission.
    :param superhero: The hero to check.
    :param perm: The permission which we check whether superhero has.
    :param superhero_perms: The permissions superhero has.
    :param should_have_perm: Expected result - Whether the hero should have the permission.
    """
    superhero.permissions = [perm.value for perm in superhero_perms]
    assert perm(superhero) is should_have_perm


def test_single_success(hero):
    perm = Permissions.PERM1
    check(hero, perm, [perm], True)


def test_single_failure(hero):
    perm = Permissions.PERM1
    check(hero, perm, [], False)
    check(hero, perm, [Permissions.PERM2], False)


def test_multiple_must_have_all_success(hero):
    perm1, perm2, perm3 = Permissions.PERM1, Permissions.PERM2, Permissions.PERM3
    check(hero, perm1 & perm2 & perm3, [perm1, perm2, perm3], True)


def test_multiple_must_have_all_failure(hero):
    perm1, perm2, perm3 = Permissions.PERM1, Permissions.PERM2, Permissions.PERM3
    check(hero, perm1 & perm2 & perm3, [perm1, perm2], False)


def test_multiple_must_have_at_least_one_success(hero):
    perm1, perm2, perm3 = Permissions.PERM1, Permissions.PERM2, Permissions.PERM3
    check(hero, perm1 | perm2 | perm3, [perm1], True)
    check(hero, perm1 | perm2 | perm3, [perm1, perm2], True)


def test_multiple_must_have_at_least_one_failure(hero):
    perm1, perm2, perm3 = Permissions.PERM1, Permissions.PERM2, Permissions.PERM3
    check(hero, perm1 | perm2 | perm3, [], False)
    check(hero, perm1 | perm2 | perm3, [Permissions.PERM4], False)


def test_combination_success(hero):
    perm1, perm2, perm3 = Permissions.PERM1, Permissions.PERM2, Permissions.PERM3
    # both of these perms should be equivalent
    for perm in [perm1 | perm2 & perm3, perm1 | (perm2 & perm3)]:
        check(hero, perm, [perm1], True)
        check(hero, perm, [perm1, perm2], True)
        check(hero, perm, [perm2, perm3], True)
        check(hero, perm, [perm1, perm3], True)


def test_combination_failure(hero):
    perm1, perm2, perm3 = Permissions.PERM1, Permissions.PERM2, Permissions.PERM3
    # both of these perms should be equivalent
    for perm in [perm1 | perm2 & perm3, perm1 | (perm2 & perm3)]:
        check(hero, perm, [], False)
        check(hero, perm, [perm2], False)
        check(hero, perm, [perm3], False)


def test_complex_combination(hero):
    perm1, perm2, perm3, perm4 = Permissions.PERM1, Permissions.PERM2, Permissions.PERM3, Permissions.PERM4
    # both of these perms should be equivalent
    for perm in [perm1 | perm2 & perm3 | perm4, perm1 | (perm2 & perm3) | perm4]:
        # SUCCESS
        check(hero, perm, [perm1], True)
        check(hero, perm, [perm1, perm2], True)
        check(hero, perm, [perm2, perm3], True)
        check(hero, perm, [perm1, perm3], True)
        check(hero, perm, [perm4], True)
        check(hero, perm, [perm1, perm2, perm3, perm4], True)
        # FAILURE
        check(hero, perm, [], False)
        check(hero, perm, [perm2], False)
        check(hero, perm, [perm3], False)


def test_negation_single_success(hero):
    perm1, perm2 = Permissions.PERM1, Permissions.PERM2
    check(hero, ~perm1, [perm2], True)
    check(hero, ~perm1, [], True)
    check(hero, ~perm1, [], True)


def test_negation_single_failure(hero):
    perm1, perm2 = Permissions.PERM1, Permissions.PERM2
    check(hero, ~perm1, [perm1], False)
    check(hero, ~perm1, [perm1, perm2], False)


def test_simple_negation_with_and(hero):
    perm1, perm2, perm3 = Permissions.PERM1, Permissions.PERM2, Permissions.PERM3
    # must not have perm1 and must have perm2
    check(hero, ~perm1 & perm2, [perm2], True)
    check(hero, ~perm1 & perm2, [perm2, perm3], True)
    check(hero, ~perm1 & perm2, [], False)
    check(hero, ~perm1 & perm2, [perm3], False)
    check(hero, ~perm1 & perm2, [perm1], False)
    check(hero, ~perm1 & perm2, [perm1, perm2], False)

    # must not have perm1 and perm2 together
    check(hero, ~(perm1 & perm2), [], True)
    check(hero, ~(perm1 & perm2), [perm3], True)
    check(hero, ~(perm1 & perm2), [perm1], True)
    check(hero, ~(perm1 & perm2), [perm2], True)
    check(hero, ~(perm1 & perm2), [perm1, perm3], True)
    check(hero, ~(perm1 & perm2), [perm2, perm3], True)
    check(hero, ~(perm1 & perm2), [perm1, perm2], False)


def tet_simple_negation_with_or(superhero):
    perm1, perm2, perm3 = Permissions.PERM1, Permissions.PERM2, Permissions.PERM3
    # must not have perm1 or must have perm2
    check(superhero, ~perm1 | perm2, [perm3], True)  # evaluates to: True | False
    check(superhero, ~perm1 | perm2, [perm2], True)  # evaluates to: False | True
    check(superhero, ~perm1 | perm2, [perm1, perm2], True)  # evaluates to: False | True
    check(superhero, ~perm1 | perm2, [], True)  # evaluates to: True | False
    check(superhero, ~perm1 | perm2, [perm1], False)  # evaluates to: False | False
    check(superhero, ~perm1 | perm2, [perm1, perm3], False)  # evaluates to: False | False

    # must not have neither perm1 nor perm2
    check(superhero, ~(perm1 | perm2), [perm3], True)
    check(superhero, ~(perm1 | perm2), [], True)
    check(superhero, ~(perm1 | perm2), [perm1], False)
    check(superhero, ~(perm1 | perm2), [perm2], False)
    check(superhero, ~(perm1 | perm2), [perm1, perm2], False)
    check(superhero, ~(perm1 | perm2), [perm1, perm2, perm3], False)


def test_negation_complex(hero):
    perm1, perm2, perm3 = Permissions.PERM1, Permissions.PERM2, Permissions.PERM3
    # must not have perm1 or must have perm2
    check(hero, ~perm1 | perm2, [perm2], True)
    check(hero, ~perm1 | perm2, [perm1], False)

    # must not have neither perm1 nor perm2 and or must have perm3
    check(hero, ~(perm1 | perm2) | perm3, [perm1], False)  # evaluates to: False | False
    check(hero, ~(perm1 | perm2) | perm3, [perm2], False)  # evaluates to: False | False
    check(hero, ~(perm1 | perm2) | perm3, [perm3], True)  # evaluates to: True | True
    check(hero, ~(perm1 | perm2) | perm3, [perm1, perm3], True)  # evaluates to: False | True
    check(hero, ~(perm1 | perm2) | perm3, [], True)  # evaluates to: True | False


def test_permission_defined_as_a_combination_of_perms_via_classmethod(hero):
    perm1, perm2, perm3 = Permissions.PERM1, Permissions.PERM2, Permissions.PERM3
    check(hero, Permissions.perms_combination_classmethod(), [perm1, perm2], True)
    check(hero, Permissions.perms_combination_classmethod(), [perm1], False)
    check(hero, Permissions.perms_combination_classmethod(), [perm2], False)
    check(hero, Permissions.perms_combination_classmethod(), [perm3], False)
    check(hero, Permissions.perms_combination_classmethod(), [perm2, perm3], False)
    check(hero, Permissions.perms_combination_classmethod(), [], False)


def test_permission_decorator(hero):
    check(hero, Permissions.is_mage, [Permissions.PERM1], False)
    check(hero, Permissions.is_mage & Permissions.PERM1, [Permissions.PERM1], False)
    check(hero, Permissions.is_mage | Permissions.PERM1, [Permissions.PERM1], True)
    hero.type = 'mage'
    check(hero, Permissions.is_mage, [Permissions.PERM1], True)


def test_permission_decorator_permissions_combination(hero):
    check(hero, Permissions.perms_1_and_2_combination, [], False)
    check(hero, Permissions.perms_1_and_2_combination, [Permissions.PERM1], False)
    check(hero, Permissions.perms_1_and_2_combination, [Permissions.PERM2], False)
    check(hero, Permissions.perms_1_and_2_combination, [Permissions.PERM1, Permissions.PERM2], True)


def test_permission_decorator_does_not_break_other_perms(hero):
    # basic perm check
    check(hero, Permissions.PERM1, [Permissions.PERM1], True)
    check(hero, Permissions.PERM1, [Permissions.PERM2], False)

    # use decorated perms
    check(hero, Permissions.is_mage, [Permissions.PERM1], False)
    hero.type = 'mage'
    check(hero, Permissions.is_mage, [Permissions.PERM1], True)

    # basic perm check still works
    check(hero, Permissions.PERM1, [Permissions.PERM1], True)
    check(hero, Permissions.PERM1, [Permissions.PERM2], False)
