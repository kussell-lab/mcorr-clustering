#!/bin/bash
# This script demonstrates how you would run mcorr-pair-sync on a larger dataset

##inputs
msa=MSA_HI_MASTER_GAPFILTERED
strainlist=sra_list.txt

##Step 1: divide your MSA into chunks (here we are doing 2 chunks)
chunkMSA ${msa} ${strainlist} 2 --chunk-folder="chunks"

##Step 2: run mcorr-pair-sync to calculate distances for a subset of the distance matrix
## this is the step you would parallelize over multiple jobs on an HPC
mkdir -p mps_out
for i in {0..1}
do
  chunk=chunks/MSA_chunk${i}
  mcorr-pair-sync ${msa} ${chunk} mps_out/mps_${i}_out.csv  --max-corr-length=3
done

##Step 3: collect mcorr-pair-sync outputs
mcorr-dm-chunks mps_out ${strainlist} mps_dm

##Step 4: cluster sequences
clusterSequences mps_dm.npy ${strainlist} "mps_results" --percentile=25 --min_size=2

##Step 5: Write XMFAs for the core and flexible genes of each cluster
clusterSplit MSA_CORE mps_out cluster_list --FLEX_MSA=MSA_FLEX