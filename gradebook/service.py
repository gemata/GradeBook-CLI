"""Business logic for the gradebook.

Provides a `Gradebook` class that wraps an in-memory dataset and exposes
functions to add students/courses/enrollments/grades and compute averages.
"""
from typing import Dict, List, Optional
import logging

from .models import Student, Course, Enrollment
from .storage import load_data, save_data

LOGGER = logging.getLogger(__name__)


def parse_grade(value: float) -> float:
    try:
        g = float(value)
    except Exception:
        raise ValueError("grade must be a number between 0 and 100")
    if not (0 <= g <= 100):
        raise ValueError("grade must be between 0 and 100")
    return g


class Gradebook:
    def __init__(self, path: str | None = None) -> None:
        self._path = path
        raw = load_data(path)
        self.students: Dict[int, Student] = {
            int(s["id"]): Student.from_dict(s) for s in raw.get("students", [])}
        self.courses: Dict[str, Course] = {
            c["code"]: Course.from_dict(c) for c in raw.get("courses", [])}
        self.enrollments: List[Enrollment] = [
            Enrollment.from_dict(e) for e in raw.get("enrollments", [])]
        self._next_student_id = max(self.students.keys(), default=0) + 1

    def _persist(self) -> None:
        data = {
            "students": [s.to_dict() for s in self.students.values()],
            "courses": [c.to_dict() for c in self.courses.values()],
            "enrollments": [e.to_dict() for e in self.enrollments],
        }
        save_data(data, self._path)

    def add_student(self, name: str) -> int:
        sid = self._next_student_id
        student = Student(id=sid, name=name)
        self.students[sid] = student
        self._next_student_id += 1
        LOGGER.info("Added student %s", student)
        self._persist()
        return sid

    def add_course(self, code: str, title: str) -> str:
        code = code.strip()
        if code in self.courses:
            raise ValueError("Course code already exists")
        course = Course(code=code, title=title)
        self.courses[course.code] = course
        LOGGER.info("Added course %s", course)
        self._persist()
        return course.code

    def enroll(self, student_id: int, course_code: str) -> None:
        if student_id not in self.students:
            raise KeyError("Unknown student id")
        if course_code not in self.courses:
            raise KeyError("Unknown course code")
        for e in self.enrollments:
            if e.student_id == student_id and e.course_code == course_code:
                LOGGER.info("Student %s already enrolled in %s",
                            student_id, course_code)
                return
        enrollment = Enrollment(student_id=student_id, course_code=course_code)
        self.enrollments.append(enrollment)
        LOGGER.info("Enrolled student %s in %s", student_id, course_code)
        self._persist()

    def add_grade(self, student_id: int, course_code: str, grade: float) -> None:
        g = parse_grade(grade)
        for e in self.enrollments:
            if e.student_id == student_id and e.course_code == course_code:
                e.grades.append(g)
                LOGGER.info("Added grade %s to %s/%s",
                            g, student_id, course_code)
                self._persist()
                return
        raise KeyError("Enrollment not found for student/course")

    def list_students(self):
        return list(self.students.values())

    def list_courses(self):
        return list(self.courses.values())

    def list_enrollments(self):
        return list(self.enrollments)

    def compute_average(self, student_id: int, course_code: str) -> Optional[float]:
        for e in self.enrollments:
            if e.student_id == student_id and e.course_code == course_code:
                if not e.grades:
                    return None
                return sum(e.grades) / len(e.grades)
        raise KeyError("Enrollment not found for student/course")

    def compute_gpa(self, student_id: int) -> Optional[float]:
        # simple mean of course averages
        avgs = []
        for e in self.enrollments:
            if e.student_id == student_id:
                if e.grades:
                    avgs.append(sum(e.grades) / len(e.grades))
        if not avgs:
            return None
        return sum(avgs) / len(avgs)
