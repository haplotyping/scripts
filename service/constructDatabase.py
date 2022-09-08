#!python3
import os, sys, configparser, logging, libraries.dmConstructDatabase as dmConstructDatabase

logging.basicConfig(format="%(asctime)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S", level=logging.INFO)

dataPath = os.path.join(os.path.dirname(os.path.realpath(__file__)),"data")
exportPath = os.path.join(os.path.dirname(os.path.realpath(__file__)),"export")
dmConstructDatabase.ConstructDatabase(dataPath, exportPath)