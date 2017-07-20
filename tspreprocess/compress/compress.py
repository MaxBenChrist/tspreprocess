# -*- coding: utf-8 -*-
# This file as well as the whole tsfresh package are licenced under the MIT licence (see the LICENCE.txt)
# Maximilian Christ (maximilianchrist.com), 2017

from __future__ import absolute_import, division
import numpy as np
import pandas as pd
from tsfresh import extract_features
from tsfresh.utilities.dataframe_functions import normalize_input_to_internal_representation
import six


def compress(df, compression_functions, interval_length, column_id, column_sort, column_kind, column_value):
    """
    Compresses the time series

    """

    dd = normalize_input_to_internal_representation(df, column_id, column_sort, column_kind, column_value)[0]

    def create_bins(x):
        return np.repeat(np.arange(np.ceil(len(x)/interval_length)), interval_length)[:len(x)]

    for k, df_k in six.iteritems(dd):
        df_k[column_id] = df_k[column_id].apply(str)  + "_bin_" + \
                          df_k.groupby(column_id)[column_value].transform(create_bins).apply(str)
        dd[k] = df_k

    dd = extract_features(dd,
                          column_id=column_id,
                          column_value=column_value,
                          default_fc_parameters=compression_functions)

    dd.columns = [x.replace("__", "_") for x in dd.columns]
    dd.reset_index(drop=False, inplace=True)

    ids = dd[column_id].str.split("_bin_").apply(lambda x: x[0])
    bin_number = dd["id"].str.split("_bin_").apply(lambda x: x[1])

    dd[column_id] = ids
    dd[column_sort] = "bin_" + bin_number

    return dd.sort_values(by=[column_id, column_sort])


def compress_SCADAlike(df, intervall_lenght, column_id, column_sort, column_kind, column_value):
    """
    Performs a SCADA like compression

    """
    return compress(df=df,
                    compression_functions=["min", "max", "mean", "var"],
                    intervall_lenght=intervall_lenght,
                    column_id=column_id, column_sort=column_sort, column_kind=column_kind, column_value=column_value)

