#/bin/bash

#==============================================
# SETTINGS
#==============================================

LOCATION_READFILES=data/reads/full
LOCATION_KMERDATABASE=data/index/full
PYTHONBINARY=python
PYTHONSCRIPT=create_kmer_databases_step1.py
THREADS=20

#==============================================
# SCRIPT
#==============================================

locations=()
for i in $({ cd "$LOCATION_KMERDATABASE" && find . -type d; }); do 
    for f in "$LOCATION_KMERDATABASE"/"$i"/kmer.list.sorted.gz; do
        if [ -e "$f" ] ;
        then
            if [ -e "$LOCATION_KMERDATABASE"/"$i/kmer.data.step1.h5.lock" ] ;
            then
                rm "$LOCATION_KMERDATABASE"/"$i/kmer.data.step1.h5.lock"
                if [ -e "$LOCATION_KMERDATABASE"/"$i/kmer.data.step1.h5" ] ;
                then
                    rm "$LOCATION_KMERDATABASE"/"$i/kmer.data.step1.h5"
                fi
            fi
            if [ -e "$LOCATION_KMERDATABASE"/"$i/kmer.data.step1.h5" ] ;
            then
                echo "SKIP $i"
            else
                echo "QUEUE $i"
                locations+=($i)
                touch "$LOCATION_KMERDATABASE"/"$i/kmer.data.step1.h5.lock"
            fi
        fi
    done
done

create_kmer_databases_step1 () {
    if [ -e "$4"/"$1/kmer.data.step1.h5.lock" ] ;
    then
        echo "Process $1"
        eval $2 $3 "\"$4/$1/kmer.list.sorted.gz\"" "\"$4/$1/kmer.data.step1\"" "\"${1}\""
        rm "$4"/"$1/kmer.data.step1.h5.lock"
    else
        echo "Problem processing $1"
    fi
}
export -f create_kmer_databases_step1

if [ ${#locations[@]} -eq 0 ];
then
    echo "Nothing to do..."
else
    parallel -j "${THREADS}" create_kmer_databases_step1 {} "${PYTHONBINARY}" "${PYTHONSCRIPT}" "$LOCATION_KMERDATABASE" ::: "${locations[@]}"
fi
