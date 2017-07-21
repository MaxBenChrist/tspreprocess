**Disclaimer: This package is WIP. Do not take any APIs for granted.**

============
tspreprocess
============

Time series can contain noise, be sampled under a non fitting rate or need to be compressed.
*tspreprocess* is a library of preprocessing tools for time series data to tackle such problems.

We are planning to add methods to do

* Denoising
* Compression
* Resampling
* ...

Our goal is to make this the most comprehensive time series preprocessing library.


Installation
============

Clone the repo, cd into it and install it with pip locally

.. code-block:: Python

    git clone https://github.com/MaxBenChrist/tspreprocess
    cd tspreprocess
    pip install -e .

You can run the test suite by

.. code-block:: Python

    python setup.py test


Relation to *tsfresh*
=====================

This package will based on the data formats from the python feature extraction pacakge *tsfresh*
(https://github.com/blue-yonder/tsfresh), allowing a seamless integration between both packages.