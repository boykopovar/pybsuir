# 📦 Типы данных в pybsuir

Все данные приходят в виде датаклассов. Их удобно использовать и выводить в консоль.

---

## 1. 🏫 Faculty
- `id: int`
- `text: str`

## 2. 🎓 Speciality
- `id: int`
- `text: str`

## 3. 📘 Course
- `course: int`
- `hasForeignPlan: bool`

## 4. 📝 Lesson
- `id: int`
- `dateString: datetime`
- `gradeBookOmissions: int`
- `isRespectfulOmission: bool`
- `lessonTypeId: int`
- `lessonTypeAbbrev: str`
- `lessonNameAbbrev: str`
- `subGroup: int`
- `marks: List[int]`
- `controlPoint: str`

## 5. 👨‍🎓 MarkedStudent
- `student_card_number: int`
- `marks: List[int]`

## 6. 👤 BsuirStudent
- `id: int`
- `fio: str` - обычно строка пуста или состоит из пробельных символов
- `subGroup: int`
- `subGroupStudent: int`
- `lessons: List[Lesson]`
- `studentCardNumber: int`

## 7. 📊 StudentPeriod
- `average: float`
- `hours: int`

## 8. 🏅 RatedStudent
- `studentCardNumber: str`
- `average: float`
- `hours: int`
- `averageShift: float`
- `first: Optional[StudentPeriod]`
- `second: Optional[StudentPeriod]`
- `third: Optional[StudentPeriod]`
