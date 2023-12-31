#!/bin/sh
#$ -q gen4.q
#$ -N dimgcp-_d5
#$ -S /bin/sh
#$ -cwd

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
echo "    Submitted using:   submit -n 8 -N dimgcp-_d5 -i in/magnesium/dimagnesocene-_d5.in -o out/magnesium/dimagnesocene-_d5.out gen4.q psi4@master"
echo "***********************************************************************"


# Load the requested Psi4 module file
vulcan load psi4@master~ambit~chemps2~debug~pcmsolver~vectorization

export PSI_SCRATCH=$TMPDIR
export KMP_DUPLICATE_LIB_OK=TRUE

psi4 -n 8 -i in/magnesium/dimagnesocene-_d5.in -o out/magnesium/dimagnesocene-_d5.out

