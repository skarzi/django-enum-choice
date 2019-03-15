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

        class DjangoModel(models.Model):
            COLOR_R = 1
            COLOR_G = 2
            COLOR_B = 3
            COLOR_CHOICES = (
                (COLOR_R, 'Red'),
                (COLOR_G, 'Green'),
                (COLOR_B, 'Blue'),
            )

            color = models.PositiveSmallIntegerField(
                choices=COLOR_CHOICES,
            )


    Simply subclass `EnumChoice`::

        # enums.py

        class Color(int, EnumChoice):
            R = (1, 'Red')
            G = (2, 'Green')
            B = (3, 'Blue')


        # models.py

        class DjangoModel(models.Model):
            color = models.PositiveSmallIntegerField(
                choices=enums.Color.choices(),
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
        return [(member.value, member.choice_text) for member in cls]

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
        print(
            '{}.__new__({}, {}, {})'.format(cls.__name__, value, args, kwargs),
        )
        # TODO: obtain this type from value in metaclass
        # for intance iterate over all declared members and get one common type
        enum_member_type, _ = cls._get_mixins_(cls.__bases__)
        if enum_member_type.__new__ == object.__new__:
            member = enum_member_type.__new__(cls)
        else:
            member = enum_member_type.__new__(cls, value)
        member._value_ = value  # pylint: disable=W0212
        return member

    def __init__(  # pylint: disable=W0613,W1113
            self,
            value: MemberValue,  # `_value_` is set in `__new__`
            choice_text: str = '',
            *args: typing.Any,  # typing.Tuple[typing.Tuple[str, typing.Any]]
            **kwargs: typing.Any
    ):
        self.choice_text = self._get_choice_text(choice_text)
        # TODO: consider adding this feature
        # for attr_name, attr_value in args:
        #     setattr(self, attr_name, attr_value)

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

    def _get_choice_text(self, choice_text: str = '') -> str:
        # pylint: disable=E1101
        return str(choice_text or self._name_.replace('_', ' ').title())
