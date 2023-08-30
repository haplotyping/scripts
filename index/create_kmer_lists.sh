#/bin/bash

cd "$(dirname "$0")"
. config

for i in $(find "$LOCATION_KMERDATABASE" -type d); do 
    for f in "$i"/kmer.kmc.*; do
        if [ -e "$f" ] ;
        then
            if [ -e "$i/kmer.list.sorted.gz" ] ;
            then
                echo "SKIP $i"
            else
                echo "PROCESS $i"
                eval $KMCANALYSIS dump "$i/kmer.kmc" \
                "$i/kmer.list" -min "$MINIMUM_FREQ" -max "$MAXIMUM_FREQ" -rc
                sort --parallel="$THREADS" "$i/kmer.list" > "$i/kmer.list.sorted"
                pigz -f -p "$THREADS" "$i/kmer.list.sorted"
                rm "$i/kmer.list"
            fi
        fi
        break
    done
done
