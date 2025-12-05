from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List

from pybsuir.interafces import IPrintable

@dataclass(repr=False, frozen=True)
class Grouping(IPrintable):
    id: int
    text: str

@dataclass(repr=False, frozen=True)
class Faculty(Grouping):
    pass

@dataclass(repr=False, frozen=True)
class Speciality(Grouping):
    pass

@dataclass(repr=False, frozen=True)
class Course(IPrintable):
    course: int
    hasForeignPlan: bool
