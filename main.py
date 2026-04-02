"""Command-line interface for the gradebook application."""
import argparse
import logging
from pathlib import Path

from gradebook.service import Gradebook, parse_grade


LOG_PATH = Path("logs") / "app.log"
LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s", handlers=[
                    logging.FileHandler(LOG_PATH, encoding="utf-8"), logging.StreamHandler()])
LOGGER = logging.getLogger(__name__)


def main(argv=None):
    parser = argparse.ArgumentParser(prog="gradebook")
    parser.add_argument("--data", default=None,
                        help="Path to data file (JSON)")
    sub = parser.add_subparsers(dest="cmd")

    a_add_student = sub.add_parser("add-student")
    a_add_student.add_argument("--name", required=True)

    a_add_course = sub.add_parser("add-course")
    a_add_course.add_argument("--code", required=True)
    a_add_course.add_argument("--title", required=True)

    a_enroll = sub.add_parser("enroll")
    a_enroll.add_argument("--student-id", required=True, type=int)
    a_enroll.add_argument("--course", required=True)

    a_add_grade = sub.add_parser("add-grade")
    a_add_grade.add_argument("--student-id", required=True, type=int)
    a_add_grade.add_argument("--course", required=True)
    a_add_grade.add_argument("--grade", required=True)

    a_list = sub.add_parser("list")
    a_list.add_argument(
        "what", choices=["students", "courses", "enrollments"], nargs=1)

    a_avg = sub.add_parser("avg")
    a_avg.add_argument("--student-id", required=True, type=int)
    a_avg.add_argument("--course", required=True)

    a_gpa = sub.add_parser("gpa")
    a_gpa.add_argument("--student-id", required=True, type=int)

    args = parser.parse_args(argv)
    gb = Gradebook(path=args.data)

    try:
        if args.cmd == "add-student":
            sid = gb.add_student(args.name)
            print(f"Added student id={sid}")
        elif args.cmd == "add-course":
            code = gb.add_course(args.code, args.title)
            print(f"Added course {code}")
        elif args.cmd == "enroll":
            gb.enroll(args.student_id, args.course)
            print("Enrolled")
        elif args.cmd == "add-grade":
            g = parse_grade(args.grade)
            gb.add_grade(args.student_id, args.course, g)
            print("Grade added")
        elif args.cmd == "list":
            if args.what[0] == "students":
                for s in gb.list_students():
                    print(s)
            elif args.what[0] == "courses":
                for c in gb.list_courses():
                    print(c)
            else:
                for e in gb.list_enrollments():
                    print(e)
        elif args.cmd == "avg":
            avg = gb.compute_average(args.student_id, args.course)
            if avg is None:
                print("No grades yet")
            else:
                print(f"Average: {avg:.2f}")
        elif args.cmd == "gpa":
            gpa = gb.compute_gpa(args.student_id)
            if gpa is None:
                print("No grades yet")
            else:
                print(f"GPA (mean of course averages): {gpa:.2f}")
        else:
            parser.print_help()
    except Exception as exc:
        LOGGER.exception("Error while running command: %s", exc)
        print(f"Error: {exc}")


if __name__ == "__main__":
    main()
