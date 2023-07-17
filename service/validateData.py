#!/usr/bin/env python3
import os, sys, logging, configparser
import importlib.util
#fallback to local version
if importlib.util.find_spec("haplotyping")==None:
    print("TRYING TO USE LOCAL VERSION OF HAPLOTYPING PACKAGE")
    locationHaplotypingPackage = "../../haplotyping"
    if not locationHaplotypingPackage in sys.path: sys.path.insert(0, locationHaplotypingPackage)
#now, import haplotyping software
import haplotyping.data

logging.basicConfig(format="%(asctime)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S", level=logging.INFO)

postfix = ".xlsx"
indexName = "index.xlsx"

# Get the total number of args passed
dataPath = os.path.join(os.path.dirname(os.path.realpath(__file__)),"data")
config = configparser.ConfigParser()
configFile = os.path.join(os.path.dirname(os.path.realpath(__file__)),"config.ini")
with open(configFile, "r") as f:
    config.read_file(f)
dataPath = config.get("PATHS","data")
if os.path.isfile(os.path.join(dataPath,indexName)):
    indexPackage = os.path.splitext(indexName)[0]+".package.json"
    indexReport = os.path.splitext(indexName)[0]+".report.txt"
    #validate index
    validateIndex = True
    if os.access(os.path.join(dataPath,indexName), os.R_OK):
        if (os.access(os.path.join(dataPath,indexPackage), os.R_OK) 
            and os.access(os.path.join(dataPath,indexReport), os.R_OK)):
            validateIndex = False
            if (os.path.getmtime(os.path.join(dataPath,indexName))>=
                os.path.getmtime(os.path.join(dataPath,indexPackage))):
                validateIndex = True
            elif (os.path.getmtime(os.path.join(dataPath,indexName))>=
                  os.path.getmtime(os.path.join(dataPath,indexReport))):
                validateIndex = True        
    else:
        raise Exception("=== couldn't find {} ===".format(indexName))
    #only validate if tests are passed
    if validateIndex:
        print("=== validate index '{}' ===".format(indexName))
        if os.access(os.path.join(dataPath,indexPackage), os.R_OK):
            os.remove(os.path.join(dataPath,indexPackage))
        if os.access(os.path.join(dataPath,indexReport), os.R_OK):
            os.remove(os.path.join(dataPath,indexReport))
        validator = haplotyping.data.ValidateIndex(dataPath,indexName)
        with open(os.path.join(dataPath,indexReport), "w") as f:
            f.write(validator.createTextReport())
        validator.createPackageJSON(os.path.join(dataPath,indexPackage))
        if not validator.valid:
            mtime = os.path.getmtime(os.path.join(dataPath,indexName))
            os.utime(os.path.join(dataPath,indexPackage), (mtime, mtime))
            print("=== couldn't validate {} ===".format(indexName))
            os._exit(0)                
    else:
        print("=== skip validation {} (no changes) ===".format(indexName))    
    #now process all files
    filenames = []
    for filename in os.listdir(dataPath):
        if os.path.isfile(os.path.join(dataPath,filename)):
            if filename==indexName:
                pass
            elif filename.endswith(postfix):                    
                filenames.append(filename)
    #loop over filenames            
    for filename in filenames:
        #try:
        filenamePackage = os.path.splitext(filename)[0]+".package.json"
        filenameReport = os.path.splitext(filename)[0]+".report.txt"
        if os.access(os.path.join(dataPath,filename), os.R_OK):
            if validateIndex:
                if os.access(os.path.join(dataPath,filenamePackage), os.R_OK):
                    os.remove(os.path.join(dataPath,filenamePackage))
                if os.access(os.path.join(dataPath,filenameReport), os.R_OK):
                    os.remove(os.path.join(dataPath,filenameReport))
            elif os.access(os.path.join(dataPath,filenamePackage), os.R_OK):
                if (os.path.getmtime(os.path.join(dataPath,filename))<
                    os.path.getmtime(os.path.join(dataPath,filenamePackage))):
                    print("=== skip validation {} (no changes) ===".format(filename))
                    continue
                else:
                    os.remove(os.path.join(dataPath,filenamePackage))
                    if os.access(os.path.join(dataPath,filenameReport), os.R_OK):
                        os.remove(os.path.join(dataPath,filenameReport))
            elif os.access(os.path.join(dataPath,filenameReport), os.R_OK):
                if (os.path.getmtime(os.path.join(dataPath,filename))<
                    os.path.getmtime(os.path.join(dataPath,filenameReport))):
                    print("=== skip validation {} (no changes) ===".format(filename))
                    continue 
                else:
                    os.remove(os.path.join(dataPath,filenameReport))
        print("=== validate resource '{}' ===".format(filename))
        validator = haplotyping.data.ValidateData(dataPath,filename,indexPackage)
        with open(os.path.join(dataPath,filenameReport), "w") as f:
            f.write(validator.createTextReport())
        validator.createPackageJSON(os.path.join(dataPath,filenamePackage))
        if not validator.valid:
            mtime = os.path.getmtime(os.path.join(dataPath,filename))
            os.utime(os.path.join(dataPath,filenamePackage), (mtime, mtime))
            print("=== couldn't validate {} ===".format(filename))                                    
else:
    print("no index detected: {}".format(os.path.join(dataPath,indexName)))        
