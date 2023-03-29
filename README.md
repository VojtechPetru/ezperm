# Easy permissions
Define user permissions and resource access simply and efficiently.

## Installation
```bash
pip install ezperm
```

## Usage & examples
### General case
Assume we are in charge of a superhero team. We have a list of heroes, and we want to define permissions for them.
Our hero model might look like this:
```python
import dataclasses


@dataclasses.dataclass
class Hero:
    name: str
    age: int
    permissions: list['Permissions']
```
After a while of working with our heroes, we realize that some of them are terrible cooks. We want to define a permission
that will allow only some of them to cook or bake. 

This can be done by extending the `PermissionEnum` class and defining a `_has_perm`
method that will check if the hero has the permission.
#### Permission enums
```python
import ezperm

class Permissions(ezperm.PermissionEnum):
    CAN_COOK = 'CAN_COOK'
    CAN_BAKE = 'CAN_BAKE'
    
    def _has_perm(self, hero: Hero) -> bool:
        return self.value in hero.permissions
```
Now lets use our permissions in the code:
```python
# Define some heroes
ironman = Hero('Ironman', 45, [Permissions.CAN_COOK, Permissions.CAN_BAKE])
deadpool = Hero('Deadpool', 30, [Permissions.CAN_BAKE])
hulk = Hero('Hulk', 55, [])

# Check if the hero has a permission
Permissions.CAN_COOK(ironman)  # ➞ True
Permissions.CAN_COOK(deadpool)  # ➞ False
Permissions.CAN_COOK(hulk)  # ➞ False
```
It is possible to use `&` _(logical and)_, `|` _(logical or)_ or `~` _(negation)_ operators to combine permissions:
```python
(Permissions.CAN_COOK & Permissions.CAN_BAKE)(ironman)  # ➞ True
(Permissions.CAN_COOK & Permissions.CAN_BAKE)(deadpool)  # ➞ False
(Permissions.CAN_COOK | Permissions.CAN_BAKE)(hulk)  # ➞ False
~(Permissions.CAN_COOK | Permissions.CAN_BAKE)(hulk)  # ➞ True
(~Permissions.CAN_COOK & Permissions.CAN_BAKE)(deadpool)  # ➞ True
```

#### Dynamic permissions
Using the `@permission` decorator, we can also define dynamic permissions that will check if the hero has a permission based on some other condition, or define a permission as a combination of other permissions.
```python
class Permissions(ezperm.PermissionEnum):
    CAN_COOK = 'CAN_COOK'
    CAN_BAKE = 'CAN_BAKE'
    
    def _has_perm(self, hero: Hero) -> bool:
        return self.value in hero.permissions
    
    ### ↓ NEW ↓ ###
    @ezperm.permission
    def is_worthy(hero: Hero) -> bool:
        return hero.name == 'Thor'
    
    @ezperm.permission
    def is_old(hero: Hero) -> bool:
        return hero.age > 50

    @ezperm.permission
    def can_use_oven(hero: Hero) -> bool:
        return (Permissions.CAN_COOK | Permissions.CAN_BAKE)(hero)
```
These permissions can be used in the same way as the static ones:
```python
Permissions.is_worthy(ironman)  # ➞ False
(Permissions.CAN_COOK | PERMISSIONS.is_worthy)(ironman)  # ➞ True
```


### Django integration
#### Installation
```bash
pip install ezperm[django]
```

ezperm comes with a couple of tools to help with Django integration. Its use is entirely optional, and you can use ezperm and Django without it.

First, lets update our `Permissions` and `Hero` classes in our example:
```python
import ezperm.django

from django.db import models
from django.contrib.postgres.fields import ArrayField


class Permissions(ezperm.PermissionEnum, models.TextChoices):
    ... # same as before


class Hero(ezperm.django.PermissionsMixin, models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    permissions = ArrayField(
        base_field=models.CharField(
            max_length=255,
            choices=Permissions.choices,
        ),
        default=list,
    )
```
Note, that we've inherited the `Permissions` from Django's `TextChoices` in order to use it as a `choices` argument for the `permissions` field.
Moreover, we've added the `PermissionsMixin` to our `Hero` model, which overrides the `has_perms` and `has_perm` method.

Now lets define a view which will allow access only to worthy or old heroes:
```python
from django.views.generic import View
from ezperm.django.views import PermissionRequiredMixin


class CookView(PermissionRequiredMixin, View):
    permission_required = Permissions.CAN_COOK | Permissions.is_worthy
    
    def get(self, request):
        return HttpResponse('You can cook!')
```


## Contributing
Pull requests for any improvements are welcome.

[Poetry](https://github.com/sdispater/poetry) is used to manage dependencies.
To get started follow these steps:

```shell
git clone https://github.com/VojtechPetru/ezperm.git
cd ezperm
poetry install
poetry run pytest
```

## Links
- Repository: https://github.com/VojtechPetru/ezperm
- Issue tracker: https://github.com/VojtechPetru/ezperm/issues. 
In case of sensitive bugs (e.g. security vulnerabilities) please contact me at _petru.vojtech@gmail.com_ directly.


