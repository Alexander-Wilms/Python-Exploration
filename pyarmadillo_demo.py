"""
Demo for PyArmadillo, which is much easier to use in the context of linear algebra than NumPy

https://pyarma.sourceforge.io/
"""

import pyarma as pa

A = pa.eye(6, 6)
b = pa.randu(6, 1)
A.print("A:")
b.print("b:")
c = A * b
c.print("c:")
