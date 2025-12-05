from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List

from pybsuir.interafces import IPrintable


@dataclass(repr=False, frozen=True)
class Lesson(IPrintable):
    id: int
    dateString: datetime
    gradeBookOmissions: int
    isRespectfulOmission: bool
    lessonTypeId: int
    lessonTypeAbbrev: str
    lessonNameAbbrev: str
    subGroup: int
    marks: List[int]
    controlPoint: str

@dataclass(repr=False, frozen=True)
class MarkedStudent(IPrintable):
    student_card_number: int
    marks: List[int]

@dataclass(repr=False)
class BsuirStudent(IPrintable):
    id: int
    fio: str
    subGroup: int
    subGroupStudent: int
    lessons: List[Lesson]
    studentCardNumber: int = None


@dataclass(repr=False, frozen=True)
class StudentPeriod(IPrintable):
    average: float
    hours: int

@dataclass(repr=False, frozen=True)
class RatedStudent(IPrintable):
    studentCardNumber: str
    average: float
    hours: int
    averageShift: float
    first: Optional[StudentPeriod] = None
    second: Optional[StudentPeriod] = None
    third: Optional[StudentPeriod] = None

