# -*- coding: utf-8 -*-
# This file as well as the whole tspreprocess package are licenced under the MIT licence (see the LICENCE.txt)
# Maximilian Christ (maximilianchrist.com), 2017

from __future__ import absolute_import, division
import numpy as np
import pandas as pd
from pandas.testing import assert_frame_equal
from tspreprocess.compress.compress import compress
from unittest import TestCase


class CompressTestCase(TestCase):
    def setUp(self):
        cid = np.repeat([10, 500], 10)
        ckind = np.repeat(["a", "b", "a", "b"], 5)
        csort = [1, 2, 3, 4, 5,
                 6, 7, 8, 9, 10,
                 1, 2, 3, 4, 5,
                 6, 7, 8, 9, 10]
        cval = [11, 9, 67, 45, 30,
                58, 62, 19, 56, 29,
                0, 27, 36, 43, 33,
                2, 24, 71, 41, 28]
        self.df = pd.DataFrame({"id": cid, "kind": ckind, "sort": csort, "val": cval})
        self.col_naming = {"column_id": "id", "column_kind": "kind", "column_sort": "sort", "column_value": "val"}

        # gives the following DataFrame
        """
             id kind  sort  val
        0    10    a     1   11
        1    10    a     2    9
        2    10    a     3   67
        3    10    a     4   45
        4    10    a     5   30
        5    10    b     6   58
        6    10    b     7   62
        7    10    b     8   19
        8    10    b     9   56
        9    10    b    10   29
        10  500    a     1    0
        11  500    a     2   27
        12  500    a     3   36
        13  500    a     4   43
        14  500    a     5   33
        15  500    b     6    2
        16  500    b     7   24
        17  500    b     8   71
        18  500    b     9   41
        19  500    b    10   28
        """

    def test_compress_max(self):
        dd = compress(self.df,
                      compression_functions={"maximum": None},
                      interval_length=2,
                      **self.col_naming)

        expected_dd = pd.DataFrame({"id": ["10"] * 3 + ["500"] * 3,
                                    "sort": ["bin_0", "bin_1", "bin_2"] * 2,
                                    "a_maximum": [11., 67., 30., 27., 43., 33.],
                                    "b_maximum": [62., 56., 29., 24., 71., 28.]})

        expected_dd = expected_dd[dd.columns]

        expected_dd.sort_values(by=["id", "sort"], inplace=True)
        assert_frame_equal(expected_dd, dd)

    def test_compress_min(self):
        dd = compress(self.df,
                      compression_functions={"minimum": None},
                      interval_length=2,
                      **self.col_naming)

        expected_dd = pd.DataFrame({"id": ["10"] * 3 + ["500"] * 3,
                                    "sort": ["bin_0", "bin_1", "bin_2"] * 2,
                                    "a_minimum": [9., 45., 30., 0., 36., 33.],
                                    "b_minimum": [58., 19., 29., 2., 41., 28.]})

        expected_dd = expected_dd[dd.columns]
        expected_dd.sort_values(by=["id", "sort"], inplace=True)
        assert_frame_equal(expected_dd, dd)


    # todo: we need tests for the other tsfresh formats, maybe just restructure the DF from above
