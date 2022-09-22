#!python3
import os, sys, configparser, logging

locationHaplotypingPackage = "../../haplotyping"
if not locationHaplotypingPackage in sys.path: sys.path.insert(0, locationHaplotypingPackage)
import haplotyping.data

logging.basicConfig(format="%(asctime)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S", level=logging.INFO)

dataPath = os.path.join(os.path.dirname(os.path.realpath(__file__)),"data")
exportPath = os.path.join(os.path.dirname(os.path.realpath(__file__)),"export")
haplotyping.data.ConstructDatabase(dataPath, exportPath)