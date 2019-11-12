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

## Setting Up DVC

At the beginning, our repository is not set up for DVC.

    dvc init

This will create the initial files needed to use DVC.

We can add our source file to put it under DVC's control:

    dvc add data/sources/glove.6B.50d.dvc -f data/sources/glove.6B.50d.dvc

Now DVC will manage the file for us! We'll see why this is useful in a little big.

Commit the files DVC created to Git!

## Setting up Remotes

DVC can move files around for us. Input and output files can be very large, so we don't
want to commit them directly to Git - DVC lets us commit pointers to them, and push and
pull the files themselves to another server.

First, we need a DVC *remote*:

    dvc remote add piret s3://dvc-demo
    dvc remote modify piret profile piret-minio
    dvc remote modify piret endpointurl http://abyss.boisestate.edu:9000
    dvc config core.remote piret

This sets up a remote called `piret` to point to our internal S3 server, and makes it the
default.  Commit our DVC config file when we're done with this!

    git status
    git add .dvc/config
    git commit

One final piece needed - the credentials, so DVC knows how to access the server. We don't
commit credentials to Git.  Get the cedential info from e-mail, and save it in the file
`~/.aws/credentials` (on Windows, `C:\Users\MyUser\.aws\credentials`).

Then we can push:

    dvc push
    git push

> **Your turn:** `git pull` your repository, and then `dvc pull` - it will download our
data file!

## Wiring Up a Command

What if we want to use DVC to run our command?

    dvc run -f data/glove.6B.50d.dvc -o data/glove.6B.50d.netcdf \
        -d data/sources/glove.6B.zip -d prep-embedding.py \
        python prep-embedding.py --glove data/sources/glove.6B.zip \
            glove.6B.50d.txt data/glove.6B.50d.netcdf

This tells DVC about our command's inputs and outputs, and the command to run.
Note that we have to specify inputs and outputs twice: once to tell DVC where they
are, and once to tell our script where to put them.

It saves the definition in `data/glove.6B.50d.dvc`. Don't forget to commit!  This file
contains:

- inputs (names and checksums)
- outputs (names and checksums)
- command to run

Every time we run the command, it will delete the old output, run the command, and save
the new output.

**Let DVC run your code.** It's normal to run commands to test things, but once you have
it ready for The Real Run, use DVC to do the run.  That way the exact commands are recorded
in DVC.

DVC is like `make`: it knows how to produce outputs fronm inputs by running commands,
but it's smarter about looking for changes and also knows how to push and pull data
to servers.

> **Your turn**: `git pull` and `dvc pull`, then extract one of the other data files.

## Re-Running a Command

`dvc repro` re-runs a command:

    dvc repro data/glove.6B.50d.dvc

Right now, it says this stage is up to date.  Good!

## Running the Notebook

Notebooks are a little weird.  We're going to run the notebook to produce *another*
notebook as output using a tool called `papermill`.

    dvc run -f WordProjections.6B.50d.dvc -O WordProjections.6B.50d.ipynb \
        -d WordProjections.ipynb -d data/glove.6B.50d.dvc \
        papermill WordProjections.ipynb WordProjections.6B.50d.ipynb

Now we can look at the output notebook.  We specified `-O`, instead of `-o`, to tell
DVC to create the file but not take control of it. This way we can commit it to git,
and view the notebook in github. That is convenient.  Most output files we don't want
in `git`, but a few can be useful.

Now if we modify the notebook and run `dvc repro`, it will re-run the notebook!

We should remember to commit early and often.

## More Fun

- Notebook variants with Papermill
- What does this layout look like in a full repository?

## Quick Tricks

- after `git pull`, `dvc pull` (unless you have local changes! commit those first!).
- `dvc push` to send data.
- this is super useful for working with R2 for Big Jobs and other computers for working
  with the results of Big Jobs.
- `dvc install` will set up Git hooks to make some things more automatic.