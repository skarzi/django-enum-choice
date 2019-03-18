from enum import _EnumDict

import pytest

from enum_choice import EnumChoice


@pytest.fixture(scope='module')
def testing_enum():
    class ChmodEnum(int, EnumChoice):
        READ = 4
        WRITE = 2
        EXECUTE = 1

    return ChmodEnum


class TestEnumChoiceMagicMethods:
    @pytest.mark.parametrize('other_value', [1.00, 1])
    def test_eq_returns_True_when_other_value_equals_to_member_value(
            self,
            testing_enum,
            other_value,
    ):
        assert testing_enum.EXECUTE == other_value

    @pytest.mark.parametrize('other_value', [1.0001, -1, '1', object()])
    def test_eq_returns_False_when_other_value_does_not_equal_to_member_value(
            self,
            testing_enum,
            other_value
    ):
        assert testing_enum.EXECUTE != other_value

    @pytest.mark.parametrize('other_value', [1.001, 11])
    def test_lt_returns_True_when_member_value_is_less_than_other_value(
            self,
            testing_enum,
            other_value,
    ):
        assert testing_enum.EXECUTE < other_value

    @pytest.mark.parametrize('other_value', [0.999, -1])
    def test_lt_returns_False_when_member_value_does_not_less_than_other_value(
            self,
            testing_enum,
            other_value,
    ):
        assert testing_enum.EXECUTE >= other_value

    def test_bool_returns_True_when_member_value_is_truthy(self):
        class TruthyEnum(EnumChoice):
            A = 1
            B = 'test'
            C = (1.1, 1)

        for member in TruthyEnum:
            assert bool(member) is True

    def test_bool_returns_False_when_member_value_is_falsy(self):
        class FalsyEnum(EnumChoice):
            A = 0
            B = ''
            C = False
            D = ((),)

        for member in FalsyEnum:
            assert bool(member) is False

    def test_str_returns_member_value_string_representation(self):
        class TestingEnum(EnumChoice):
            A = 47
            B = 'test'
            C = False
            D = (1, 2)
            E = 1.2

        for member in TestingEnum:
            assert str(member) == str(member.value)

    def test_hash_returns_member_value_hash(self):
        class TestingEnum(EnumChoice):
            A = 47
            B = 'test'
            C = False
            D = (1, 2)
            E = object()

        for member in TestingEnum:
            assert hash(member) == hash(member.value)


class TestEnumChoiceMemberInitialization:
    @pytest.mark.parametrize('member_type, members', [
        (int, {'R': 1, 'G': 2, 'B': 3}),
        (float, {'R': 0.9, 'G': 2.6, 'B': 3.14}),
        (str, {'R': 'red', 'G': 'green', 'B': 'blue'}),
        (type('TestingType', (object,), dict()), {'R': 1, 'G': 2, 'B': 3}),
    ])
    def test_enum_members_is_instance_of_member_base_class_returned_by_EnumMeta_get_mixin(
            self,
            member_type,
            members,
    ):
        def _enum_dict(mapping):
            enum_dict = _EnumDict()
            for key, value in mapping.items():
                enum_dict[key] = value
            return enum_dict

        enum_class = type(
            '{}Enum'.format(member_type.__name__),
            (member_type, EnumChoice),
            _enum_dict(members),
        )
        for member_name in members:
            assert isinstance(getattr(enum_class, member_name), member_type)

    def test_enum_members_type_is_object_when_any_other_type_injected(self):
        class TestingEnum(EnumChoice):
            TEST_ME = 'like you do'

        assert isinstance(TestingEnum.TEST_ME, object)

    def test_enum_member_label_text_is_set_to_second_args_element_if_its_passed(
            self,
    ):
        labels = ['First', '1', '7.4']

        class EnumWithChoiceTexts(EnumChoice):
            A = (1, 'First')
            B = (2, 1)
            C = (3, 7.4)

        for i, member in enumerate(EnumWithChoiceTexts):
            assert member.label == labels[i]

    def test_enum_member_label_text_has_default_value_when_second_args_element_missing(
            self,
    ):
        labels = ['Red', 'Dark Red', 'Super Dark Red']

        class EnumWhithoutChoiceTexts(EnumChoice):
            RED = 1
            DARK_RED = 2
            SUPER_DARK_RED = 3

        for i, member in enumerate(EnumWhithoutChoiceTexts):
            assert member.label == labels[i]


class TestEnumChoiceClassMethods:
    def test_get_returns_member_when_member_with_given_name_exist(
            self,
            testing_enum,
    ):
        assert testing_enum.get('READ') == testing_enum.READ
        assert testing_enum.get('WRITE') == testing_enum.WRITE
        assert testing_enum.get('EXECUTE') == testing_enum.EXECUTE

    @pytest.mark.parametrize('name', ['SUID', 'read', 'Write'])
    def test_get_returns_fallback_when_member_with_given_name_does_not_exist_and_fallback_passed(
            self,
            testing_enum,
            name,
    ):
        fallback = object()
        assert testing_enum.get(name, fallback) == fallback

    @pytest.mark.parametrize('name', ['SUID', 'read', 'Write'])
    def test_get_raises_AttributeError_when_member_with_given_name_does_not_exist_and_fallback_not_passed(
            self,
            testing_enum,
            name,
    ):
        with pytest.raises(AttributeError):
            testing_enum.get(name)

    def test_choices_returns_list_of_tuples_with_choice_value_and_text(self):
        class TestingEnum(EnumChoice):
            A = 1
            B = (2, 'bbbb')
            C = ('c', 'third letter')

        expected_choices = [(1, 'A'), (2, 'bbbb'), ('c', 'third letter')]
        assert TestingEnum.choices() == expected_choices
