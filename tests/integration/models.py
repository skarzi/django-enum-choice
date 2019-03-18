from django.db import models

from . import enums


class Student(models.Model):
    year_in_school = models.CharField(
        max_length=2,
        choices=enums.YearInSchool.choices(),
        default=enums.YearInSchool.FRESHMAN,
    )
    grade = models.SmallIntegerField(
        choices=enums.Grade.choices(),
        default=enums.Grade.C
    )
    gender = models.CharField(
        max_length=1,
        choices=enums.Gender.choices(),
        blank=True,
    )

    class Meta:
        app_label = 'integration'
