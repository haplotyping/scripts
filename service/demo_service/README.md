The files provided in [demo_data](../demo_data/)
```
pedigree.xlsx
data_resource1.xlsx
data_resource2.xlsx
data_resource2.csv.gz
```
will here result, after succesfully applying the provided scripts, in a sqlite database with additional files for markers and k-mer data
```
db.sqlite
identifiers.json
kmer/resource1/demo1/kmer.kmc.kmc_pre
kmer/resource1/demo1/kmer.kmc.kmc_suf
kmer/resource1/demo1/kmer.data.h5
kmer/resource1/demo2/kmer.kmc.kmc_pre
kmer/resource1/demo2/kmer.kmc.kmc_suf
kmer/resource1/demo2/kmer.data.h5
marker/markers_data_resource2_5_0.h5
```
Here the k-mer databases originate from applying the [index](../index/) scripts.

An additional created file `identifiers.json` contains assigned identifiers to guarantee assigning the same identifiers after rerunning the scripts.
