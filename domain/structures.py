
from dataclasses import dataclass, field


@dataclass
class MarkData:
    first_mark: int
    second_mark: int


@dataclass
class SubjectData:
    title: str
    marks: list[MarkData] = field(default_factory=list)
