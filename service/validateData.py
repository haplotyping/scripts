#!python3
import os, sys, logging, libraries.dmValidator as dmValidator

logging.basicConfig(format="%(asctime)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S", level=logging.INFO)

postfix = ".xlsx"
pedigreeName = "pedigree.xlsx"

# Get the total number of args passed
dataPath = os.path.join(os.path.dirname(os.path.realpath(__file__)),"data")
schemaPath = os.path.join(os.path.dirname(os.path.realpath(__file__)),"schema")
if os.path.isfile(os.path.join(dataPath,pedigreeName)):
    pedigreePackage = os.path.splitext(pedigreeName)[0]+".package.json"
    pedigreeReport = os.path.splitext(pedigreeName)[0]+".report.txt"
    #validate pedigree
    validatePedigree = True
    if os.access(os.path.join(dataPath,pedigreeName), os.R_OK):
        if (os.access(os.path.join(dataPath,pedigreePackage), os.R_OK) 
            and os.access(os.path.join(dataPath,pedigreeReport), os.R_OK)):
            validatePedigree = False
            if (os.path.getmtime(os.path.join(dataPath,pedigreeName))>=
                os.path.getmtime(os.path.join(dataPath,pedigreePackage))):
                validatePedigree = True
            elif (os.path.getmtime(os.path.join(dataPath,pedigreeName))>=
                  os.path.getmtime(os.path.join(dataPath,pedigreeReport))):
                validatePedigree = True        
    else:
        raise Exception("=== couldn't find {} ===".format(pedigreeName))
    #only validate if tests are passed
    if validatePedigree:
        print("=== validate {} ===".format(pedigreeName))
        if os.access(os.path.join(dataPath,pedigreePackage), os.R_OK):
            os.remove(os.path.join(dataPath,pedigreePackage))
        if os.access(os.path.join(dataPath,pedigreeReport), os.R_OK):
            os.remove(os.path.join(dataPath,pedigreeReport))
        validator = dmValidator.ValidatePedigree(dataPath,schemaPath,pedigreeName)
        with open(os.path.join(dataPath,pedigreeReport), "w") as f:
            f.write(validator.createTextReport())
        validator.createPackageJSON(os.path.join(dataPath,pedigreePackage))
        if not validator.valid:
            mtime = os.path.getmtime(os.path.join(dataPath,pedigreeName))
            os.utime(os.path.join(dataPath,pedigreePackage), (mtime, mtime))
            print("=== couldn't validate {} ===".format(pedigreeName))
            os._exit(0)                
    else:
        print("=== skip validation {} (no changes) ===".format(pedigreeName))    
    #now process all files
    filenames = []
    for filename in os.listdir(dataPath):
        if os.path.isfile(os.path.join(dataPath,filename)):
            if filename==pedigreeName:
                pass
            elif filename.endswith(postfix):                    
                filenames.append(filename)
    #loop over filenames            
    for filename in filenames:
        #try:
        filenamePackage = os.path.splitext(filename)[0]+".package.json"
        filenameReport = os.path.splitext(filename)[0]+".report.txt"
        if os.access(os.path.join(dataPath,filename), os.R_OK):
            if validatePedigree:
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
        print("=== validate {} ===".format(filename))
        validator = dmValidator.ValidateData(dataPath,schemaPath,filename,pedigreePackage)
        with open(os.path.join(dataPath,filenameReport), "w") as f:
            f.write(validator.createTextReport())
        validator.createPackageJSON(os.path.join(dataPath,filenamePackage))
        if not validator.valid:
            mtime = os.path.getmtime(os.path.join(dataPath,filename))
            os.utime(os.path.join(dataPath,filenamePackage), (mtime, mtime))
            print("=== couldn't validate {} ===".format(filename))                                    
else:
    print("no pedigree detected: {}".format(os.path.join(dataPath,pedigreePackage)))        

