import unittest
import tempfile
import shutil
from pathlib import Path

from gradebook.service import Gradebook


class TestService(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.mkdtemp()
        self.path = Path(self.dir) / "gradebook.json"
        self.gb = Gradebook(path=str(self.path))

    def tearDown(self):
        shutil.rmtree(self.dir)

    def test_add_student_and_persist(self):
        sid = self.gb.add_student("Test Student")
        self.assertIsInstance(sid, int)
        # reload from disk
        gb2 = Gradebook(path=str(self.path))
        self.assertIn(sid, [s.id for s in gb2.list_students()])

    def test_add_grade_and_average(self):
        sid = self.gb.add_student("S")
        self.gb.add_course("CS101", "Intro")
        self.gb.enroll(sid, "CS101")
        self.gb.add_grade(sid, "CS101", 90)
        self.gb.add_grade(sid, "CS101", 80)
        avg = self.gb.compute_average(sid, "CS101")
        self.assertAlmostEqual(avg, 85.0)

    def test_average_no_grades_raises_none(self):
        sid = self.gb.add_student("S2")
        self.gb.add_course("CS102", "Intro2")
        self.gb.enroll(sid, "CS102")
        avg = self.gb.compute_average(sid, "CS102")
        self.assertIsNone(avg)


if __name__ == "__main__":
    unittest.main()
