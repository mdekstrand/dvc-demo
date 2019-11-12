"""
Prepare an embedding file for subsequent analysis.

Usage:
    prepare-embedding.py --glove ZIPFILE NAME OUTFILE
"""

from docopt import docopt

import sys
import csv

import zipfile

import pandas as pd
import numpy as np
import xarray as xa


def msg(msg, *args):
    "Print a status message"
    print(msg.format(*args), file=sys.stderr)


def import_glove(path, name):
    with zipfile.ZipFile(path) as zf:
        with zf.open(name) as gfile:
            msg('reading {} from zip file {}', name, path)
            wvs = pd.read_table(gfile, sep=' ', header=None, quoting=csv.QUOTE_NONE)
            msg('read {} words from {}:{}', len(wvs), path, name)

    # The first column is the word
    wvs.rename(columns={0: 'word'}, inplace=True)
    wvs.set_index('word', inplace=True)
    wvs.name = name
    
    # Convert to xarray
    return xa.DataArray(wvs, dims=['word', 'dim'])


def normalize_embedding(words):
    "Normalize an embedding to unit vectors."
    msg('normalizing word embeddings')
    norms = np.linalg.norm(words, axis=1)
    return (words.T / norms).T


def write_embedding(file, words):
    msg('writing words to {}', file)
    words.to_netcdf(file, encoding={words.name: {'zlib': True}})


if __name__ == '__main__':
    opts = docopt(__doc__)
    outfile = opts['OUTFILE']
    
    if opts['--glove']:
        zip_path = opts['ZIPFILE']
        zip_name = opts['NAME']
        words = import_glove(zip_path, zip_name)
    else:
        raise NotImplementedError('unknown import mode')

    words = normalize_embedding(words)
    write_embedding(outfile, words)