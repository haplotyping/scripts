#/bin/bash

cd "$(dirname "$0")"
. config

mkdir -p "$LOCATION_TMP"

for i in $({ cd "$LOCATION_READFILES" && find . -type d; }); do 
    for f in "$LOCATION_READFILES"/"$i"/*; do
    	if [[ ${f} =~ .*\.fastq\.gz ]] || [[ ${f} =~ .*\.fq\.gz ]] ;
    	then
        	if [ -e "$f" ] ;
        	then
         	   mkdir -p "$LOCATION_KMERDATABASE"/"$i"
            	if [ -e "$LOCATION_KMERDATABASE"/"$i/kmer.kmc.kmc_suf" ] ;
	            then	
    	            echo "SKIP $i"
        	    else
            	    echo "PROCESS $i"
                	find "$LOCATION_READFILES"/"$i" -regextype egrep -regex ".*(\.fastq\.gz|\.fq\.gz)" > "$LOCATION_KMERDATABASE"/"$i/kmer.lst"
	                eval $KMC -k"$KMER_SIZE" -ci"$MINIMUM_FREQ" \
    	               -cs"$MAXIMUM_FREQ" -t"$THREADS" \
        	           @"$LOCATION_KMERDATABASE"/"$i/kmer.lst" "$LOCATION_KMERDATABASE"/"$i/kmer.kmc" "$LOCATION_TMP"
            	    rm "$LOCATION_KMERDATABASE"/"$i/kmer.lst"
	            fi
	        fi
        fi
        break
    done
done
