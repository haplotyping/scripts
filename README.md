# Scripts 

Several scripts to prepare and process data

* **create_kmc_files.sh** : from the reads, create kmc files
* **create_kmer_lists.sh** : from the kmc-files, create sorted lists with k-mers

Make sure to configure at least the correct location of 
* readfiles
* k-mer databases
* temporary storage
* kmc_analysis binary

Additionally, number of threads, k-mer size and frequency range can be adjusted

Directories will be traversed recursively

The directory-structure used for the read-files will be duplicated to the k-mer database storage.
