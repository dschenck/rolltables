import unittest

import datetime

from rolltables.priortables import Priortable
from rolltables.constants import MONTHS

class TestPriorContractTables(unittest.TestCase):
    def test_initialization(self):
        table = Priortable({"CL":{x:MONTHS[MONTHS.index(x) -1] for x in MONTHS}})
        self.assertIsInstance(table, Priortable)

    def test_resolver(self):
        table = Priortable({"CL":{x:MONTHS[MONTHS.index(x) -1] for x in MONTHS}})

        self.assertEqual(table.resolve("CLX2019"), "CLV2019")
        self.assertEqual(table.resolve("CLZ2019"), "CLX2019")
        self.assertEqual(table.resolve("CLF2020"), "CLZ2019")
        self.assertEqual(table.resolve("CLG2020"), "CLF2020")

        with self.assertRaises(ValueError):
            table.resolve("XBZ2019")

        with self.assertRaises(ValueError):
            table.resolve("CLZ219")

        self.assertEqual(table.get("CLX2019"), "CLV2019")
        self.assertEqual(table.get("CLZ2019"), "CLX2019")
        self.assertEqual(table.get("CLF2020"), "CLZ2019")
        self.assertEqual(table.get("CLG2020"), "CLF2020")

        with self.assertRaises(ValueError):
            table.get("XBZ2019")

        with self.assertRaises(ValueError):
            table.get("CLZ219")

    def test_contains(self):
        table = Priortable({"CL":{x:MONTHS[MONTHS.index(x) -1] for x in MONTHS}})

        self.assertEqual("CLZ2019" in table, True)