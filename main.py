
import asyncio

from infrastructure.decorators import async_time_log_decorator
from services.data_processors import get_page_content, parse_page_content
from services.represent_services import (ChartMatplotlibRepresenter,
                                         CsvMarksRepresenter,
                                         ExcelMarksRepresenter,
                                         MarksRepresentComposer)


@async_time_log_decorator("Все графики и таблицы созданы!")
async def main() -> None:
    try:
        url = "https://4ege.ru/novosti-ege/4023-shkala-perevoda-ballov-ege.html"
        page_html = await get_page_content(url=url)
        data = parse_page_content(page_html)

        representators = [
            ChartMatplotlibRepresenter(),
            CsvMarksRepresenter(),
            ExcelMarksRepresenter()
        ]
        composer = MarksRepresentComposer()

        for subject in data:
            print('-' * 15)
            print(f"Обработка предмета {subject.title}...")
            composer.represent(subject, representators)
            print('-' * 15)
    except Exception as error:
        print(error)


if __name__ == "__main__":
    asyncio.run(main())
