import re 
import json
import os

import rolltables.constants

class Priortable: 
    """
    Class designed to interface a prior contract table

    Parameters
    ----------
    table : dict
        a mapping of commodity tickers to mapping of contracts to prior contracts
        e.g. "CL":{"F":"Z", ..., "Z":"X"}
    """
    def __init__(self, table):
        if not isinstance(table, dict): 
            raise ValueError("table should be a mapping of commodities to contracts")
        if not all([isinstance(t, dict) for t in table.values()]): 
            raise ValueError("table should be a mapping of commodities to contract")
        self.table = table

    def resolve(self, future):
        """
        resolves the prior contract for a given future contract, i.e. the eligible 
        contract that expires immeditely before the given future

        Parameters
        ----------
        future : str
            the name of the future contract for which we resolve the prior contract
            e.g. CLZ2019

        Returns
        ----------
            prior contract : str

        Raises
        ----------
        ValueError
            if the commodity is not in the prior contract table
            if the month is not in the prior contract table
        """
        if not re.match(f"[A-Za-z ]+[{rolltables.constants.MONTHS}]\d{{4}}", future):
            raise ValueError(f"invalid future name '{future}'")
        commodity, month, year = future[:-5], future[-5], future[-4:]
        if commodity not in self.table: 
            raise ValueError(f"commodity '{commodity}' is not in the prior table")
        if month not in self.table[commodity]: 
            raise ValueError(f"'{future}' is not in the prior contract table")
        if rolltables.constants.MONTHS.index(self.table[commodity][month]) >= \
            rolltables.constants.MONTHS.index(month): 
            return commodity + self.table[commodity][month] + str(int(year)-1)
        return commodity + self.table[commodity][month] + year

    def get(self, future):
        """
        alias for resolve
        """
        return self.resolve(future)

    def __contains__(self, future):
        """
        determines whether a future has a prior contract
        """
        if not re.match(f"[A-Za-z ]+[{rolltables.constants.MONTHS}]\d{{4}}", future):
            raise ValueError(f"invalid future name '{future}'")
        commodity, month = future[:-5], future[-5]
        return month in self.table.get(commodity, {})

with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), "data", "priortables.json"), "r") as file: 
    source = json.load(file)
    
    BCOMRS = Priortable(source["BCOMRS"])
    BCOMRS.source = "https://data.bloomberglp.com/professional/sites/10/BCOM-Methodology-December-2019.pdf"
