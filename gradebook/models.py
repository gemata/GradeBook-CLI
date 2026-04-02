"""Core data models for the gradebook.

Contains Student, Course, and Enrollment classes with basic validation
and serialization helpers.
"""
from dataclasses import dataclass, field
from typing import List, Dict, Any


def _non_empty_str(value: str, name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{name} must be a non-empty string")
    return value.strip()


@dataclass
class Student:
    id: int
    name: str

    def __post_init__(self) -> None:
        self.name = _non_empty_str(self.name, "name")

    def __str__(self) -> str:
        return f"Student(id={self.id}, name={self.name})"

    def to_dict(self) -> Dict[str, Any]:
        return {"id": self.id, "name": self.name}

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "Student":
        return Student(id=int(data["id"]), name=data["name"])


@dataclass
class Course:
    code: str
    title: str

    def __post_init__(self) -> None:
        self.code = _non_empty_str(self.code, "code")
        self.title = _non_empty_str(self.title, "title")

    def __str__(self) -> str:
        return f"Course(code={self.code}, title={self.title})"

    def to_dict(self) -> Dict[str, Any]:
        return {"code": self.code, "title": self.title}

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "Course":
        return Course(code=data["code"], title=data["title"])


@dataclass
class Enrollment:
    student_id: int
    course_code: str
    grades: List[float] = field(default_factory=list)

    def __post_init__(self) -> None:
        if not isinstance(self.student_id, int):
            raise ValueError("student_id must be an integer")
        self.course_code = _non_empty_str(self.course_code, "course_code")
        # Normalize grades to floats
        self.grades = [float(g) for g in self.grades]

    def __str__(self) -> str:
        return f"Enrollment(student_id={self.student_id}, course_code={self.course_code}, grades={self.grades})"

    def to_dict(self) -> Dict[str, Any]:
        return {"student_id": self.student_id, "course_code": self.course_code, "grades": self.grades}

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "Enrollment":
        return Enrollment(student_id=int(data["student_id"]), course_code=data["course_code"], grades=list(data.get("grades", [])))
