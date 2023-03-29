import dataclasses

import pytest
import typing

import ezperm


@dataclasses.dataclass
class Hero:
    name: str
    type: typing.Literal['mage', 'warrior']
    permissions: typing.List[ezperm.PermissionEnum]


@pytest.fixture
def hero() -> Hero:
    return Hero(name='Rocco', type='warrior', permissions=[])

