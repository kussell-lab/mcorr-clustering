#!/usr/bin/env python3
import time
import argparse
import os
from . import clusterSequences as cS
"""
this commandline program runs the mcorr-clustering program with mcorr-pair in steps
"""

def mkdir_p(dir):
    'make a directory if doesnt exist'
    if not os.path.exists(dir):
        os.mkdir(dir)
def main():
    parser = argparse.ArgumentParser(description="Takes the output of mcorr-pair, clusters sequences,\
                                                    and breaks clusters into core and flexible genomes")
    parser.add_argument("working_dir", help="the working space and output directory")
    parser.add_argument("master_msa", type=str, help="master msa file for all strain sequences")
    parser.add_argument("strain_list", type=str, help="list of strains")
    parser.add_argument("--percentile", type=float, default=25, help="cutoff percentile of pairwise distances to use for making flat clusters (Default: 25)")
    parser.add_argument("--min_size", type=int, default=2, help="minimum number of strains in a cluster")
    parser.add_argument("--outdir", type=str, default="mcp_out", help="output directory")
    ##define commandline args as variables
    args = parser.parse_args()
    wrkdir = args.working_dir
    percentile = args.percentile
    msa = args.master_msa
    outdir = args.outdir
    min_size = args.min_size
    strains = args.strain_list



    start_time = time.time()

    os.chdir(wrkdir)

    ##make the output directory
    mkdir_p(outdir)

    #Step 1: run mcorr-pair
    print("running mcorr-pair ...")
    mcp_out = os.path.join(wrkdir, outdir, "mcp_out.csv")
    os.system("mcorr-pair %s %s --max-corr-length=3" %(msa, mcp_out))

    #Step 2: take mcorr-pair output and translate to distance matrix and a list of strains
    print("converting mcorr-pair to matrix ...")
    os.system("mcorr-dm %s distancematrix" % mcp_out)

    #Step 3: take the distance matrix and list of names
    print("clustering sequences ...")
    cS.clusterSequences(strains, str(percentile), str(min_size))

    #Step 4: divide the core and flexible genome XMFA into XMFAs for each cluster
    print("writing cluster MSA files ...")
    os.system("ClusterSplit MSA_CORE %s cluster_list --FLEX_MSA=MSA_FLEX" % outdir)
    print("Done clustering and writing cluster XMFA files")
    print("Total run time: %s minutes" % str((time.time() - start_time)/60))

if __name__ == "__main__":
    main()