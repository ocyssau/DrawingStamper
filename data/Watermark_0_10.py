# coding: utf8 
import os
import getpass
from datetime import date
#import reportlab
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer,Table,TableStyle
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle as PS
from reportlab.lib.enums import TA_CENTER, TA_LEFT,TA_RIGHT,TA_JUSTIFY
from reportlab.lib.styles import ParagraphStyle
#
from PyPDF2 import PdfFileWriter, PdfFileReader





##def stringWidth2(string, font, size, charspace):
##    width = canvas.stringWidth(string, font, size)
##    width += (len(string) - 1) * charspace
##    return width

def Tampon(fileName="watermark.pdf",Texte="Bon pour Fabrication",Username="",Date="",x=5,y=4,RGB=(1,0,0)):
    """ Creation d'un tampon"""
    
    if Username == "":
        Username= "{} (SIER)".format(getpass.getuser()) # Username
        #Username="T.Demange"
    if Date=="":
        Date = date.today()
    #Ligne= "{}\n{}\n{:%d %b %Y}".format(Texte,Username,Date)
    data=[[Texte],[Username],[Date]]
    t=Table(data)
    t.setStyle(TableStyle([
                       ('TEXTCOLOR',(0,0),(0,2),RGB),
                       ('ALIGN',(1,0),(0,0),'LEFT'),
                       ('ALIGN',(0,0),(0,0),'CENTER'),
                       ('FONT', (0, 0), (-1, 0), 'Helvetica-Bold'),
                           ('BOX', (0,0), (-1,-1), 2.75, RGB)])
                      
               )

    c = canvas.Canvas(fileName)
    t.wrapOn(c,0,0)
    t.drawOn(c,x*cm,y*cm)
    c.save()
    #return c

def MergePDF(WatermarkFile,FichierIN,RepOUT):
   # print WatermarkFile
  #  print type(FichierIN),FichierIN
  #  print RepOUT
    # Get the watermark file you just created
    f_watermark=open(WatermarkFile, "rb")
    watermark = PdfFileReader(f_watermark)
    # Get our files ready
    output_file = PdfFileWriter()
    f_input=open(FichierIN, "rb")
    input_file = PdfFileReader(f_input)
    # Number of pages in input document
    page_count = input_file.getNumPages()
    for page_number in range(page_count):
        #print "Watermarking page {} of {}".format(page_number, page_count)
        # merge the watermark with the page
        input_page = input_file.getPage(page_number)
        input_page.mergePage(watermark.getPage(0))
        input_page.compressContentStreams()
        output_file.addPage(input_page)

    # finally, write "output" to document-output.pdf
    filename, file_extension = os.path.splitext(FichierIN)
    NewName = os.path.join(RepOUT,os.path.basename(filename)+"_TP.pdf")

    f_out=open(NewName, "wb")
    with f_out as outputStream:
        output_file.write(outputStream)
    f_input.close()    
    f_watermark.close()
    f_out.close()
    outputStream.close()
    return None

class WaterRep:
    def __init__(self,RepSource,RepDest,Txt,Dx,Dy,StringStatus=None,RGB=(1,0,0)):
        
        self.nb=0
        self.n=0
        self.status=-1
        lstFile=[]
        self.RepDest=RepDest
        self.StringStatus=StringStatus
        #print "ICI",StringStatus

        # Creation du tampon
        TamponFile=os.path.join(str(RepDest),"TamponSIER.pdf")
        Tampon(fileName=TamponFile,Texte=Txt,x=Dx,y=Dy,RGB=RGB)
        
        for elm in os.listdir(str(RepSource)):
            filename, file_extension = os.path.splitext(elm)
           # print file_extension.upper()
            FichierIn=os.path.join(RepSource,elm)
            if file_extension.upper()==".PDF":
                lstFile.append(FichierIn)
                
        self.nb=len(lstFile)
        for fichier in  lstFile  :
               # print (FichierIn)
               self.n=self.n+1
               if self.StringStatus!=None:
                   ligne=u" Status : {} / {} PDF".format(self.n,self.nb)
                   print ligne
                   #StringStatus.set(ligne)
                   self.StringStatus.set(ligne)
               MergePDF(TamponFile,fichier,RepDest)
               
        print self.n,self.nb,self.status,self.StringStatus
                
        self.status=0

    def  ExpXls(self):
        if lstFile!=[]:
            FichierXls=os.path.join(self.RepDest,"Liste.xls")
            fs=open(FichierXls,"w")
            fs.write( "Source\tDestination\tStatus\n")
            for elm in lstFile:
                ligne="{}\t{}_BPF.pdf\t{}\n".format(elm,elm,Txt)
                fs.write(elm+"\n")
            fs.close()


       # return 0,len(lstFile)
            

if __name__ == '__main__':
    Tampon(Texte="Not for manufacturing\nOnly for quotation",RGB=(0,1,0))
    #WaterRep("/home/user/Dev/Python/PDF_Watermarks/PDF_Source/",u"/home/user/Dev/Python/PDF_Watermarks/PDF_Dest/",Txt="test55",Dx=3.,Dy=5.)

    

