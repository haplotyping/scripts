#/bin/bash

LOCATION_READFILES=data/reads/full
LOCATION_KMERDATABASE=data/index/full
PYTHONBINARY=python
PYTHONSCRIPT=create_kmer_databases.py
THREADS=20

for i in $({ cd "$LOCATION_KMERDATABASE" && find . -type d; }); do 
    for f in "$LOCATION_KMERDATABASE"/"$i"/kmer.list.sorted.gz; do
        if [ -e "$f" ] ;
        then
            if [ -e "$LOCATION_KMERDATABASE"/"$i/kmer.data.h5.lock" ] ;
            then
                rm "$LOCATION_KMERDATABASE"/"$i/kmer.data.h5.lock"
                if [ -e "$LOCATION_KMERDATABASE"/"$i/kmer.data.h5" ] ;
                then
                    rm "$LOCATION_KMERDATABASE"/"$i/kmer.data.h5"
                fi
            fi
            if [ -e "$LOCATION_KMERDATABASE"/"$i/kmer.data.h5" ] ;
            then
                echo "SKIP $i"
            else
                echo "PROCESS $i"
                touch "$LOCATION_KMERDATABASE"/"$i/kmer.data.h5.lock"
                eval $PYTHONBINARY $PYTHONSCRIPT "\"${LOCATION_READFILES}/${i}\"" "\"${LOCATION_KMERDATABASE}/${i}/kmer.list.sorted.gz\"" "\"${LOCATION_KMERDATABASE}/${i}/kmer.data\"" "${THREADS}" "\"${i}\""
                rm "$LOCATION_KMERDATABASE"/"$i/kmer.data.h5.lock"
            fi
        fi
    done
done