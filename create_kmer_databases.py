#!python3
import os,sys,logging
locationHaplotypingPackage = "../haplotyping"
if not locationHaplotypingPackage in sys.path: sys.path.insert(0, locationHaplotypingPackage)
import haplotyping.index

logging.basicConfig(format="%(asctime)s | %(name)s |  %(levelname)s: %(message)s", datefmt="%m-%d-%y %H:%M:%S")
logging.getLogger("haplotyping.index.database").setLevel(logging.DEBUG)
logging.getLogger("haplotyping.index.splits").setLevel(logging.DEBUG)
logging.getLogger("haplotyping.index.reads").setLevel(logging.DEBUG)
logging.getLogger("haplotyping.index.storage").setLevel(logging.DEBUG)

if len(sys.argv) == 6:
    
    directoryReadFiles = os.path.realpath(sys.argv[1])
    locationSortedList = os.path.realpath(sys.argv[2])
    locationOutputBase = os.path.realpath(sys.argv[3])
    threads = int(sys.argv[4])
    name  = sys.argv[5]
    
    k = haplotyping.index.Database.detectKmerSize(locationSortedList)
    (unpairedReadFiles, pairedReadFiles, allReadFiles) = haplotyping.index.Database.detectReadFiles(
                                                            directoryReadFiles)
    
    database = haplotyping.index.Database(k, name, 
                                           locationOutputBase, locationSortedList, 
                                           unpairedReadFiles, pairedReadFiles, 
                                           maximumProcesses=threads)
else:
    raise Exception("call: {} <directoryReadFiles> <locationSortedList> <locationOutputBase> <threads> <name>".format(
        sys.argv[0]))