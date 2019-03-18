from enum_choice import EnumChoice


# `str`s members with default label
class YearInSchool(str, EnumChoice):
    FRESHMAN = 'FR'
    SOPHOMORE = 'SO'
    JUNIOR = 'JR'
    SENIOR = 'SR'


# `int`s members with custom labels
class Grade(int, EnumChoice):
    A = (5, 'Highest Grade')
    B = (4, 'Very strong pass')
    C = (3, 'Passed but with difficulties')
    D = (2, 'Borderline: not passed but was not far from passing')
    F = (0, 'Failed')


# `object`s members with default labels
class Gender(EnumChoice):
    UNSPECIFIED = ''
    MALE = 'M'
    FEMALE = 'F'
