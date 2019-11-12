# DVC Demo

## Pre-Meeting Setup

1. Clone this git repository:
2. Install the software specified in `environment.yml`:

        conda env create -f environment.yml

This step will install the following (along with dependencies):

- Python
- pandas
- xarray
- PyTables
- dvc
- docopt
- papermill
- Jupyter

## Initial Layout

THis repository works with embedding files.  The data is in `data`; I have
downloaded the Glove 6B file into `data/sources`.

Our little repository has a couple of steps:

1. Convert data into a more useful form
2. Analyze it in a notebook

We can add more steps if we want!

We can run the conversion process:

    python prep-embedding.py --glove data/sources/glove.6B.zip \
        glove.6B.50d.txt data/glove.6B.50d.netcdf

This will extract the 50d embedding, normalize it, and save it in an XArray-based
NetCDF file for easy loading later.

The `WordProjections.ipynb` notebook looks at one of these embeddings.

