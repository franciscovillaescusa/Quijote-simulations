#!/bin/bash

CAMB=/projects/QUIJOTE/Leander/CAMB-Jan2017/camb

module purge

echo Running CAMB ...
module load intel/19.1/64/19.1.1.217
$CAMB $1 | tee $2

