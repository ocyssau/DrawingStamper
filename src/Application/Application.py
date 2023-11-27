import os
from datetime import datetime
import tempfile
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A0
from PyPDF2 import PdfWriter, PdfReader, Transformation, PdfMerger
import logging
import sys
import io
import glob
import copy

#from pathlib import Path
#from typing import Union, Literal, List

class Application():
    
    VERSION = "0.0.1"
    APPLICATION_PATH = ""    
    SRC_PATH = ""
    DATA_PATH = ""
    CONFIG_INIPATH = ""
    CONFIG_DIST_INIPATH = ""
    USER_HOME = ""
    WEB_SITE = ""
    
    def __init__(self):
        #https://docs.python.org/2/library/logging.html
        logging.basicConfig(stream=sys.stderr, level=logging.DEBUG, format='%(pathname)s:%(lineno)s:%(message)s')

    @staticmethod
    def getPdfFromDirectory(path):
        try:
            pattern = "*.pdf"
            globPathName = os.path.join(path, pattern)
            fileList = glob.glob(globPathName)
            fileList.sort()
        except Exception as e:
            fileList = []
            logging.debug(str(e))

        fileListFiltered =  []
        for filename in fileList:
            filename = os.path.basename(filename)
            filepath = os.path.join(path, filename)
            
            if os.path.isdir(filepath):
                continue
            else:
                fileListFiltered.append(filepath)

        return fileListFiltered

class Stamper():
    
    def __init__(self, myStamp):
        reader = PdfReader(myStamp.file)
        self.stampPage = reader.pages[0]
        self.stamp = myStamp

    def addFromDirectory(self, path):
        fileList = Application.getPdfFromDirectory(path)
        for filepath in fileList:
            outpdf = filepath
            position = [30,30]
            self.stampPdf(filepath, outpdf, "ALL", position)

    def stampPdf(self, inpdf, outpdf, pages, position):
        reader = PdfReader(inpdf)
        writer = PdfWriter()

        if pages == "ALL":
            pages = list(range(0, len(reader.pages)))

        for index in pages:
            myPage = reader.pages[index]
            myMediabox = myPage.mediabox
            
            posX, posY = position
            
            if posX < 0 :
                trX = (float(myMediabox.width) - float(self.stamp.width)) + float(posX)
            else:
                trX = posX

            if posY < 0 :
                trY = (float(myMediabox.height) - float(self.stamp.height)) + float(posY)
            else:
                trY = posY
            
            #les valeurs de trX et trY doivent etres des entiers, sign�s
            myStampPage =  copy.deepcopy(self.stampPage)
            myStampPage.add_transformation(Transformation().translate(tx=round(trX,0), ty=round(trY,0)))
            myPage.merge_page(myStampPage)
            myPage.compress_content_streams()
            
            #myPage.mediabox = myMediabox
            writer.add_page(myPage)
        
        writer.add_metadata(reader.metadata)
        #with open(outpdf, "wb") as fp:
            #writer.write(fp)

class Merger():
    
    def __init__(self):
        self.writer = PdfWriter()
    
    def addFromDirectory(self, path):
        fileList = Application.getPdfFromDirectory(path)
        for filepath in fileList:
            self.addPdf(filepath, "ALL")
    
    def addPdf(self, inpdf, pages):
        reader = PdfReader(inpdf)
        if pages == "ALL":
            pages = list(range(0, len(reader.pages)))
        for index in pages:
            myPage = reader.pages[index]
            myPage.compress_content_streams()
            self.writer.add_page(myPage)
    
    def save(self, outpdf):
        with open(outpdf, "wb") as fp:
            self.writer.write(fp)

class Stamp():
    
    def __init__(self):
        self.mm = mm
        self.message = "NON VALIDE POUR FAB"
        self.date = datetime.today().strftime('%d-%m-%Y')
        self.projectNumber = "xx-xxxx"
        self.username = os.getlogin() + "(SIER)"
        self.width = 130*self.mm
        self.color = colors.red #blue, green
        self.backgroundColor = colors.transparent
        self.thickness = 2
        self.file = tempfile.TemporaryFile(mode='w+b', prefix="SIERDrawingStamp")
        self.nrow = 4
        self.ncol = 1
        self.setPoliceSize(8*mm)
    
    def setPoliceSize(self, policeSize):
        self.policeSize = policeSize
        self.rowHeight = self.policeSize + 15
        self.height = self.rowHeight * self.nrow
    
    def setStatus(self, status):
        self.backgroundColor = colors.transparent
        
        if status == "BPF":
            self.message = "BON POUR FABRICATION"
            self.color = colors.green
        elif status == "BPC":
            self.message = "BON POUR CONSULTATION"
            self.color = colors.blue
        elif status == "BPA":
            self.message = "BON POUR APPRO"
            self.color = colors.blue
        elif status == "NPF":
            self.message = "NON VALIDE POUR FAB"
            self.color = colors.red
    
    def update(self):
        
        #out to memory virtual file
        packet = io.BytesIO()
        
        c = canvas.Canvas(packet, pagesize=A0)  # alternatively use bottomup=False
        width, height = [300,300]
        
        data = [[self.message],[self.date],[self.projectNumber],[self.username]]
        self.nrow = len(data)
        
        table = Table(data, colWidths=self.width, rowHeights=self.rowHeight)
        table.setStyle(TableStyle([('ALIGN',(0,0),(0,-1),'LEFT'),
                                ('VALIGN', (0,0), (0,-1), 'MIDDLE'),
                                ('FONTSIZE', (0,0), (0,-1), self.policeSize),
                                ('TEXTCOLOR',(0,0),(0,-1),self.color),
                                ('INNERGRID', (0,0), (0,-1), self.thickness, self.color),
                                ('BOX', (0,0), (0,-1), self.thickness, self.color),
                                ('BACKGROUND', (0,0), (0,-1), self.backgroundColor),
                                ]))
        
        table.wrapOn(c, width, height)
        table.drawOn(c, 0, 0)
        
        c.save()
        
        #move to the beginning of the StringIO buffer
        packet.seek(0)
        self.file = packet
        
    def saveToFile(self, filename):
        if os.path.isfile(filename):
            None
        with open(filename, "wb") as f:
            f.write(self.file.getbuffer())
            