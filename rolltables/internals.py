import datetime
import re 

def polyarg(function):
    """
    Decorators intended to superchage the Rolltable.resolve
    """
    def inner(self, *args, **kwargs):
        for arg in args:
            if arg is None: 
                continue 
            if isinstance(arg, (datetime.datetime, datetime.date)): 
                kwargs["month"] = arg.month
                kwargs["year"] = arg.year
            elif isinstance(arg, (int, float)) and int(arg) == arg and 1900 < arg < 2100: 
                kwargs["year"] = int(arg)
            elif isinstance(arg, (int, float)) and int(arg) == arg and 1 <= arg <= 12: 
                kwargs["month"] = int(arg)
            elif arg in ["roll-in", "roll-out"]: 
                kwargs["which"]  = arg
            elif isinstance(arg, str) and re.match("(F|C)-?[0-9]", arg): 
                kwargs["forward"] = arg
            else: 
                kwargs["commodity"] = arg
        if "forward" not in kwargs:
            kwargs["forward"] = "F0"
        if "which" not in kwargs:
            kwargs["which"] = None
        for kwarg in ["commodity","forward","month","year","which"]: 
            if kwarg not in kwargs: 
                raise ValueError(f"no value given for '{kwarg}'")
        return function(self, **kwargs)
    return inner