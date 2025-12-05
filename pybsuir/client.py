import asyncio
from typing import List, Union, Optional, Tuple, Dict

from pybsuir import Faculty, Speciality, Course, MarkedStudent
from pybsuir.types.types import RatedStudent, BsuirStudent
from pybsuir.utils.dict_utils import dict_to_dataclass
from pybsuir.utils.http_utils import get_json_response, TIMEOUT

BASE_URL = "https://iis.bsuir.by/api/v1"

class BsuirStatsClient:

    def __init__(self, timeout: int = TIMEOUT):
        self._timeout = timeout
        self._headers = {
            "accept": "application/json, text/plain, */*",
            "accept-encoding": "gzip",
            "accept-language": "ru,en-US;q=0.9,en;q=0.8,da;q=0.7",
            "cache-control": "no-cache, no-store, max-age=0, must-revalidate",
            "pragma": "no-cache",
            "sec-ch-ua": '"Chromium";v="140", "Not=A?Brand";v="24", "Opera";v="124"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36 OPR/124.0.0.0"
        }
        self._lite_headers = {"accept": "application/json"}

    async def get_students(
            self,
            speciality: Union[int, Speciality] = 20657,
            course: Union[int, Course] = 2
    ) -> List[RatedStudent]:
        speciality = speciality if isinstance(speciality, int) else speciality.id
        course = course if isinstance(course, int) else course.course

        params = {"sdef": speciality, "course": course}
        data = await get_json_response(
            url=f"{BASE_URL}/rating",
            headers=self._lite_headers,
            ok_status=200,
            timeout=self._timeout,
            params=params
        )
        return [dict_to_dataclass(item, RatedStudent) for item in data]


    async def get_rating(
            self,
            student_card_number: Union[int, RatedStudent]
    ) -> BsuirStudent:
        if isinstance(student_card_number, RatedStudent):
            student_card_number = student_card_number.studentCardNumber

        params = {"studentCardNumber": student_card_number}
        data = await get_json_response(
            url=f"{BASE_URL}/rating/studentRating",
            headers=self._headers,
            ok_status=200,
            timeout=self._timeout,
            params=params
        )
        student = dict_to_dataclass(data, BsuirStudent)
        student.studentCardNumber = student_card_number
        return student


    async def get_faculties(self) -> List[Faculty]:
        data = await get_json_response(
            url=f"{BASE_URL}/schedule/faculties",
            headers=self._headers,
            ok_status=200,
            timeout=self._timeout
        )

        return [dict_to_dataclass(item, Faculty) for item in data]

    async def get_specialities(self, faculty: Union[Faculty, int]) -> List[Speciality]:
        if isinstance(faculty, Faculty):
            faculty = faculty.id

        data = await get_json_response(
            url=f"{BASE_URL}/rating/specialities?facultyId={faculty}",
            headers=self._headers,
            ok_status=200,
            timeout=self._timeout
        )

        return [dict_to_dataclass(item, Speciality) for item in data]

    async def get_courses(
            self,
            faculty: Union[Faculty, int],
            speciality: Union[Speciality, int]
    ) -> List[Course]:
        if isinstance(faculty, Faculty):
            faculty = faculty.id
        if isinstance(speciality, Speciality):
            speciality = speciality.id

        data = await get_json_response(
            url=f"{BASE_URL}/rating/courses?facultyId={faculty}&specialityId={speciality}",
            headers=self._headers,
            ok_status=200,
            timeout=self._timeout
        )

        return [dict_to_dataclass(item, Course) for item in data]

    async def get_top_students(
            self,
            speciality: Union[Speciality, int],
            course: Union[Course, int],
            lesson_name_abbrev: str,
            lesson_type_abbrev: Optional[str] = None,
            student_number_prefix: Optional[str] = None
    ) -> List[MarkedStudent]:

        students: List[RatedStudent] = await self.get_students(speciality, course)
        tasks = []

        for student in students:
            if student_number_prefix is None or str(student.studentCardNumber).startswith(student_number_prefix):
                tasks.append(self.get_rating(student))

        students: List[BsuirStudent] = await asyncio.gather(*tasks)

        marks: Dict[int, List[int]] = {}
        for student in students:
            marks[student.studentCardNumber] = []
            for lesson in student.lessons:
                if lesson.lessonNameAbbrev == lesson_name_abbrev:
                    if lesson_type_abbrev is None or lesson.lessonTypeAbbrev == lesson_type_abbrev:
                        for mark in lesson.marks:
                            marks[student.studentCardNumber].append(mark)

        sorted_students: List[Tuple[int, List[int]]] = sorted(
            marks.items(),
            key=lambda item: sum(item[1]) / len(item[1]) if item[1] else 0,
            reverse=True
        )
        return [MarkedStudent(student_number, st_marks) for (student_number, st_marks) in sorted_students]
