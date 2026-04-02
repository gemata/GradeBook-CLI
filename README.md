# Gradebook CLI

Small Python CLI project for managing students, courses, enrollments, and grades.

Usage (basic):

- Seed sample data:

```bash
python -m scripts.seed
```

- Run CLI:

```bash
python main.py add-student --name "Blend"
python main.py add-course --code CS101 --title "Intro to CS"
python main.py enroll --student-id 1 --course CS101
python main.py add-grade --student-id 1 --course CS101 --grade 95
python main.py list students
python main.py avg --student-id 1 --course CS101
python main.py gpa --student-id 1
```

Data is stored in `data/gradebook.json` by default. Configure a different path with `--data`.

Run tests:

```bash
python -m unittest discover -v
python -m unittest discover -s tests -p "test_*.py" -v
```

Design decisions & limitations:

- Persistence is JSON-based and simple; concurrent access is not handled.
- Grades are floats in range 0–100.
- `compute_gpa` is a simple mean of course averages.
