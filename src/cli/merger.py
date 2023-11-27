#!/usr/bin/python
from Application.Application import Application, Merger
import argparse
import sys
import os
import tempfile
import logging

app = Application()

# determine if application is a script file or frozen exe
if getattr(sys, 'frozen', False):
    srcPath = os.path.dirname((os.path.dirname(sys.executable)))
    dataPath = os.path.join(os.path.dirname(srcPath), "data")
elif __file__:
    srcPath = os.path.dirname(os.path.dirname(__file__))
    dataPath = os.path.join(os.path.dirname(srcPath), "data")

Application.SRC_PATH = srcPath
Application.DATA_PATH = dataPath

logging.info("SOURCE PATH: " + srcPath)
logging.info("DATA PATH: " + dataPath)

parser = argparse.ArgumentParser('placards')
parser.description = 'macro fusionnage des plans pdf'
parser.epilog = 'for sier'

parser.add_argument('-i', help='Input Directory', default = dataPath)
parser.add_argument('-o', help='Output File', default = os.path.join(tempfile.gettempdir(), "mergeout.pdf"))
parser.add_argument('-v', help='Display infos and version')

args = parser.parse_args()
print(args)

if args.v == 1:
    print("Merger for pdf SIER, See source code and help: " +  Application.WEB_SITE)
    print("Version: " +  Application.VERSION)

outpdf = args.o
indir = args.i
myMerger = Merger()

myMerger.addFromDirectory(indir)
myMerger.save(outpdf)

logging.info("INPUT DIR: " + indir)
logging.info("OUTPUT DIR: " + outpdf)
