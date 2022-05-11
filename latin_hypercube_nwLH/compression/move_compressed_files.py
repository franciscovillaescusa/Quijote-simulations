import numpy as np
import sys,os

for i in range(1000,1999):
    os.system('mv %d/* ../%d/'%(i,i))
