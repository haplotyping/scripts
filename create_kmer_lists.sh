#/bin/bash

LOCATION_KMERDATABASE=data/kmer

THREADS=20
MINIMUM_FREQ=2
MAXIMUM_FREQ=100000000

for i in $(find "$LOCATION_KMERDATABASE" -type d); do 
    for f in "$i"/kmer.kmc.*; do
        if [ -e "$f" ] ;
        then
            echo "$i"
            ../kmc_analysis/bin/kmc_analysis dump "$i/kmer.kmc" \
		"$i/kmer.list" -min "$MINIMUM_FREQ" -max "$MAXIMUM_FREQ" -rc
            sort --parallel="$THREADS" "$i/kmer.list" > "$i/kmer.list.sorted"
            gzip -f "$i/kmer.list.sorted"
            rm "$i/kmer.list"
        fi
        break
    done
done