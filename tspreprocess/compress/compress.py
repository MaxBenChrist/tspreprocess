# -*- coding: utf-8 -*-
# This file as well as the whole tspreprocess package are licenced under the MIT licence (see the LICENCE.txt)
# Maximilian Christ (maximilianchrist.com), 2017

from __future__ import absolute_import, division
import numpy as np
from tsfresh import extract_features
from tsfresh.utilities.dataframe_functions import _normalize_input_to_internal_representation


# todo: maybe compress is not the right term? because we are losing information
# todo: add support for generic numpy methods as aggregation function
# todo: add support for custom aggregation functions
def compress(ts, compression_functions, interval_length, column_id, column_sort, column_kind, column_value):
    """
    This method compresses time series by applying a compression function on bins. Then the values of the compression
    function over the bins are returned as a new, compressed time series.

    This decreasing the memory footprint of the time series. E.g. by applying a singular compression function on chunks
    of size 10, the time series is compressed by a factor 10.

    It is also possible to use multiple compression functions.

    The time series container ts must be in one of the formats that are supported by the tsfresh package.

    :param ts: The pandas.DataFrame with the time series to compute the features for, or a dictionary of pandas.DataFrames.
    :type ts: pandas.DataFrame or dict

    :param compression_functions: mapping from feature calculator names to parameters. See tsfresh documentation
    :type compression_functions: dict

    :param interval_length: the length of each bin to which the aggregation functions are applied
    :type interval_length: int

    :param column_id: The name of the id column to group by.
    :type column_id: str

    :param column_sort: The name of the sort column.
    :type column_sort: str

    :param column_kind: The name of the column keeping record on the kind of the value.
    :type column_kind: str

    :param column_value: The name for the column keeping the value itself.
    :type column_value: str
    """

    dd, column_id, column_kind, column_value = \
        _normalize_input_to_internal_representation(ts, column_id, column_sort, column_kind, column_value)

    def create_bins(v):
        n_bins = np.ceil(len(v) / interval_length)
        return np.repeat(np.arange(n_bins), interval_length)[:len(v)]

    dd[column_id] = dd[column_id].apply(str) + "_bin_" + \
                    dd.groupby([column_id, column_kind])[column_value].transform(create_bins).apply(str)

    dd = extract_features(dd,
                          column_id=column_id,
                          column_value=column_value,
                          column_kind=column_kind,
                          default_fc_parameters=compression_functions)

    dd.columns = [x.replace("__", "_") for x in dd.columns]
    dd.columns = [x.replace("feature", "map") for x in dd.columns]
    dd.reset_index(drop=False, inplace=True)

    ids = dd[column_id].str.split("_bin_").apply(lambda s: s[0])
    bin_number = dd["id"].str.split("_bin_").apply(lambda s: eval(s[1]))

    dd[column_id] = ids
    dd["bin"] =  bin_number

    return dd.sort_values(by=[column_id, "bin"])


# todo: add references to SCADA sources
# add unit tests for this method
def compress_SCADA_like(ts, interval_length, column_id, column_sort, column_kind, column_value):
    """
    Takes a tsfresh compatible time series container and performs compression by calculating max, min, mean and
    variance of each time series.

    This is a common compression technique for SCADA (Supervisory Control and Data Acquisition) systems, deployed in
    Industrial environments.

    """
    return compress(ts=ts,
                    compression_functions={"minimum": None, "maximum": None, "mean": None, "variance": None},
                    intervall_lenght=interval_length,
                    column_id=column_id, column_sort=column_sort, column_kind=column_kind, column_value=column_value)


def make_SAX():

    pass