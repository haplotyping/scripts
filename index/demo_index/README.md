The reads provided in [demo_reads](../demo_reads/)
```
resource1/demo1/reads.fastq.gz
resource1/demo1/reads_R1_001.fastq.gz
resource1/demo1/reads_R2_001.fastq.gz
resource1/demo2/reads.fastq.gz
resource1/demo2/reads_R1_001.fastq.gz
resource1/demo2/reads_R2_001.fastq.gz
```
will result, after succesfully applying the provided scripts, in
* kmc files
  ```
  resource1/demo1/kmer.kmc.kmc_pre
  resource1/demo1/kmer.kmc.kmc_suf
  resource1/demo2/kmer.kmc.kmc_pre
  resource1/demo2/kmer.kmc.kmc_suf
  ```
 * sorted k-mer lists
  ```
  resource1/demo1/kmer.list.sorted.gz
  resource1/demo2/kmer.list.sorted.gz
  ```
 * k-mer databases
  ```
  resource1/demo1/kmer.data.h5
  resource1/demo2/kmer.data.h5
  ```
 * and logfiles
  ```
  resource1/demo1/kmer.data.log
  resource1/demo2/kmer.data.log
  ```
