from datetime import date
import importlib.util
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch


spec = importlib.util.spec_from_file_location("diary", Path(__file__).with_name("daily-diary-sync.py"))
diary = importlib.util.module_from_spec(spec)
spec.loader.exec_module(diary)


class DiaryTest(unittest.TestCase):
    def test_retry_preserves_manual_notes_and_other_days(self):
        day = date(2026, 11, 23)
        original = "# 월 일지\n## 11-23\n작성자 메모\n## 11-22\n이전 기록\n"
        first = diary.merge(original, day, "- 초안")
        second = diary.merge(first, day, "- 최종")
        self.assertEqual(second, diary.merge(second, day, "- 최종"))
        self.assertEqual(second.count("## 11-23"), 1)
        self.assertIn("작성자 메모", second)
        self.assertTrue(second.endswith("## 11-22\n이전 기록\n"))
        self.assertNotIn("초안", second)

    def test_catchup_only_advances_after_success(self):
        with tempfile.TemporaryDirectory() as tmp:
            state = Path(tmp)
            class Clock(date):
                @classmethod
                def today(cls):
                    return cls(2026, 11, 25)
            with patch.object(diary, "STATE", state), patch.object(diary, "date", Clock), patch(
                "sys.argv", ["sync", "--start", "2026-11-22", "--folder", "example"]
            ), patch.object(diary, "sync", side_effect=["empty", RuntimeError(), "verified", "verified"]) as sync:
                with self.assertRaises(RuntimeError):
                    diary.main()
                self.assertEqual((state / "last-day").read_text(), "2026-11-22")
                diary.main()
                diary.main()
                self.assertEqual([call.args[0].day for call in sync.call_args_list], [22, 23, 23, 24])
                self.assertEqual((state / "last-day").read_text(), "2026-11-24")
