Rolltables made easy
======================================
Major commodity future indices, like the Bloomberg Commodity Index (BCOM) and the S&P GSCI periodically roll future contracts following a pre-determined contract schedule. Such a schedule is known as a rolltable. The **Rolltables** module provides an easy-to-use interface to resolve active future contracts and prior contracts. 

Quickstart
-------------------------------------
Installing rolltables is simple with pip: 
::

    $ pip install rolltables

Using rolltables is also easy
::

   >>> from rolltables import Rolltable, BCOM, GSCI

   #determine the current active contract
   >>> BCOM.resolve("CL", "F0", 2, 2020, "roll-out")
   'CLH2020'

   #determine the next active future
   >>> BCOM.resolve("CL", "F0", 2, 2020, "roll-in")
   'CLK2020'

   #resolve the F6 contract
   >>> BCOM.resolve("CL", "F6", 2, 2020, "roll-in")
   'CLU2020'

   #resolve the C2 contract (2nd distinct contract after F0)
   >>> BCOM.resolve("CL", "C2", 2, 2020, "roll-in")
   'CLU2020'

Creating your custom rolltable
---------------------------------
Creating a rolltable simply involves passing a dictionary mapping a commodity name (e.g. :code:`NG`) to a list of nearby contracts. Each contract should be comprised of a month letter (:code:`F` for January...) and a year offset (:code:`0` for the same month, :code:`1` for next year, etc.)

::

   >>> from rolltables import Rolltable
   
   >>> table = Rolltable({"CL":["G0","H0","J0","K0","M0","N0","Q0","U0","V0","X0","Z0","F1"]}, "roll-in")
   >>> table.resolve("CL", "F0", 3, 2020)
   'CLJ2020'

   #you can also generate a rolltable from a pandas.DataFrame
   #the dataframe should have 12 columns, with the index representing commodity names
   >>> table = Rolltable.parse(data, "roll-in")

Design choices
----------------------------------
the :code:`rolltable.resolve` method takes 5 arguments: 

1. the commodity shortcode (e.g. NG)
2. the forward name (one of F0..F6 or one of C1..C6)
3. the month (e.g. 1 for January)
4. the year (e.g. 2020)
5. one of 'roll-in' or 'roll-out' to disambiguate which contract is being resolved

.. note:: *Why not take a date in lieu of the 3rd and 4th argument?*
   Some indices pre-roll ahead of the benchmarks - the above approach forces the user to unambiguously specify which month the rolltable should resolve.  

.. note:: *What are Fx and Cx forwards?*
   F forwards are the contracts the index will hold in *x* months from today: the F1 is simply the contract that will be held in a month's time. 

Prior contract tables
----------------------------------
A contract's prior contract is the future contract expiring immediately the given contract. These prior contract may or may not be in a rolltable; as such, the :code:`F0` contract is not necessarily the prior contract of the :code:`F1` contract. The :code:`Priortable` object allows to resolve this contract easily. 
::

   >>> from rolltables.priortables import Priortable, BCOMRS
   
   >>> BCOMRS.resolve("CLX2020")
   'CLV2020'

Utils
-----------------------------------
Use the utility functions and classes makes your code cleaner
::

   >>> from rolltables import F
   
   >>> F(1) + 1
   'F2'

   >>> C(4) - 1
   'C3'

API Documentation 
-----------------------------------

Rolltable
***********************************

.. autoclass:: rolltables.Rolltable
    :members:

Priortable
***********************************

.. autoclass:: rolltables.Priortable
    :members:

