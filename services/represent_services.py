
from abc import ABC, abstractmethod
from typing import Iterable

import matplotlib.pyplot as plt
import pandas as pd

from domain.structures import SubjectData
from infrastructure.decorators import sync_time_log_decorator


class MarksRepresenter(ABC):
    @abstractmethod
    def represent(self, subject: SubjectData):
        raise NotImplementedError


class ChartMatplotlibRepresenter(MarksRepresenter):
    @sync_time_log_decorator("График успешно создан!")
    def represent(self, subject: SubjectData) -> None:
        x_data = [mark.first_mark for mark in subject.marks]
        y_data = [mark.second_mark for mark in subject.marks]
        
        plt.figure(figsize=(10, 6))
        
        plt.plot(
            x_data, 
            y_data,
            'o-',
            markersize=8,
            linewidth=2,
            color='#1f77b4',
            markeredgecolor='white',
            markeredgewidth=1.5,
            label=f'Данные по предмету "{subject.title}"'
        )
        
        plt.xlabel("Первичные баллы", fontsize=12, fontweight='medium')
        plt.ylabel("Вторичные баллы", fontsize=12, fontweight='medium')
        plt.title(f"Зависимость вторичных баллов от первичных\n{subject.title}", 
                fontsize=14, fontweight='bold', pad=20)
        
        plt.grid(True, which='both', linestyle='--', linewidth=0.5, alpha=0.7)
        plt.minorticks_on()
        plt.grid(True, which='minor', linestyle=':', linewidth=0.3, alpha=0.4)
        
        plt.legend(loc='best', fontsize=11, framealpha=0.9, shadow=True)
        
        plt.xlim(min(x_data) - 1, max(x_data) + 1)
        plt.ylim(min(y_data) - 5, max(y_data) + 5)
        
        if len(x_data) > 1:
            plt.annotate(f'({x_data[0]}, {y_data[0]})', 
                        xy=(x_data[0], y_data[0]), 
                        xytext=(5, 5), textcoords='offset points',
                        fontsize=9, ha='left')
            plt.annotate(f'({x_data[-1]}, {y_data[-1]})', 
                        xy=(x_data[-1], y_data[-1]), 
                        xytext=(5, -15), textcoords='offset points',
                        fontsize=9, ha='left')
        
        plt.tight_layout()
        
        filename = f"{subject.title}_marks.png"
        plt.savefig(filename, dpi=150, bbox_inches='tight')
        plt.close()


class TablePandasRepresenter(MarksRepresenter):
    def _prepare_data(self, subject: SubjectData) -> pd.DataFrame:
        data = [
            {
                "Первичный балл": mark.first_mark,
                "Вторичный балл": mark.second_mark
            }
            for mark in subject.marks
        ]

        return pd.DataFrame(data)


class CsvMarksRepresenter(TablePandasRepresenter):
    @sync_time_log_decorator("Таблица CSV успешно создана!")
    def represent(self, subject: SubjectData) -> None:
        df = self._prepare_data(subject)
        df.to_csv(f"{subject.title}_marks.csv", index=False)


class ExcelMarksRepresenter(TablePandasRepresenter):
    @sync_time_log_decorator("Таблица Excel успешно создана!")
    def represent(self, subject: SubjectData) -> None:
        df = self._prepare_data(subject)
        df.to_excel(f"{subject.title}_marks.xlsx", index=False)


class TextMarksRepresenter(MarksRepresenter):
    @sync_time_log_decorator("Текстовый файл успешно создан!")
    def represent(self, subject: SubjectData):
        with open(
            f"{subject.title}_marks.txt",
            mode="w",
            encoding="utf-8"
        ) as file:
            file.write(f"Предмет: {subject.title}\n")
            file.write("Первичный балл | Вторичный балл\n")

            for mark in subject.marks:
                file.write(f"{mark.first_mark} | {mark.second_mark}\n")


class MarksRepresentComposer:
    def represent(self, subject: SubjectData, representators: Iterable[MarksRepresenter]) -> None:
        for representator in representators:
            representator.represent(subject)
