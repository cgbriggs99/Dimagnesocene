#!/bin/sh
#$ -q gen4.q
#$ -N dimgcp_h4_opt
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
echo "    Submitted using:   submit -n 8 -N dimgcp_h4_opt -i in/magnesium/dimagnesocene_h4.in -o out/magnesium/dimagnesocene_h4.out gen4.q psi4@master"
echo "***********************************************************************"


# Load the requested Psi4 module file
vulcan load psi4@master~ambit~chemps2~debug~pcmsolver~vectorization

export PSI_SCRATCH=$TMPDIR
export KMP_DUPLICATE_LIB_OK=TRUE

psi4 -n 8 -i in/magnesium/dimagnesocene_h4.in -o out/magnesium/dimagnesocene_h4.out

