#!/bin/sh
#$ -q gen4.q
#$ -N mgcp_mgmg
#$ -S /bin/sh
#$ -cwd
#$ -t 1-10
#$ -tc 4

. /etc/profile.d/modules.sh

# Disable production of core dump files
ulimit -c 0

echo ""
echo "***********************************************************************"
echo " Starting job:"
echo ""
echo "    Name:              "$JOB_NAME
echo "    ID:                "$JOB_ID
echo "    Hostname:          "$HOSTNAME
echo "    Working directory: "$SGE_O_WORKDIR
echo ""
echo "    Submitted using:   submit --array 1-10 -N mgcp_mgmg -i in/dimgce_mgmg_pes.in gen4.q psi4@master"
echo "***********************************************************************"

# cd into individual task directory
cd $SGE_O_WORKDIR/$SGE_TASK_ID

# Load the requested Psi4 module file
vulcan load psi4@master~ambit~chemps2~debug~pcmsolver~vectorization

export PSI_SCRATCH=$TMPDIR
export KMP_DUPLICATE_LIB_OK=TRUE

psi4 -n 4 -i in/dimgce_mgmg_pes.in -o output.dat

