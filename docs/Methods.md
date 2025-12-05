# 📝 Методы BsuirStatsClient

## 1. 🏫 `get_faculties`

Получение списка факультетов БГУИР.

- 🔧 **Параметры**: нет.
- 📤 **Возвращает**: `List[Faculty]` — список факультетов.
- ⚠️ **Исключения**: `BsuirStatsException`.

**Пример**:

```python
import asyncio
from pybsuir import BsuirStatsClient

async def main():
    client = BsuirStatsClient()
    faculties = await client.get_faculties()
    print(faculties)

asyncio.run(main())
````

---

## 2. 🏷️ `get_specialities`

Получение списка специальностей по факультету.

* 🔧 **Параметры**:

  * `faculty: Union[Faculty, int]` — объект факультета или его ID.
* 📤 **Возвращает**: `List[Speciality]` — список специальностей.
* ⚠️ **Исключения**: `BsuirStatsException`.

**Пример**:

```python
import asyncio
from pybsuir import BsuirStatsClient

async def main():
    client = BsuirStatsClient()
    specialities = await client.get_specialities(faculty=1)
    print(specialities)

asyncio.run(main())
```

---

## 3. 📚 `get_courses`

Получение списка курсов по факультету и специальности.

* 🔧 **Параметры**:

  * `faculty: Union[Faculty, int]`
  * `speciality: Union[Speciality, int]`
* 📤 **Возвращает**: `List[Course]` — список курсов.
* ⚠️ **Исключения**: `BsuirStatsException`.

**Пример**:

```python
import asyncio
from pybsuir import BsuirStatsClient

async def main():
    client = BsuirStatsClient()
    courses = await client.get_courses(faculty=1, speciality=20657)
    print(courses)

asyncio.run(main())
```

---

## 4. 👨‍🎓 `get_students`

Получение списка студентов по специальности и курсу.

* 🔧 **Параметры**:

  * `speciality: Union[int, Speciality] = 20657` — ID специальности или объект `Speciality`.
  * `course: Union[int, Course] = 2` — номер курса или объект `Course`.
* 📤 **Возвращает**: `List[RatedStudent]` — список студентов с рейтингами.
* ⚠️ **Исключения**: `BsuirStatsException`.

**Пример**:

```python
import asyncio
from pybsuir import BsuirStatsClient

async def main():
    client = BsuirStatsClient()
    students = await client.get_students(speciality=20657, course=2)
    print(students)

asyncio.run(main())
```

---

## 5. 📊 `get_rating`

Получение детального рейтинга конкретного студента.

* 🔧 **Параметры**:

  * `student_card_number: Union[int, RatedStudent]` — ID студента или объект `RatedStudent`.
* 📤 **Возвращает**: `BsuirStudent`.
* ⚠️ **Исключения**: `BsuirStatsException`.

**Пример**:

```python
import asyncio
from pybsuir import BsuirStatsClient

async def main():
    client = BsuirStatsClient()
    student = await client.get_rating(123456)
    print(student)

asyncio.run(main())
```

---

## 6. 🏆 `get_top_students`

Получение таблицы лидеров по конкретной дисциплине.

> ⚡ **Примечание**: Этот метод является абстракцией. Он вызывает внутренне методы `get_students` и `get_rating` для формирования полной таблицы рейтинга студентов по заданной дисциплине.

* 🔧 **Параметры**:

  * `speciality: Union[Speciality, int]`
  * `course: Union[Course, int]`
  * `lesson_name_abbrev: str` — аббревиатура дисциплины для фильтрации.
  * `lesson_type_abbrev: Optional[str]` — аббревиатура типа занятия (опционально).
  * `student_number_prefix: Optional[str]` — фильтр по началу номера студенческого билета (опционально).
* 📤 **Возвращает**: `List[MarkedStudent]` — топ студентов по выбранной дисциплине.
* ⚠️ **Исключения**: `BsuirStatsException`.

**Пример**:

```python
import asyncio
from pybsuir import BsuirStatsClient

async def main():
    client = BsuirStatsClient()
    top_students = await client.get_top_students(
        speciality=20657,
        course=2,
        lesson_name_abbrev="КПрог",
        lesson_type_abbrev="ЛР"
    )
    print(top_students)

asyncio.run(main())
```
