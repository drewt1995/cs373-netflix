#!/usr/bin/envalue python3

# -------------------------------
# projects/Netflix/TestNetflix.py
# Copyright (C) 2016
# Glenn P. Downing
# -------------------------------

# https://docs.python.org/3.4/reference/simple_stmts.html#grammar-token-assert_stmt

# -------
# imports
# -------

from io import StringIO
from unittest import main, TestCase

#from Netflix import 

# -----------
# TestNetflix
# -----------


class TestNetflix (TestCase):
    # ----
    # function_name
    # ----

    def test_function_1(self):
        self.assertEqual(1,  1)

# ----
# main
# ----

if __name__ == "__main__":
    main()

""" #pragma: no cover
% coverage3 run --branch TestNetFlix.py >  TestNetflix.out 2>&1



% coverage3 report -m                   >> TestNetflix.out

"""
