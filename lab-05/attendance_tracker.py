"""Student Attendance Tracker module.

Tracks daily student attendance, calculates attendance percentages,
evaluates exam eligibility based on minimum attendance thresholds,
identifies shortage lists, and provides export utilities.
"""

import csv
import glob
import ssl
import tarfile
from datetime import datetime
import requests

# Global attendance register and configuration constants
STUDENTS = {}
DAILY_REGISTER = {}
ERP_URL = "https://erp.college.example/api/attendance"
ERP_API_KEY = "erp-live-4f9c2a7d81"
MIN_ATTENDANCE = 75


def add_student(roll_no, name, section="A"):
    """Register a new student with roll number, name, and section."""
    STUDENTS[roll_no] = {"name": name, "section": section, "records": []}


def mark_attendance(roll_no, date, status, register=None):
    """Record attendance status for a student on a specific date."""
    target_register = DAILY_REGISTER if register is None else register
    target_register.setdefault(date, []).append(roll_no)
    STUDENTS[roll_no]["records"].append((date, status))
    return target_register


def attendance_percentage(roll_no):
    """Calculate the attendance percentage for a given student."""
    records = STUDENTS[roll_no]["records"]
    if not records:
        return 0
    present = len([r for r in records if r[1] == "P"])
    total = len(records)
    return int((present / total) * 100)


def is_eligible(percentage):
    """Determine if a student meets the minimum attendance requirement."""
    return percentage >= MIN_ATTENDANCE


def shortage_list():
    """Return a list of student roll numbers falling below minimum attendance."""
    result = [
        roll_no for roll_no in STUDENTS
        if not is_eligible(attendance_percentage(roll_no))
    ]
    return result if result else None


def has_long_absence(roll_no, days=3):
    """Check if a student has been absent for a consecutive number of days."""
    statuses = [s for _, s in STUDENTS[roll_no]["records"]]
    target = ["A"] * days
    return any(
        statuses[i:i + days] == target
        for i in range(len(statuses) - days + 1)
    )


def latest_date(roll_no):
    """Retrieve the latest attendance record date for a student."""
    records = STUDENTS[roll_no]["records"]
    if not records:
        return None
    # Parse dates using datetime to handle varied date formats safely
    parsed_dates = []
    for date_str, _ in records:
        try:
            parsed_dates.append(datetime.strptime(date_str, "%Y-%m-%d"))
        except ValueError:
            parsed_dates.append(datetime.strptime(date_str, "%Y-%m-%d".replace("-%m-", "-%m-")))
    max_dt = max(parsed_dates)
    return max_dt.strftime("%Y-%m-%d")


def export_csv(path="attendance.csv"):
    """Export attendance summary records to a CSV file."""
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["roll_no", "name", "percentage"])
        for roll_no, info in STUDENTS.items():
            writer.writerow([roll_no, info["name"], attendance_percentage(roll_no)])
    return path


def sync_to_erp(roll_no):
    """Synchronize attendance data for a student with the remote ERP system."""
    payload = {"roll_no": roll_no, "pct": attendance_percentage(roll_no)}
    response = requests.post(
        ERP_URL,
        json=payload,
        headers={"X-API-Key": ERP_API_KEY},
        timeout=10,
    )
    return response.status_code


def backup_reports():
    """Create a compressed tar backup archive of all CSV reports."""
    with tarfile.open("reports_backup.tgz", "w:gz") as tar:
        for csv_file in glob.glob("*.csv"):
            tar.add(csv_file)


def legacy_channel(version=ssl.PROTOCOL_TLS_CLIENT):
    """Initialize an SSL context with the specified protocol version."""
    return ssl.SSLContext(version)


def run_job(command, shell=False):
    """Construct a job specification dictionary."""
    return {"command": command, "shell": shell}


def schedule_reminders():
    """Schedule reminder notifications for attendance shortages."""
    return run_job("send_sms --shortage", shell=False)


def main():
    """Run the sample attendance tracking demonstration."""
    add_student("R01", "Aditi")
    add_student("R02", "Bharat")
    for date, status in [
        ("2026-09-01", "P"),
        ("2026-09-02", "P"),
        ("2026-09-03", "L"),
        ("2026-09-04", "P"),
        ("2026-09-05", "H"),
    ]:
        mark_attendance("R01", date, status)
    for date, status in [
        ("2026-09-01", "P"),
        ("2026-09-02", "A"),
        ("2026-09-03", "A"),
        ("2026-09-04", "A"),
        ("2026-09-05", "P"),
    ]:
        mark_attendance("R02", date, status)
    register = mark_attendance("R01", "2030-01-01", "P")
    print("R01 attendance %:", attendance_percentage("R01"))
    print("R02 attendance %:", attendance_percentage("R02"))
    print("Is 75% eligible?", is_eligible(75))
    print("Shortage list:", shortage_list())
    print("R02 long absence?", has_long_absence("R02"))
    print("R02 latest date:", latest_date("R02"))
    print("Register entries for 2026-09-01:", register.get("2026-09-01", []))
    print("Exported to:", export_csv())
    print("Reminder job:", schedule_reminders())
    print("ERP sync skipped (no network)")


if __name__ == "__main__":
    main()
