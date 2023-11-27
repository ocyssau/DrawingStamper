#!/usr/bin/python
# from PyPDF2 import PdfFileWriter, PdfFileReader

from Application.Application import Stamp, Stamper, Application
from reportlab.lib.units import mm
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

myStamp = Stamp()

parser = argparse.ArgumentParser('placards')
parser.description = 'macro de tamponnage des plans pdf'
parser.epilog = 'for sier'

parser.add_argument('--inDir', help='Input Directory', default = dataPath)
parser.add_argument('--outDir', help='Output Directory', default = tempfile.gettempdir())
parser.add_argument('-i', help='Input File', default = os.path.join(dataPath, "in.pdf"))
parser.add_argument('-o', help='Output File', default = os.path.join(tempfile.gettempdir(), "out.pdf"))
parser.add_argument('-m', help='Message', default = myStamp.message)
parser.add_argument('-d', help='Date', default = myStamp.date)
parser.add_argument('-p', help='Project number', default = myStamp.projectNumber)
parser.add_argument('-u', help='Username', default = myStamp.username)
parser.add_argument('-w', help='table Width', default = myStamp.width)
parser.add_argument('-s', help='police Size', default = myStamp.policeSize)
parser.add_argument('-x', help='position X')
parser.add_argument('-y', help='position Y')
parser.add_argument('-c', help='Color', default = myStamp.color)
parser.add_argument('-bc', help='Background Color', default=myStamp.backgroundColor)
parser.add_argument('-v', help='Display infos and version')

args = parser.parse_args()
print(args)

if args.v == 1:
    print("Stamper for pdf SIER, See source code and help: " +  Application.WEB_SITE)
    print("Version: " +  Application.VERSION)

myStamp.message = args.m
myStamp.date = args.d
myStamp.projectNumber = args.p
myStamp.username = args.u
myStamp.width = args.w
myStamp.policeSize = args.s
myStamp.color = args.c  # blue, green, red
myStamp.backgroundColor = args.bc  # beige

#generate pdf file for the stamp in a temmp file
myStamp.update()

#logging.info("STAMP: " + myStamp.file.name)
logging.info(mm)

#init the stamper
myStamper = Stamper(myStamp)

#get files in current directory
inpdf = args.i
outpdf = args.o

posX = args.x * mm
posY = args.y * mm

#stamp the pdf
myStamper.stampPdf(inpdf, outpdf, "ALL", [posX, posY])

logging.info("INPUT DIR: " + inpdf)
logging.info("OUTPUT DIR: " + outpdf)
