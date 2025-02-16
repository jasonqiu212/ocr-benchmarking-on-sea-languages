# Running Scripts on the NUS SoC Compute Cluster

> [!TIP]
> For quick information, refer to this [Slurm Quick Start Guide](https://dochub.comp.nus.edu.sg/cf/guides/compute-cluster/slurm-quick) done by SoC.

1. Running Python code on the compute cluster using Slurm requires two files: A Unix shell script (`.sh`) and a Python script (`.py`). Refer to the `hello_world.sh` and `hello_world.py` files as an example.

2. If you are using any Python libraries (e.g., `jiwer` in `hello_world.py`), you must first create a virtual environment in the same directory as the scripts and install the necessary libraries. For instance:

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

3. Submit the shell script to Slurm.

```
sbatch hello_world.sh
```

4. You can monitor the Slurm job queue via `squeue`.

> [!TIP]
> `squeue --me` prints the job queues done by the current user.

5. When your batch job completes, Slurm writes its terminal output to the `slurm-<jobid>.out` file.
