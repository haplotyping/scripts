#!python3
import os,sys,logging
locationHaplotypingPackage = "../../haplotyping"
if not locationHaplotypingPackage in sys.path: sys.path.insert(0, locationHaplotypingPackage)
import haplotyping.index

logging.basicConfig(format="%(asctime)s | %(name)s |  %(levelname)s: %(message)s", datefmt="%m-%d-%y %H:%M:%S")
logging.getLogger("haplotyping.index.database").setLevel(logging.DEBUG)
logging.getLogger("haplotyping.index.splits").setLevel(logging.DEBUG)

if len(sys.argv) == 4:
    
    locationSortedList = os.path.realpath(sys.argv[1])
    locationOutputBase = os.path.realpath(sys.argv[2])
    name  = sys.argv[3]
    
    k = haplotyping.index.Database.detectKmerSize(locationSortedList)  
    database = haplotyping.index.Database(k, name, locationOutputBase, locationSortedList, onlySplittingKmers=True)
else:
    raise Exception("call: {} <locationSortedList> <locationOutputBase> <name>".format(
        sys.argv[0]))
