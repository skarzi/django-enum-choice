# pylint: disable=W0143
import enum
import typing

from functools import total_ordering

MemberValue = typing.TypeVar('MemberValue')
NOT_PASSED = object()


@total_ordering
class EnumChoice(enum.Enum):
    """Integrate Enum with Django fields's choices.

    Examples
    --------
    Instead of writing long code in Django models as suggested in docs::

        from django.db import models


        class Student(models.Model):
            FRESHMAN = 'FR'
            SOPHOMORE = 'SO'
            JUNIOR = 'JR'
            SENIOR = 'SR'
            YEAR_IN_SCHOOL_CHOICES = (
                (FRESHMAN, 'Freshman'),
                (SOPHOMORE, 'Sophomore'),
                (JUNIOR, 'Junior'),
                (SENIOR, 'Senior'),
            )
            year_in_school = models.CharField(
                max_length=2,
                choices=YEAR_IN_SCHOOL_CHOICES,
                default=FRESHMAN,
            )


    Simply create `EnumChoice` sublass with all choices::

        from django.db import models


        # enums.py

        class YearInSchool(str, EnumChoice):
            FRESHMAN = ('FR', 'Freshman')
            SOPHOMORE = ('SO', 'Sophomore')
            JUNIOR = ('JR', 'Junior')
            SENIOR = ('SR', 'Senior')


        # models.py

        class Student(models.Model):
            year_in_school = models.CharField(
                max_length=2,
                choices=YearInSchool.choices(),
                default=YearInSchool.FRESHMAN,
            )
    """
    @classmethod
    def get(cls, name: str, fallback: typing.Any = NOT_PASSED) -> typing.Any:
        """Get member by it's name.

        Raises
        ------
        AttributeError
            when member with given `name` does not exist
        """
        name = cls.process_name(name)
        member = cls.__members__.get(name, fallback)
        if member is NOT_PASSED:
            raise AttributeError(name)
        return member

    @classmethod
    def process_name(cls, name: str) -> str:
        """Process `name` to make it valid member name.
        """
        return name

    @classmethod
    def choices(cls) -> typing.Sequence[typing.Tuple[MemberValue, str]]:
        """Iterable to use as Django fields' `choices` argument.
        """
        return [(member.value, member.label) for member in cls]

    # enum member methods
    def __new__(
            cls,
            value: MemberValue,
            *args: typing.Any,
            **kwargs: typing.Any
    ) -> 'EnumChoice':
        """Return member intance for `value`.

        Member base type is obtained by using [`enum.EnumMeta._get_mixin_`]
        (https://github.com/python/cpython/blob/master/Lib/enum.py#L474).
        It's necessary to use member base type `__new__` method, if
        members have to be treated like it will be instances of type
        of its values.
        """
        enum_member_type, _ = cls._get_mixins_(cls.__bases__)
        if enum_member_type.__new__ == object.__new__:
            member = enum_member_type.__new__(cls)
        else:
            member = enum_member_type.__new__(cls, value)
        member._value_ = value  # pylint: disable=W0212
        return member

    def __init__(  # pylint: disable=W0613,W1113
            self,
            value: MemberValue,
            label: str = '',
            *args: typing.Any,  # typing.Tuple[typing.Tuple[str, typing.Any]]
            **kwargs: typing.Any
    ):
        """Initialize enum member.

        `_value_` is already set in `EnumChoice.__new__`.
        """
        self.label = self._get_label(label)

    def __eq__(self, other: typing.Any) -> bool:
        return self.value == other

    def __lt__(self, other: typing.Any) -> bool:
        return self.value < other

    def __int__(self):
        return int(self.value)

    def __bool__(self):
        return bool(self.value)

    def __str__(self):
        return str(self.value)

    def __hash__(self):
        return hash(self.value)

    def _get_label(self, label: str = '') -> str:
        # pylint: disable=E1101
        return str(label or self.name.replace('_', ' ').title())
