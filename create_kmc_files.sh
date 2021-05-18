#/bin/bash

LOCATION_READFILES=data/readfiles
LOCATION_KMERDATABASE=data/kmer
LOCATION_TMP=tmp

THREADS=20
KMER_SIZE=31
MINIMUM_FREQ=1
MAXIMUM_FREQ=100000000

for i in $({ cd "$LOCATION_READFILES" && find . -type d; }); do 
    for f in "$LOCATION_READFILES"/"$i"/*.fastq.gz; do
        if [ -e "$f" ] ;
        then
            echo "$i"
            mkdir -p "$LOCATION_KMERDATABASE"/"$i"
            find "$LOCATION_READFILES"/"$i" -name *.fastq.gz > "$LOCATION_KMERDATABASE"/"$i/kmer.lst"
            kmc -k"$KMER_SIZE" -ci"$MINIMUM_FREQ" \
               -cx"$MAXIMUM_FREQ" -cs"$MAXIMUM_FREQ" -t"$THREADS" \
               @"$LOCATION_KMERDATABASE"/"$i/kmer.lst" "$LOCATION_KMERDATABASE"/"$i/kmer.kmc" tmp
            rm "$LOCATION_KMERDATABASE"/"$i/kmer.lst"
        fi
        break
    done
done