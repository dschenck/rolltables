import re 
import json
import os
import pandas as pd

import rolltables.constants

class Rolltable: 
    """
    Class designed to interface a commodity roll-table, where users can resolve
    the current forward ("F0") contract or any other contract that would be be
    the current forward contract some months from the given review date
    
    Parameters
    ----------
    table : dict
        a mapping of commodity tickers to list of 12 contracts
        e.g. "CL":["G0","G0","J0","J0","M0","M0","Q0","U0","V0","Z0","Z0","F1"]
    
    tabletype : str, optional (defaults to 'roll-out')
        must be one of 'roll-in' or 'roll-out'
        specifies whether the provided table is a roll-out table or a roll-in
        table, i.e. whether the contract listed for each month is the contract 
        that prevails before or after the roll period.
        
    Raises
    ----------
    ValueError
        on invalid arguments
    """
    def __init__(self, table, tabletype="roll-out"): 
        if not isinstance(table, dict):
            raise ValueError("table should be a mapping of commodity tickers to list of 12 contracts")
        if not all(len(t) == 12 for t in table.values()):
            raise ValueError("table should be a mapping of commodity tickers to list of 12 contracts")
        if not all(all(re.match(f"[{rolltables.constants.MONTHS}]\d?", c) for c in t) for t in table.values()): 
            raise ValueError(f"contracts should be of the form '[{rolltables.constants.MONTHS}]\d?'")
        self.table = table
        if tabletype not in ["roll-in", "roll-out"]: 
            raise ValueError("tabletype should be one of 'roll-in', 'roll-out', {tabletype} given")
        self.tabletype = tabletype

    def __contains__(self, future):
        """
        determines whether a given future contract is in the roll table, i.e. whether the given future
        is eligible for trading under this roll table. The commodity must be in the roll table

        Parameters
        ----------
        future : str
            a future full name (e.g. CLZ2019)

        Returns
        ----------
        maybe : bool
            True if the contract is in the rolltable, False otherwise

        Raises
        ----------
        ValueError
            on invalid arguments
        """
        future = str(future)
        if not re.match(f"[A-Za-z ]+[{rolltables.constants.MONTHS}]\d{{4}}", future):
            raise ValueError("invalid future name")
        commodity, month, year = future[:-5], future[-5], future[-4:]
        for contract in self.table.get(commodity, []): 
            if contract[0] == month:
                return True
        return False

    def reverse(self, future, month, year, which=None):
        """
        resolves the F-name of the given future contract
        as long as the contract is within 9 Fs of the current F0
        if the same contract is held over several rolltables.constants.MONTHS, this returns
        the nearest F-name from the current F0

        Parameters
        ----------
        future : str
            a future full name (e.g. CLZ2019)
        month : int
            must be one of 1..12
        year : int: 
            must be one of 1950..2050
        which : str, optional
            must be one of None, 'roll-in' or 'roll-out'
            specifies whether the requested forward should be the one that 
            prevails before or after the roll period
            if which is None, then it is assumed it is the same as the table type

        Returns
        ----------
        F-name : str
            one of [F-9..F9]

        Raises
        ----------
        ValueError: 
            on invalid arguments
        """
        if future not in self: 
            raise ValueError(f"future {future} is not in the rolltable")
        for index in range(10):
            if future == self.resolve(future[:-5], f"F{index}", month, year, which): 
                return f"F{index}"
        for index in range(10): 
            if future == self.resolve(future[:-5], f"F-{index}", month, year, which): 
                return f"F-{index}"
        raise ValueError(f"future {future} is out of range")
        
    def resolve(self, commodity, forward, month, year, which=None):
        """
        resolves a forward contract to its actual fullname
        
        Parameters
        ----------
        commodity : str
            a commodity ticker (must be in the roll table)
        forward : str
            one of F0..F9 or C0..C9
            if forward is one of FX, then the method returns the F0 contract
            that prevails X rolltables.constants.MONTHS from the given (month, year)
            if forward is one of CX, then the method returns the X-th distinct 
            contract in the roll table offset from the F0 on the given (month, year)
        month : int
            must be one of 1..12
        year : int: 
            must be one of 1950..2050
        which : str, optional
            must be one of None, 'roll-in' or 'roll-out'
            specifies whether the requested forward should be the one that 
            prevails before or after the roll period
            if which is None, then it is assumed it is the same as the table type
            
        Returns
        ----------
        future : str
            the fullname of the future contract

        Example
        ----------
        rolltable.resolve("CL", "F2", 12, 2019)
        > CLG2020
        
        Raises
        ----------
        ValueError
            on invalid arguments
        """
        if not re.match("(F|C)-?[0-9]", forward):
            raise ValueError(f"expected forward to be one of F0..F9 or C1..C9, {forward} given")
        if not commodity in self.table: 
            raise ValueError(f"commodity {commodity} not in roll table")
        if not 1 <= month <= 12: 
            raise ValueError(f"month should be one of 1..12, {month} given")
        if not 1950 <= year <= 2050:
            raise ValueError(f"year should be one of 1950..2050, {year} given")
        if which is None: 
            which = self.tabletype
        if which not in ["roll-in", "roll-out"]: 
            raise ValueError(f"which should be one of 'roll-in', 'roll-out', {which} given")
        if forward[0] == "F":
            index = int(forward[1:]) + (1 if which == "roll-in" else 0) - (1 if self.tabletype == "roll-in" else 0)
            month, year = (month - 1 + 12 * year + index) % 12 + 1, year + (month + index - 1)//12
            generic = self.table[commodity][month-1]
            return commodity + generic[0] + str(year + int(generic[1:] if len(generic) != 1 else 0))
        
        if forward[0] == "C": 
            index, current = int(forward[1:]), self.resolve(commodity, "F0", month, year, which)
            while index != 0: 
                if index > 0: 
                    if month == 12: 
                        month, year = 1, year + 1
                    else: 
                        month, year = month + 1, year
                    if current != self.resolve(commodity, "F0", month, year, which):
                        current = self.resolve(commodity, "F0", month, year, which)
                        index = index - 1
                else: 
                    if month == 1: 
                        month, year = 12, year - 1
                    else: 
                        month, year = month - 1, year
                    if current != self.resolve(commodity, "F0", month, year, which):
                        current = self.resolve(commodity, "F0", month, year, which)
                        index = index + 1
            return current

    @staticmethod
    def convert(data):
        """
        converts a pd.Series or a pd.DataFrame into a rolltable
        """
        if isinstance(data, pd.Series):
            if not len(data) == 12: 
                raise ValueError(f"expected 12 points from pd.Series, received {len(data)}")
            return rolltables.Rolltable({data.name:data.values})

        if isinstance(data, pd.DataFrame):
            if not len(data.columns) == 12: 
                raise ValueError(f"expected 12 columns from pd.DataFrame, received {len(data.columns)}")
            return rolltables.Rolltable({row.name:row.values for i, row in data.iterrows()})

        raise ValueError(f"expected pd.Series or pd.DataFrame, received {type(data)}")

with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), "data", "rolltables.json"), "r") as file: 
    source = json.load(file)
    
    BCOM = Rolltable(source["BCOM"], tabletype="roll-out")
    BCOM.source = "https://data.bloomberglp.com/indices/sites/2/2018/02/BCOM-Methodology-January-2018_FINAL-2.pdf#page=38"

    GSCI = Rolltable(source["GSCI"], tabletype="roll-out")
    GSCI.source = "https://www.spindices.com/documents/methodologies/methodology-sp-gsci.pdf#page=27"