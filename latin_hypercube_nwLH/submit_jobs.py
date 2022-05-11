import numpy as np
import sys,os

root  = '/mnt/ceph/users/fvillaescusa/Quijote/nwLH'
start = 1900
end   = 2000

# do a loop over the considered folders
for i in range(start,end):
    os.chdir('%s/%d'%(root,i))
    os.system('pwd')
    os.system('sbatch script.sh')
    
