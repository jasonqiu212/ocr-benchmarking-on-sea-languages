# Running Scripts on the NUS SoC Compute Cluster

> [!TIP]
> For quick information, refer to this [Slurm Quick Start Guide](https://dochub.comp.nus.edu.sg/cf/guides/compute-cluster/slurm-quick) done by SoC.

1. To run Python code on the compute cluster using Slurm, create a Unix shell script (`.sh`) and a Python script (`.py`). Refer to the `hello_world.sh` and `hello_world.py` files as an example.

> [!NOTE]
> If you are using any Python libraries, I recommend using [`venv`](#using-venv) or [Conda](#using-conda).

2. Submit the shell script to Slurm.

```
sbatch hello_world.sh
```

3. You can monitor the Slurm job queue via `squeue`.

> [!TIP] > `squeue --me` prints the job queues done by the current user.

4. When your batch job completes, Slurm writes its terminal output to the `slurm-<jobid>.out` file.

## Using `venv`

> [`venv`](https://docs.python.org/3/library/venv.html) creates isolated environments to manage Python packages.

To run scripts using `venv`, you must first create a virtual environment in the same directory as the scripts and install the necessary packages. For instance:

```
python3 -m venv sample
source sample/bin/activate
pip install jiwer
deactivate
```

Your shell script should activate the virtual environment before running the Python script. For instance:

```
source sample/bin/activate
python3 hello_world.py
deactivate
```

> [!NOTE]
> To use `source` in the shell script, you need to change the `#!/bin/sh` to `#!/bin/bash`, which is different from what the SoC Quick Start Guide says. This specifies that the script should be executed using bash (the Bourne Again shell), which is an enhanced version of sh (the original Bourne shell).

### `venv` Scripts and Necessary Packages

- `hello_world`: `jiwer`
- `easyocr_*`: `easyocr`

## Using Conda

> [Miniconda](https://www.anaconda.com/docs/getting-started/miniconda/main) is a miniature installation of Conda that creates isolated environments to manage Python packages and system libraries.

To run scripts using Conda, you must first install Miniconda and create a new Conda environment and install the necessary packages. For instance:

```
# Assuming Miniconda is installed in the root directory
source ~/miniconda3/bin/activate
conda create --name sample
conda activate sample
conda install -c conda-forge pytesseract tesseract
conda deactivate
```

Your shell script should activate the Conda environment before running the Python script. For instance:

```
source ~/miniconda3/bin/activate
conda activate sample
python3 tesseract_en.py
conda deactivate
```

### Conda Scripts and Necessary Libraries

- `tesseract_*`: `pytesseract`, `tesseract`
