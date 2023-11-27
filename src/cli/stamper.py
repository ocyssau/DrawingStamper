from Application.Application import Stamp, Stamper, Application
from reportlab.lib.units import mm
import sys
import os
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
myStamp.message = "BON A FABRIQUER"
myStamp.date = "05/12/23"
myStamp.projectNumber = "xx-xxx"
myStamp.username = "O CYSSAU"
myStamp.width = 80*mm
myStamp.policeSize = 5*mm
myStamp.color = "green"  # blue, green, red
#myStamp.backgroundColor = "beige"  # beige

#generate pdf file for the stamp in a temmp file
myStamp.update()
myStamp.saveToFile("mystamp.pdf")

#logging.info("STAMP: " + myStamp.file.name)
logging.info(mm)

#init the stamper
myStamper = Stamper(myStamp)

#get files in current directory
inpdf = ""
outpdf = ""

posX = 50 * mm
posY = 50 * mm

#stamp the pdf
#myStamper.stampPdf(inpdf, outpdf, "ALL", [posX, posY])

logging.info("INPUT DIR: " + inpdf)
logging.info("OUTPUT DIR: " + outpdf)
