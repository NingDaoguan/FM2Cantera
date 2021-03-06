"""
Zhen Lu 2017/07/19 <albert.lz07@gmail.com>

Sample points from the flamelet solution of chi_st. Z is get with the
beta-distribution.
"""

import glob
import numpy as np
import matplotlib.pyplot as plt

# mean of Z
Z_mean = [0.304,]
# var defined as var Z / (Z*(1-Z)), varies from 0 to 1
Z_var = [0.5,]
# the number of points
N_p = 100

fuel_name   = 'H2'
folder_name = 'tables_{0}/'.format(fuel_name)
dest_dir    = 'samples_{0}/'.format(fuel_name)
dict_file   = 'speciestranslated_{0}'.format(fuel_name)
table_pre   = 'Table_'
file_end    = '.csv'

compositions = []
with open(dict_file) as f:
    for line in f:
        compositions.append(line[:line.find('\t')])
compositions.append('T')
compositions.append('chi')

for table in glob.glob('{0}{1}*{2}'.format(folder_name,table_pre,file_end)): 

    data = np.genfromtxt(table,delimiter=',',names=True)
    chist = table[len(folder_name)+len(table_pre):table.find(file_end)]

    for mean in Z_mean:
        for var in np.arange(0.1,1.,0.1):

            alpha = mean*(1./var-1.)
            beta  = (1-mean)*(1./var-1.)

            Z = np.random.beta(alpha,beta,N_p)

            samples = np.zeros((N_p,len(compositions)))

            for i, sp in enumerate(compositions):
                samples[:,i] = np.interp(Z,data['Z'],data[sp])
            
            file_name = 'samples_ave{0:.3f}_var{1:.3f}_chi{2}.dat'             \
                        .format(mean,var,chist)

            np.savetxt('{0}{1}'.format(dest_dir,file_name),samples,fmt='%12.5f')

            # output a list for the FORTRAN
            with open('{0}input'.format(dest_dir),'w') as f:
                f.write(file_name+'\n')
                f.write('{0:12.5f}{1:12.5f}{2:12.5f}'
                        .format(mean,var,float(chist)))
