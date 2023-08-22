#!/bin/bash

module load psi4/master

psi4 -i in/dimgce_pes/dimgce_pes-`$SGE_TASK_ID`.in -o out/dimgce_pes/dimgce_pes-`$SGE_TASK_ID`.out
