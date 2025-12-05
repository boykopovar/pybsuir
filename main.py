import asyncio
from pybsuir import BsuirStatsClient


async def main():
    client = BsuirStatsClient()
    top_students = await client.get_top_students(
        speciality=20657,
        course=2,
        lesson_name_abbrev="КПрог",
        lesson_type_abbrev="ЛК"
    )

    place = 1
    for st in top_students:
        print(f"{place}. {st.student_card_number}: {' '.join([str(mark) for mark in st.marks])}")
        place+=1



asyncio.run(main())