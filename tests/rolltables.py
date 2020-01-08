import unittest
import pandas as pd

import rolltables

class TestRolltables(unittest.TestCase):
    def test_initialisation(self): 
        table = rolltables.Rolltable({"CL":["G0","H0","J0","K0","M0","N0","Q0","U0","V0","X0","Z0","F1"]}, "roll-in")
        self.assertIsInstance(table, rolltables.Rolltable)
        self.assertIsInstance(rolltables.BCOM, rolltables.Rolltable)
        self.assertIsInstance(rolltables.GSCI, rolltables.Rolltable)

        with self.assertRaises(ValueError):
            table = rolltables.Rolltable({"CL":["G0","H0","J0","K0","M0","N0","Q0","U0","V0","X0","Z0","F1"]}, "roll")

        with self.assertRaises(ValueError):
            table = rolltables.Rolltable("undefined data", tabletype="roll-in")

        with self.assertRaises(ValueError):
            #small typo in the roll table in February
            table = rolltables.Rolltable({"CL":["G0","P0","J0","K0","M0","N0","Q0","U0","V0","X0","Z0","F1"]}, tabletype="roll-in")

        with self.assertRaises(ValueError):
            #11 contracts
            rolltables.Rolltable({"CL":["G0","H0","J0","K0","M0","N0","Q0","U0","V0","X0","Z0"]}, "roll-in")

    def test_resolver(self):
        table = rolltables.Rolltable({"CL":["H0","H0","K0","K0","N0","N0","U0","U0","X0","X0","F1","F1"]}, "roll-in")

        self.assertEqual(table.resolve("CL", "F0", 12, 2019), "CLF2020")
        self.assertEqual(table.resolve("CL", "F0", 12, 2019, "roll-in"), "CLF2020")
        self.assertEqual(table.resolve("CL", "F0", 12, 2019, "roll-out"), "CLF2020")

        #F contracts
        self.assertEqual(table.resolve("CL", "F1", 12, 2019), "CLH2020")
        self.assertEqual(table.resolve("CL", "F2", 12, 2019), "CLH2020")
        self.assertEqual(table.resolve("CL", "F3", 12, 2019), "CLK2020")
        self.assertEqual(table.resolve("CL", "F4", 12, 2019), "CLK2020")
        self.assertEqual(table.resolve("CL", "F5", 12, 2019), "CLN2020")
        self.assertEqual(table.resolve("CL", "F6", 12, 2019), "CLN2020")

        #C contracts
        self.assertEqual(table.resolve("CL", "C0", 12, 2019), "CLF2020")
        self.assertEqual(table.resolve("CL", "C1", 12, 2019), "CLH2020")
        self.assertEqual(table.resolve("CL", "C2", 12, 2019), "CLK2020")
        self.assertEqual(table.resolve("CL", "C3", 12, 2019), "CLN2020")

        #negative indices
        self.assertEqual(table.resolve("CL", "F-1", 12, 2019), "CLF2020")
        self.assertEqual(table.resolve("CL", "F-2", 12, 2019), "CLX2019")
        self.assertEqual(table.resolve("CL", "C-1", 12, 2019), "CLX2019")
        self.assertEqual(table.resolve("CL", "C-2", 12, 2019), "CLU2019")
        
        #test roll-out table
        table = rolltables.Rolltable({"CL":["H0","H0","K0","K0","N0","N0","U0","U0","X0","X0","F1","F1"]}, "roll-out")

        self.assertEqual(table.resolve("CL", "F0", 12, 2019), "CLF2020")
        self.assertEqual(table.resolve("CL", "F0", 12, 2019, "roll-out"), "CLF2020")
        self.assertEqual(table.resolve("CL", "F0", 12, 2019, "roll-in"), "CLH2020")

        table = rolltables.Rolltable({"CL":["H0","H0","K0","K0","N0","N0","U0","U0","X0","X0","F1","F1"]}, "roll-in")

        self.assertEqual(table.resolve("CL", "F0", 12, 2019, "roll-out"), "CLF2020")
        self.assertEqual(table.resolve("CL", "F0", 12, 2019, "roll-in"), "CLF2020")

        table = rolltables.Rolltable({"CL":["H0","H0","K0","K0","N0","N0","U0","U0","X0","X0","F1","F1"]}, "roll-out")

        self.assertEqual(table.resolve("CL", "F0", 12, 2019, "roll-out"), "CLF2020")
        self.assertEqual(table.resolve("CL", "F0", 12, 2019, "roll-in"), "CLH2020")

        #test exceptions
        with self.assertRaises(ValueError):
            table.resolve("CL", "X0", 12, 2019)
        
        with self.assertRaises(ValueError):
            table.resolve("GC", "F0", 12, 2020)

        with self.assertRaises(ValueError):
            table.resolve("CL", "F0", 0, 2019)

        with self.assertRaises(ValueError):
            table.resolve("CL", "F0", 12, 2019, "roll out")

    def test_contains(self):
        table = rolltables.Rolltable({"CL":["H0","H0","K0","K0","N0","N0","U0","U0","X0","X0","F1","F1"]}, "roll-in")

        self.assertTrue("CLF2020" in table)
        self.assertFalse("CLG2020" in table)

        #must be a valid contract name
        with self.assertRaises(ValueError):
            "CLXXXXX" in table

    def test_reverse(self):
        table = rolltables.Rolltable({"CL":["H0","H0","K0","K0","N0","N0","U0","U0","X0","X0","F1","F1"]}, "roll-in")

        self.assertEqual(table.reverse("CLF2020", 12, 2019), "F0")
        self.assertEqual(table.reverse("CLH2020", 12, 2019), "F1")
        self.assertEqual(table.reverse("CLK2020", 12, 2019), "F3")
        self.assertEqual(table.reverse("CLX2019", 12, 2019), "F-2")

    def test_BCOM(self):
        table = rolltables.BCOM

        self.assertEqual(table.resolve("NG", "F0", 1, 2020, "roll-in"), "NGH2020")
        self.assertEqual(table.resolve("NG", "F0", 1, 2020, "roll-out"), "NGH2020")

        self.assertEqual(table.resolve("NG", "F0", 2, 2020, "roll-in"), "NGK2020")
        self.assertEqual(table.resolve("NG", "F0", 2, 2020, "roll-out"), "NGH2020")

        self.assertEqual(table.resolve("LX", "F0", 6, 2020), "LXN2020")

    def test_GSCI(self):
        table = rolltables.GSCI

        self.assertEqual(table.resolve("WH", "F0", 2, 2020, "roll-in"), "WHK2020")
        self.assertEqual(table.resolve("WH", "F0", 2, 2020, "roll-out"), "WHH2020")

    def test_parse(self):
        parsed = rolltables.parse("FHHKKNNU0UXXF1")

        self.assertEqual(len(parsed), 12)
        self.assertEqual(parsed[0], "F0")
        self.assertEqual(parsed[-1], "F1")

        with self.assertRaises(ValueError): 
            #1 contract missing
            parsed = rolltables.parse("FHHKKNNUXXF1")

        with self.assertRaises(ValueError): 
            #unrecognized letter
            parsed = rolltables.parse("AFHHKKNNUUXXF1")

    def test_parse(self):
        source = pd.DataFrame({"CL":["G0","G0","J0","K0","M0","N0","Q0","U0","V0","X0","Z0","F1"],
                               "GC":["G0","G0","J0","K0","M0","N0","Q0","U0","V0","X0","Z0","F1"]}).T
        table = rolltables.Rolltable.convert(source)

        self.assertIsInstance(table, rolltables.Rolltable)

