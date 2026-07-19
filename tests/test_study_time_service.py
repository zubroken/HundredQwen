import unittest
from datetime import datetime, timedelta
from pathlib import Path
from tempfile import TemporaryDirectory

from services.study_time_service import StudyTimeService


class StudyTimeServiceTest(unittest.TestCase):
    def setUp(self):
        self.temp_dir = TemporaryDirectory()
        self.db_path = Path(self.temp_dir.name) / "study-time.db"
        self.now = datetime(2026, 7, 18, 10, 0, 0)
        self.service = StudyTimeService(self.db_path, clock=lambda: self.now)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_new_student_starts_with_26_hours_in_current_week(self):
        summary = self.service.get_summary("stu_001")

        self.assertEqual(summary["week_seconds"], 26 * 60 * 60)
        self.assertEqual(summary["total_seconds"], 26 * 60 * 60)
        self.assertFalse(summary["active"])

    def test_start_and_pause_session_adds_elapsed_time_once(self):
        self.service.start("stu_001")
        self.now += timedelta(minutes=45)

        summary = self.service.pause("stu_001")

        self.assertEqual(summary["week_seconds"], 26 * 60 * 60 + 45 * 60)
        self.assertFalse(summary["active"])

    def test_student_cannot_start_two_active_sessions(self):
        self.service.start("stu_001")

        with self.assertRaises(ValueError):
            self.service.start("stu_001")


if __name__ == "__main__":
    unittest.main()
