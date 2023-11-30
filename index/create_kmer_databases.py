#!python3
import os,sys,logging
import importlib.util

#use spawn, also on linux
import multiprocessing as mp
if __name__ == "__main__":
    mp.set_start_method("spawn")

#fallback to local version
if importlib.util.find_spec("haplotyping")==None:
    print("TRYING TO USE LOCAL VERSION OF HAPLOTYPING PACKAGE")
    locationHaplotypingPackage = "../../haplotyping"
    if not locationHaplotypingPackage in sys.path: sys.path.insert(0, locationHaplotypingPackage)
#now, import haplotyping software
import haplotyping.index

if len(sys.argv) == 8:
    directoryReadFiles = os.path.realpath(sys.argv[1])
    locationSortedList = os.path.realpath(sys.argv[2])
    locationOutputBase = os.path.realpath(sys.argv[3])
    threads = int(sys.argv[4])
    name  = sys.argv[5]
    memory  = int(sys.argv[6])
    indexType = sys.argv[7]
    debug = False
    keepTemporaryFiles = False
    
    logging.basicConfig(format="%(asctime)s | %(name)s |  %(levelname)s: %(message)s", datefmt="%m-%d-%y %H:%M:%S",
                   handlers=[logging.FileHandler(locationOutputBase+".log", mode="w"), logging.StreamHandler()])
    logging.getLogger("haplotyping.index.database").setLevel(logging.DEBUG)
    logging.getLogger("haplotyping.index.splits").setLevel(logging.DEBUG)
    logging.getLogger("haplotyping.index.connections").setLevel(logging.DEBUG)
    logging.getLogger("haplotyping.index.storage").setLevel(logging.DEBUG)
    logging.getLogger("haplotyping.index.storage.worker.automaton").setLevel(logging.DEBUG)
    logging.getLogger("haplotyping.index.storage.worker.index").setLevel(logging.DEBUG)
    logging.getLogger("haplotyping.index.storage.worker.matches").setLevel(logging.DEBUG)
    logging.getLogger("haplotyping.index.storage.worker.merges").setLevel(logging.DEBUG)
    
    k = haplotyping.index.Database.detectKmerSize(locationSortedList)
    (unpairedReadFiles, pairedReadFiles, allReadFiles) = haplotyping.index.Database.detectReadFiles(
                                                            directoryReadFiles)
    
    database = haplotyping.index.Database(k, name, 
                                           locationOutputBase, locationSortedList, 
                                           unpairedReadFiles, pairedReadFiles, 
                                           maximumProcesses=threads,
                                           maximumMemory=memory,
                                           indexType=indexType,
                                           keepTemporaryFiles=keepTemporaryFiles, 
                                           debug=debug)
else:
    raise Exception("call: {} <directoryReadFiles> <locationSortedList> <locationOutputBase> ".format(sys.argv[0])+
                    "<threads> <name> <memory> <indexType>")
