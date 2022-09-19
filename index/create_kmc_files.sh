#/bin/bash

LOCATION_READFILES=data/reads
LOCATION_KMERDATABASE=data/index
LOCATION_TMP=tmp

KMC=kmc

THREADS=20
KMER_SIZE=31
MINIMUM_FREQ=2
MAXIMUM_FREQ=65535

mkdir -p "$LOCATION_TMP"

for i in $({ cd "$LOCATION_READFILES" && find . -type d; }); do 
    for f in "$LOCATION_READFILES"/"$i"/*.fastq.gz; do
        if [ -e "$f" ] ;
        then
            mkdir -p "$LOCATION_KMERDATABASE"/"$i"
            if [ -e "$LOCATION_KMERDATABASE"/"$i/kmer.kmc.kmc_suf" ] ;
            then
                echo "SKIP $i"
            else
                echo "PROCESS $i"
                find "$LOCATION_READFILES"/"$i" -name *.fastq.gz > "$LOCATION_KMERDATABASE"/"$i/kmer.lst"
                eval $KMC -k"$KMER_SIZE" -ci"$MINIMUM_FREQ" \
                   -cs"$MAXIMUM_FREQ" -t"$THREADS" \
                   @"$LOCATION_KMERDATABASE"/"$i/kmer.lst" "$LOCATION_KMERDATABASE"/"$i/kmer.kmc" "$LOCATION_TMP"
                rm "$LOCATION_KMERDATABASE"/"$i/kmer.lst"
            fi
        fi
        break
    done
done
