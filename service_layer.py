
"""APPLICATION LAYER: business rules. Knows nothing about HTTP or SQL."""

import re
import data_layer as db


class ValidationError(Exception):
    pass


class NotFoundError(Exception):
    pass


class DuplicateError(Exception):
    pass


REG_PATTERN = re.compile(r"^[A-Z0-9]+([/\-][A-Z0-9]+){1,7}$")


def _clean(data):
    reg_no = (data.get("reg_no") or "").strip().upper()
    name = (data.get("name") or "").strip()
    course = (data.get("course") or "").strip()

    try:
        year = int(data.get("year"))
    except (TypeError, ValueError):
        raise ValidationError("Year must be a number between 1 and 4")

    if not REG_PATTERN.match(reg_no):
        raise ValidationError(
            "Reg number must be groups of letters or digits split by / or - (e.g. BDSA/MK/4079/09/25)"
        )

    if len(reg_no) > 30:
        raise ValidationError("Reg number is too long")

    if len(name) < 2:
        raise ValidationError("Name is required")

    if not course:
        raise ValidationError("Course is required")

    if not 1 <= year <= 4:
        raise ValidationError("Year must be a number between 1 and 4")

    return reg_no, name, course, year


def register_student(data):
    reg_no, name, course, year = _clean(data)

    if db.find_by_reg_no(reg_no):
        raise DuplicateError(f"Reg number {reg_no} already exists")

    return db.insert(reg_no, name, course, year)


def list_students():
    return db.fetch_all()


def edit_student(student_id, data):
    reg_no, name, course, year = _clean(data)

    existing = db.find_by_reg_no(reg_no)

    if existing and existing["id"] != student_id:
        raise DuplicateError(f"Reg number {reg_no} already exists")

    if db.update(student_id, reg_no, name, course, year) == 0:
        raise NotFoundError("Student not found")


def remove_student(student_id):
    if db.delete(student_id) == 0:
        raise NotFoundError("Student not found")
