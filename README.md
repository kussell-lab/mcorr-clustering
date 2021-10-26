# mcorr-clustering
This repository contains everything needed to do 
hierarchical clustering using mcorr. It takes in gap-filtered XMFA files generated
from our [ReferenceAlignmentGenerator](https://github.com/kussell-lab/ReferenceAlignmentGenerator),
clusters them using average linkage ([UPGMA](https://en.wikipedia.org/wiki/UPGMA)) using synonymous diversity 
as the distance metric and outputs pairwise distances, a sequence tree, and XMFA files for the core and accessory genes
of each sequence cluster.

# Installation

For basic usage (hierarchical clustering of a small dataset ~100-5000 whole genome sequences) clone this repository and
install the program clusterWrite via pip:

`pip install ~/go/src/github.com/kussell-lab/mcorr-clustering/clusterWriteXMFA`

you need to then install the following in-house developed programs found in this repo:

* `go get -u github.com/kussell-lab/mcorr-clustering/mcorr-pair`
* `go get -u github.com/kussell-lab/mcorr-clustering/mcorr-dm`
* `go get -u github.com/kussell-lab/mcorr-clustering/ClusterSplit`

For doing hierarchical clustering of large datasets ~20,000 whole genome sequences, you can install all the CLI programs
needed from this repo via the `go get` command, with the exception of the program `clusterSequences`, which can also be installed
via pip:

`pip install ~/go/src/github.com/kussell-lab/mcorr-clustering/clusterSequences`

# Usage

### Small datasets (<5,000 sequences)

Datasets with <5000 sequences can be run in several hours using `clusterWrite`. You can input `clusterWrite --help`
into your terminal to see the inputs. This makes flat clusters based on the pairwise distance between sequences,
and you can change the cutoff percentile (which is the percentile of all the distances) at which the tree is cut.
You can also change the minimum number of strains for a cluster to be included.

### large datasets (~20,000 sequences)

For large datasets, you can cluster these sequences in several steps:

(1) Use `ChunkMSA` to divide up your XMFA file into several chunks

(2) Use `mcorr-pair-sync` to measure a subset of all of the pairwise distances necessary for the final
distance matrix. Here, you can run these jobs in parallel on an HPC to speed up the process.

(3) Once your parallelized jobs are completed, you can collect the results into a single distance matrix using
`mcorr-dm-chunks`.

(4) You can then run `clusterSequences` to cluster the sequences and `ClusterSplit` to split up the original XMFA
into XMFA files for each sequence cluster.

# Examples

See the subdirectory "hinfluenzae_example" to run both of the described examples.

### clusterWrite example
For an example of how to run `clusterWrite`, run the clusterWrite_example.sh script.
This should only take a few seconds to run on a standard PC.

### Example using mcorr-pair-sync
If you're interested in clustering and writing XMFA files for collections of 10,000 to 30,000 sequences, you
can parallelize `mcorr-pair-sync` over an HPC. An example workflow is given in the script mcorrpairsync_example.sh.
Step 2 is what would be run as parallel jobs on an HPC.
