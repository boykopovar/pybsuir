 pybsuir - статистика и рейтинги студентов БГУИР

![Python](https://img.shields.io/badge/python-3.8%2B-blue?logo=python&logoColor=white)
![Async](https://img.shields.io/badge/asyncio-powered-blueviolet)

Python-библиотека для работы с официальным и неофициальным API БГУИР. Данные соответствуют странице [iis.bsuir.by/rating-of-students](https://iis.bsuir.by/rating-of-students).

## Установка

```bash
pip install pybsuir
```

По умолчанию используется `aiohttp`, устанавливается автоматически как зависимость.

### Установка без зависимостей

```bash
pip install pybsuir --no-deps
```

Без внешних зависимостей библиотека использует встроенную реализацию на `urllib`.

Как альтернативу можно установить `httpx` - он будет использован при отсутствии `aiohttp`:

```bash
pip install httpx
```

`httpx` и встроенная реализация на `urllib` медленнее, чем `aiohttp`.

## Быстрый старт

```python
import asyncio
from pybsuir import BsuirStatsClient

async def main():
    client = BsuirStatsClient()
    students = await client.get_students(20657, 2)
    print(students[0])

asyncio.run(main())
```

Вывод:

```
{
    "studentCardNumber": "12345678",
    "average": 3.89,
    "hours": 80,
    "averageShift": 0.33000000000000007,
    "first": null,
    "second": null,
    "third": null
}
```

Получение статистики потока по конкретному предмету:

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

    place = 1
    for st in top_students:
        print(f"{place}. {st.student_card_number}: {' '.join([str(mark) for mark in st.marks])}")
        place += 1

asyncio.run(main())
```

Вывод:

```
1. 123456: 10 9 10
2. 654321: 9 10 9
...
```

## Возможности

- Список факультетов, специальностей и курсов.
- Рейтинг студентов по курсу и специальности.
- Подробная информация об успеваемости студента.
- Ответы в виде [датаклассов](docs/Types.md).

## Исключения

`BsuirStatsException` - выбрасывается при ошибках HTTP-запроса. Содержит поля: `status`, `url`, `text`, `headers`.

## Документация

[Описание методов и примеры](docs/Methods.md)
