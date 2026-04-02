"""Seed script to create sample data and save to data/gradebook.json."""
from pathlib import Path

from gradebook.service import Gradebook


def seed(path: str | None = None):
    gb = Gradebook(path=path)
    # If there are already students, assume seeded
    if gb.list_students():
        print("Gradebook already has data; skipping seed")
        return

    s1 = gb.add_student("Blend")
    s2 = gb.add_student("Berat")

    c1 = gb.add_course("CS101", "Intro to CS")
    c2 = gb.add_course("MATH200", "Calculus")

    gb.enroll(s1, c1)
    gb.enroll(s1, c2)
    gb.enroll(s2, c1)

    gb.add_grade(s1, c1, 92)
    gb.add_grade(s1, c1, 85)
    gb.add_grade(s1, c2, 78)
    gb.add_grade(s2, c1, 88)

    print("Seeded sample data")


if __name__ == "__main__":
    seed()
