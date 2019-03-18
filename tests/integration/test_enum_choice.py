import pytest

from . import (
    enums,
    models,
)


@pytest.mark.django_db
class TestDjangoIntegration:
    @pytest.mark.parametrize('year_in_school', list(enums.YearInSchool))
    @pytest.mark.parametrize('grade', list(enums.Grade))
    @pytest.mark.parametrize('gender', list(enums.Gender))
    def test_creating_model_instance_with_choices_field_when_passing_enum_member_instance(
            self,
            year_in_school,
            grade,
            gender,
    ):
        student = models.Student.objects.create(
            year_in_school=year_in_school,
            grade=grade,
            gender=gender,
        )
        assert student.id is not None
        student.refresh_from_db()
        assert student.year_in_school == year_in_school
        assert student.grade == grade
        assert student.gender == gender
