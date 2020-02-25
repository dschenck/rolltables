import re

import rolltables
import rolltables.constants 

def parse(string):
    """
    parses a string of contracts into a list
    e.g. 'GHJKMNQUVXZF1' >> ['G0', 'H0', 'J0', 'K0'...'F1']

    Parameters
    ----------
    string : str
        pseudo-table of contracts

    Returns
    ----------
    contracts : list
        list of generic contract name, e.g. ['G0', 'H0', 'J0', 'K0'...'F1']
    """
    match = re.match(f"([{rolltables.constants.MONTHS}]\d?)" * 12, string)
    if not match:
        raise ValueError("invalid pseudo-table")
    return [contract + ("0" if len(contract) == 1 else "") for contract in match.groups()]

class F(str):
    """
    Forward index

    Arguments
    -------------
    index : int
        the forward index

    Example
    -------------
    >>> F(0) + 1
    'F1'
    >>> F(6) - 1
    'F5'
    """ 
    def __new__(cls, index):
        value = str.__new__(cls, f"F{index}")
        value.index = index
        return value
    
    def __add__(self, other):
        if isinstance(other, int): 
            return F(self.index + other)
    
    def __sub__(self, other):
        if isinstance(other, int): 
            return F(self.index - other)
        
def C(str):
    """
    Distinct forward index
    """
    def __new__(cls, index):
        value = str.__new__(cls, f"C{index}")
        value.index = index
        return value
    
    def __add__(self, other):
        if isinstance(other, int): 
            return C(self.index + other)
    
    def __sub__(self, other):
        if isinstance(other, int): 
            return C(self.index - other)