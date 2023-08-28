#!/bin/csh
#$ -q gen4.q
#$ -S /bin/csh 
#$ -cwd

# Set User Variables
setenv wrkpath /home/vulcan/cgb31826/git/Dimagnesocene

# Set CFOUR Variables
module load cfour/2.0/parallel
setenv scratch $TMPDIR/$USER/$JOB_ID

# Found User-Defined Data 
setenv CFOUR_GENBAS $wrkpath/GENBAS

# Set MPI Variables
setenv OMP_NUM_THREADS 1
setenv NSLOTS `cat /proc/cpuinfo | grep processor | wc -l`

# Copy Job/Executable Data
cp $wrkpath/ZMAT $scratch/ZMAT
cp $CFOUR_GENBAS $scratch
cp $CFOUR_ECPDATA $scratch

echo " Running cfour/2.0/parallel on `hostname`"
echo " Running calculation...(`date`)"

cd $scratch
xcfour >& $wrkpath/output.dat
xja2fja
/opt/scripts/cfour2avogadro $wrkpath/output.dat

echo " Saving data and cleaning up..."
if (-e ZMATnew) cp -f ZMATnew $wrkpath/ZMATnew
find . -type f -size -75M | xargs tar czvf $wrkpath/Job_Data_${JOB_ID}.tgz --exclude 'I*' --exclude 'MOLDEN' --exclude 'rank*' --exclude 'basinfo.dat' --exclude 'ncpu' --exclude 'MOINTS' --exclude 'VPOUT' --exclude 'GAMLAM'

cd $wrkpath
rm -rf $scratch

echo " Job complete. (`date`)"
