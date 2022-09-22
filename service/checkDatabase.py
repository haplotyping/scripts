#!python3
import os, sys, logging

locationHaplotypingPackage = "../../haplotyping"
if not locationHaplotypingPackage in sys.path: sys.path.insert(0, locationHaplotypingPackage)
import haplotyping.data

logging.basicConfig(format="%(asctime)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S", level=logging.INFO)

databasePath = os.path.join(os.path.dirname(os.path.realpath(__file__)),"export")
haplotyping.data.CheckDatabase(databasePath)