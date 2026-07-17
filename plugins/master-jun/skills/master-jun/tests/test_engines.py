#!/usr/bin/env python3

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / "scripts"))
from daliuren_core import calculate
from time_basis import resolve
from bazi_core import inspect_chart
from ziwei_base import calculate as ziwei


class DaLiurenRegression(unittest.TestCase):
    def assert_transmissions(self, stem, branch, general, hour, method, expected):
        result = calculate(stem, branch, general, hour)
        self.assertTrue(result["method"].startswith(method))
        self.assertEqual("".join(x["branch"] for x in result["three_transmissions"]), expected)

    def test_synthetic_method_fixtures(self):
        # Artificial fixtures selected only to exercise distinct engine paths.
        # They are not copied from a user, consultation, or real-world event.
        cases = [
            ("甲", "子", "子", "子", "伏吟", "寅巳申"),
            ("甲", "子", "子", "寅", "元首", "戌申午"),
            ("甲", "子", "子", "丑", "比用", "子亥戌"),
            ("甲", "子", "子", "辰", "重审", "戌午寅"),
            ("甲", "辰", "子", "寅", "涉害", "寅子戌"),
            ("甲", "寅", "子", "卯", "蒿矢", "申巳寅"),
            ("甲", "寅", "子", "申", "弹射", "戌寅午"),
            ("乙", "未", "子", "丑", "昴星", "戌卯午"),
            ("丙", "辰", "子", "亥", "别责", "亥午午"),
            ("丁", "未", "子", "丑", "八专", "卯午午"),
        ]
        for case in cases:
            with self.subTest(case=case): self.assert_transmissions(*case)


class SupportEngines(unittest.TestCase):
    def test_boundary_detection(self):
        x = resolve("2031-03-15T12:00:00+08:00", "昨天", "10:59", 5)
        self.assertEqual(x["date"], "2031-03-14"); self.assertTrue(x["boundary_sensitive"])

    def test_bazi_verified_input(self):
        x = inspect_chart(["甲子", "丙寅", "戊辰", "庚申"])
        self.assertEqual(x["day_master"], "戊"); self.assertIn("辰", x["roots"])

    def test_ziwei_base(self):
        x = ziwei(1, "申", "乙", "女")
        self.assertEqual(x["major_cycle_direction"], "顺"); self.assertEqual(x["status"], "BASE_ONLY")


if __name__ == "__main__": unittest.main()
