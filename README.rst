|license|

Disclaimer: This package is WIP. Do not take any APIs for granted.

============
tspreprocess
============

Time series can contain noise, be sampled under a non fitting rate or need to be compressed.
*tspreprocess* is a library of preprocessing tools for time series data to tackle such problems.

It contains methods to do

* Denoising
* Compression
* Resampling


Goal
====

We want to make this the most comprehensive time series preprocessing library.


Installation
============

Use clone the repo, cd into it and install it with `pip install -e .`.

You can run tests by `python setup.py test`


Relation to *tsfresh*
=====================

This package will based on the APIs from *tsfresh* (https://github.com/blue-yonder/tsfresh), allowing a seamless
integration between both packages.