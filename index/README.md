# Create splitting k-mer databases

Several scripts to prepare and process data

* **create_kmc_files.sh** : from the reads, create kmc files
* **create_kmer_lists.sh** : from the kmc-files, create sorted lists with k-mers
* **create_kmer_databases.sh** : from the reads and sorted lists with k-mers, create databases

To make better use of all available cores, the simultanuous construction of multiple databases can be split 
into two separate steps:

* **create_kmer_databases_step1.sh** : in this step, for each database only a single core can be used. However, when creating multiple databases, multiple processes can run parallel
* **create_kmer_databases_step2.sh** : in this step for each database the use of multiple cores is possible. Multiple databases will be created sequential

First create a file `config` 

```
LOCATION_READFILES=demo_reads
LOCATION_KMERDATABASE=demo_index
LOCATION_TMP=tmp

KMC=kmc
KMCANALYSIS=../../kmc_analysis/bin/kmc_analysis
PYTHONBINARY=python

THREADS=10
KMER_SIZE=31
MINIMUM_FREQ=2
MAXIMUM_FREQ=65535
MAXIMUM_MEMORY=10737418240
```

Check and/or adjust the correct location of 
* readfiles
* k-mer databases
* temporary storage
* binaries [kmc](https://github.com/refresh-bio/KMC) and [kmc_analysis](https://github.com/haplotyping/kmc_analysis)

Additionally, number of threads, k-mer size, frequency range and maximum memory usage can be adjusted

Directories will be traversed recursively

The directory-structure used for the read-files will be duplicated to the k-mer database storage. 
