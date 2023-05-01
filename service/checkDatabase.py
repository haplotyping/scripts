#!python3
import os, sys, logging, configparser
import haplotyping.data

logging.basicConfig(format="%(asctime)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S", level=logging.INFO)

config = configparser.ConfigParser()
configFile = os.path.join(os.path.dirname(os.path.realpath(__file__)),"config.ini")
with open(configFile, "r") as f:
    config.read_file(f)
haplotyping.data.CheckDatabase(config.get("PATHS","service"))
