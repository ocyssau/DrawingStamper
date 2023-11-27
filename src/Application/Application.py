import os
from datetime import datetime
import tempfile
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A0

#from PyPDF2 import PdfWriter, PdfReader, Transformation#, PdfMerger
from pypdf import PdfWriter, PdfReader, Transformation #, PdfMerger

#from PDFlib import *

import logging
import sys
import io
import glob
import copy
import json

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
        #watermark reader
        self.wmReader = PdfReader(myStamp.file)
        #watermark page
        self.wmPage = self.wmReader.pages[0]
        self.wm = myStamp

    def addFromDirectory(self, path):
        fileList = Application.getPdfFromDirectory(path)
        for filepath in fileList:
            position = [30,30]
            outfiles = []
            outfiles.append(self.stampPdf(filepath, "ALL", position))
        return outfiles

    def stampPdf(self, inpdf,  pages, position):
        pdfReader = PdfReader(open(inpdf, 'rb'), strict=False)
        pdfWriter = PdfWriter()

        if pages == "ALL":
            pages = list(range(0, len(pdfReader.pages)))
        for page in pages:
            
            page = pdfReader.pages[page]
            myMediabox = page.mediabox
            posX, posY = position
            
            if posX < 0 :
                trX = (float(myMediabox.width) - float(self.wm.width)) + float(posX)
            else:
                trX = posX

            if posY < 0 :
                trY = (float(myMediabox.height) - float(self.wm.height)) + float(posY)
            else:
                trY = posY
            
            #les valeurs de trX et trY doivent etres des entiers, sign�s
            myWmPage =  copy.deepcopy(self.wmPage)
            myWmPage.add_transformation(Transformation().translate(tx=round(trX,0), ty=round(trY,0)))
            
            page.merge_page(myWmPage)
            
            #myPage.mediabox = myMediabox
            p = pdfWriter.add_page(page)
            p.compress_content_streams()
        
        pdfWriter.add_metadata(pdfReader.metadata)
        
        pdfReader.stream.close()
        
        return pdfWriter

class Merger():
    
    def __init__(self):
        self.pdfWriter = PdfWriter()
    
    def addFromDirectory(self, path):
        fileList = Application.getPdfFromDirectory(path)
        for filepath in fileList:
            self.addPdf(filepath, "ALL")
    
    def addPdf(self, inpdf, pages):
        pdfReader = PdfReader(inpdf)
        if pages == "ALL":
            pages = list(range(0, len(pdfReader.pages)))
        for index in pages:
            myPage = pdfReader.pages[index]
            self.pdfWriter.add_page(myPage)
    
    def save(self, outpdf):
        if len(self.pdfWriter.pages) > 0:
            with open(outpdf, "wb") as fp:
                self.pdfWriter.write(fp)
                return True
        else:
            return False

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

    def loadFromJson(self, jData):
        self.__dict__ = json.load(jData)

    def saveToJson(self):
        return json.dumps(self)
    
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
            