
import aiohttp
from bs4 import BeautifulSoup

from domain.structures import MarkData, SubjectData
from infrastructure.decorators import (async_time_log_decorator,
                                       sync_time_log_decorator)
from infrastructure.exceptions import RequestError


@async_time_log_decorator("Контент страницы успешно получен!")
async def get_page_content(url: str) -> str:
    async with aiohttp.ClientSession() as session:
        response = await session.get(url=url)
        status_code = response.status

        if status_code != 200:
            raise RequestError(f"Неверный статус код ответа: {status_code}")

        html = await response.text()
        return html


@sync_time_log_decorator("Контент страницы успешно обработан!")
def parse_page_content(html: str) -> list[SubjectData]:
    soup = BeautifulSoup(html, "lxml")

    subject_titles = soup.find_all(
        "div", 
        {
            "class": "title_spoiler"
        }
    )
    subject_titles = [title.find('a').text for title in subject_titles[2:]] 
    # [2:] - скип минимальных баллов за год и базовой математики


    marks_table = soup.find_all(
        "table",
        {
            "class": "bnjun"
        }
    )
    marks_table.pop(2) 
    # .pop(2) - скип распределения баллов для профильной математики

    subject_marks = []
    for mark in marks_table[1:]: # [1:] - скип базовой математики
        data = []
        rows = mark.find_all('tr')[1:] # [1:] - скип первого ряда с текстом

        for row in rows:
            first_mark, second_mark = map(lambda x: x.text, row.find_all('td'))
            mark_data = MarkData(int(first_mark), int(second_mark))

            data.append(mark_data)

        subject_marks.append(data)

    data = []
    for title, marks in zip(subject_titles, subject_marks):
        data.append(SubjectData(title, marks))
    return data
