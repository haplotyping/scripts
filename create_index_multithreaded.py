
#----------
# SETTINGS
#----------

locationKmerList = "./data/kmer/"
locationReads = "./data/readFiles/"
locationOutput = "./data/kmer/"
numberOfThreads = 3
kmerSize = 31

#----------------------------
# CREATE NAME FROM DIRECTORY
#----------------------------
 
def getName(dirname,readFiles):
    name = dirname.split(os.sep)[-1]
    #return None to skip entry
    if "cultivar2" in name:        
        return None
    return name

#-------------
# MAIN SCRIPT
#-------------

import sys,os,glob,queue,threading,time,logging
locationHaplotypingPackage = "../haplotyping"
if not locationHaplotypingPackage in sys.path: sys.path.insert(0, locationHaplotypingPackage)
import haplotyping.index

logger = logging.getLogger("script")
logging.getLogger().setLevel(logging.WARNING)
logger.setLevel(logging.INFO)
logging.basicConfig(format="%(asctime)s | %(name)s |  %(levelname)s: %(message)s", datefmt="%m-%d-%y %H:%M:%S")

logger.info("search for directories with sorted k-mer lists and reads")
possibleDirectories = []

patternsKmerList = ["kmer.list.sorted.gz"]
patternsReads = ["*.fastq.gz"]
possibleKmerListFiles = set([y for x in os.walk(locationKmerList) 
                        for p in patternsKmerList
                        for y in glob.glob(os.path.join(x[0], p))])
for possibleKmerListFile in possibleKmerListFiles:
    possibleKmerListDirectory = os.path.dirname(possibleKmerListFile)
    if possibleKmerListDirectory[0:len(locationKmerList)]==locationKmerList:                
        possibleReadsDirectory = locationReads+possibleKmerListDirectory[len(locationKmerList):]
        outputDirectory = locationOutput+possibleKmerListDirectory[len(locationKmerList):]
        possibleReadFiles = set([y for x in os.walk(possibleReadsDirectory) 
                        for p in patternsReads
                        for y in glob.glob(os.path.join(x[0], p))])
        if len(possibleReadFiles)>0:
            name = getName(possibleKmerListDirectory,possibleReadFiles)
            if not name==None:
                possibleDirectories.append([name,
                                        possibleKmerListFile,
                                        outputDirectory,
                                        possibleReadsDirectory])
        else:
            logger.warning("no reads found in '"+str(possibleReadsDirectory)+"', skipping '"+
                  str(possibleKmerListDirectory)+"'")
    else:
        logger.error("problem with directory '"+str(possibleKmerListDirectory)+"'")
logger.info("found "+str(len(possibleDirectories))+" directories with sorted k-mer lists and reads")    

exitFlag = 0

class myThread (threading.Thread):
   def __init__(self, threadID, name, q):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.name = name
      self.q = q
   def run(self):
      create_index(self.name, self.q)

def create_index(threadName, q):
    while not exitFlag:
        queueLock.acquire()
        if not workQueue.empty():
            data = q.get()
            queueLock.release()
            logger.info(str(threadName)+": create index "+str(data[0]))
            name=data[0]
            (unpairedReadFiles, pairedReadFiles, allReadFiles) = haplotyping.index.Database.detectReadFiles(data[3])
            sortedList = data[1]
            outputFile = data[2]+"/kmer.data"
            database = haplotyping.index.Database(kmerSize, name, 
                                       outputFile, sortedList, 
                                       unpairedReadFiles, pairedReadFiles)
        else:
            queueLock.release()
        time.sleep(1)       
       
    
logger.info("creating indices using "+str(numberOfThreads)+" threads started")

queueLock = threading.Lock()
workQueue = queue.Queue(-1)
threads = []

# create new threads
for i in range(numberOfThreads):
   thread = myThread(i, "thread-"+str(i), workQueue)
   thread.start()
   threads.append(thread)

# fill the queue
queueLock.acquire()
for item in possibleDirectories:
   workQueue.put(item)
queueLock.release()

# wait for queue to empty
while not workQueue.empty():
   pass

# notify threads it's time to exit
exitFlag = 1

# wait for all threads to complete
for t in threads:
   t.join()
logger.info("creating indices finished")
