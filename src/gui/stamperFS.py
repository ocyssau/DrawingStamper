# -*- coding:utf-8 -*-
import os
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from Application.Application import Stamp, Stamper, Merger, Application
from reportlab.lib.units import mm
import argparse
import tempfile
import logging

class stamperGui(Tk):
        """ Mon programme graphique utilisant Python3 et Tkinter """
 
        statusBPF = "BON pour Fabrication"
        statusNPF = "NON VALIDE pour Fabrication"
        statusBPC = "BON pour Consultation"
        statusBPA = "BON pour Approvisionnement"
        
        def __init__(self, application):
            Tk.__init__(self)  # On dérive de Tk, on reprend sa méthode d'instanciation
            
            self.application = application
            
            # Widgets
            
            ##frame 0 : ACTIONS
            self.Frame0 = LabelFrame(self, relief=GROOVE, borderwidth=2, text="Selectionnez les tâches")
            self.Frame0.grid(row=0 , column=0, columnspan=8, sticky=W)

            # case a cocher
            ## stamp CC
            self.stampPdfVal = IntVar()
            self.stampPdfVal.set(1)
            self.stampPdfCC = Checkbutton(self.Frame0, text = "Tamponner les PDFs", command = self._stampPdfCCOnClick, variable = self.stampPdfVal)
            self.stampPdfCC.grid(row=0 , column=0)

            ## merge pdf CC
            self.mergePdfVal = IntVar()
            self.mergePdfCC = Checkbutton(self.Frame0,text = "Fusionner les PDFs de sortie",command = self._MergePdfCCOnClick, variable = self.mergePdfVal)
            self.mergePdfVal.set(1)
            self.mergePdfCC.grid(row=0 , column=1)

            ##Box selction entrees-sorties
            self.title("Sier Drawing Stamper - Merger V"+self.application.VERSION)
            self.geometry('450x450+100+100')
            
            ##frame 1 : IN - OUT
            self.Frame1 = LabelFrame(self, relief=GROOVE, borderwidth=2, text="PDF : Selectionner les répertoires d'entrée et de sortie")
            self.Frame1.grid(row=1 , column=0, columnspan=8, sticky=W)
            
            ##repertoire entree
            self.RepInButtonLabel = Label(self.Frame1, justify='left', text=u" Répertoire Source")
            self.RepInButtonLabel.grid(row=0 , column=0)
            self.RepInButton = Button(self.Frame1, text=u" Select ", command=self._RepInd)
            self.RepInButton.grid(row=1 , column=1)
            self.RepIn = Label(self.Frame1, text=os.getcwd(), justify='left', relief=SUNKEN)
            self.RepIn.grid(row=1 , column=0)
            
            ##rep sortie
#             self.RepOutButtonLabel = Label(self.Frame1, text=u" Répertoire Destination", justify='left')
#             self.RepOutButtonLabel.grid(row=2 , column=0)
#             self.RepOutButton = Button(self.Frame1, text=u" Select ", command=self._RepOutd)
#             self.RepOutButton.grid(row=3 , column=1)
#             self.RepOut = Label(self.Frame1, text="C:\TEMP", justify='left', relief=SUNKEN)
#             self.RepOut.grid(row=3 , column=0)
            
            ## frame 2 tampon
            self.Frame2 = LabelFrame(self, relief=GROOVE, borderwidth=2, text="TAMPON", padx=5, pady=5)
            self.Frame2.grid(row=2 , column=0, columnspan=8, sticky=W)
            
            ##liste de selection du status
            statusListe = (self.statusBPF, self.statusNPF) #self.statusBPA, self.statusBPC
            self.statusSelectLabel = Label(self.Frame2, text=u" Status :")
            self.statusSelectLabel.grid(row=0 , column=0, sticky=W)
            self.statusSelect = ttk.Combobox(self.Frame2, text="", values=statusListe)
            self.statusSelect.set(statusListe[1])
            self.statusSelect.grid(row=0 , column=1, sticky=W, columnspan=8)
            
            ##project number
            self.projectInLabel = Label(self.Frame2, text=u" Project Number ")
            self.projectInLabel.grid(row=2 , column=0, sticky=W)
            projectInVal = StringVar()
            projectInVal.set('xx-xxx')
            self.projectIn = Entry(self.Frame2, textvariable=projectInVal)
            self.projectIn.grid(row=2 , column=1, sticky=W, columnspan=8)
            
            ## frame 3 position
            self.Frame3 = LabelFrame(self.Frame2, relief=GROOVE, borderwidth=0, text="Position", padx=2, pady=2)
            self.Frame3.grid(row=3 , column=0, columnspan=8, sticky=W)
            
            ##position
            self.label3 = Label(self.Frame3, text=u"(Ref : Bas-Gauche de la page, ou haut-droit en cas de valeur négatives)")
            self.label3.grid(row=3 , column=0, columnspan=8, sticky=W)
            
            ##position X
            posXVal = StringVar()
            posXVal.set('15')
            self.PosXInLabel = Label(self.Frame3, text=u" X (mm)= ")
            self.PosXInLabel.grid(row=4 , column=0, sticky=W)
            self.PosXIn = Entry(self.Frame3, textvariable=posXVal)
            self.PosXIn.grid(row=4 , column=1)
            
            ##position Y
            posYVal = StringVar()
            posYVal.set('-30')
            self.PosYInLabel = Label(self.Frame3, text=u" Y (mm)= ")
            self.PosYInLabel.grid(row=5 , column=0, sticky=W)
            self.PosYIn = Entry(self.Frame3, textvariable=posYVal)
            self.PosYIn.grid(row=5 , column=1)
            
            ## DIMENSIONS
            self.Frame4 = LabelFrame(self.Frame2, relief=GROOVE, borderwidth=0, text="Dimensions", padx=2, pady=2)
            self.Frame4.grid(row=4 , column=0, columnspan=8, sticky=W)
            
            ## Police size
            PoliceSizeVal = StringVar()
            PoliceSizeVal.set('5')
            self.PoliceSizeLabel = Label(self.Frame4, text=u" Taille de la police (mm)= ")
            self.PoliceSizeLabel.grid(row=0 , column=0, sticky=W)
            self.PoliceSizeIn = Entry(self.Frame4, textvariable=PoliceSizeVal)
            self.PoliceSizeIn.grid(row=0 , column=1)
            
            ## Width
            WidthVal = StringVar()
            WidthVal.set('80')
            self.WidthLabel = Label(self.Frame4, text=u" Largeur du tableau (mm)= ")
            self.WidthLabel.grid(row=1 , column=0, sticky=W)
            self.WidthIn = Entry(self.Frame4, textvariable=WidthVal)
            self.WidthIn.grid(row=1 , column=1)
            
            ## frame 4 BUTTONS
            self.Frame4 = LabelFrame(self, relief=GROOVE, borderwidth=0, text="", padx=2, pady=2)
            self.Frame4.grid(row=4 , column=0, columnspan=8, sticky=W)
            
            ## Button ok
            self.OKB = Button(self.Frame4, text=u" OK ", command=self._validate)
            self.OKB.grid(row=2 , column=0)
            
            ## Button Cancel
            self.ExitB = Button(self.Frame4, text=u" Cancel ", command=self._cancel)
            self.ExitB.grid(row=2 , column=1)
            
            ## LOGGER RETURN
            self.logOutputLabel = Label(self, text="Status :")
            self.logOutputLabel.grid(row=5 , column=0, columnspan=8, sticky=W)

        def _validate(self):
            self.logOutputLabel['text'] = "En cours..."
            
            try:
                # init stamp
                myStamp = Stamp()
                myStamp.projectNumber = self.projectIn.get()
            except Exception as e:
                self.log(str(e))
            try:
                status = self.statusSelect.get()
                if status == self.statusBPF:
                    myStamp.setStatus("BPF")
                elif status == self.statusBPC:
                    myStamp.setStatus("BPC")
                elif status == self.statusNPF:
                    myStamp.setStatus("NPF")
                elif status == self.statusBPA:
                    myStamp.setStatus("BPA")
                else:
                    myStamp.setStatus("NPF")
                
                policeSize = float(self.PoliceSizeIn.get()) * mm
                myStamp.setPoliceSize(policeSize)
                
                width = float(self.WidthIn.get()) * mm
                myStamp.width = width
                
                posX = float(self.PosXIn.get()) * mm
                posY = float(self.PosYIn.get()) * mm
                position = [posX, posY]
                
                # update datas of stamp
                myStamp.update()

                #get files in current directory
                inpdf = self.RepIn['text']
                #myStamp.saveToFile(os.path.join(inpdf, "stamp.pdf"))

            except Exception as e:
                self.log(str(e))
            
            ## STAMP
            if self.stampPdfVal.get() :
                try:
                    #init the stamper
                    myStamper = Stamper(myStamp)
                    
                    #stamp the pdf
                    fileList = Application.getPdfFromDirectory(inpdf)
                    for filepath in fileList:
                        #outpdf = filepath.replace(".pdf", "-wm.pdf")
                        outpdf = filepath
                        self.log("Stamp " + outpdf)
                        pdfWriter = myStamper.stampPdf(filepath, "ALL", position)
                        pdfWriter.write(outpdf)
                        
                except Exception as e:
                    self.log(str(e))
            
            ## MERGE
            if self.mergePdfVal.get() :
                try:
                    #get files in current directory
                    #outDir = self.RepOut['text']
                    
                    #init the merger
                    myMerger = Merger()
                    myMerger.addFromDirectory(inpdf)
                    mergedFile = os.path.join(inpdf, "merged.pdf")
                    self.log("Merge to " + mergedFile)
                    myMerger.save(mergedFile)
                except Exception as e:
                    self.log(str(e))
                
            self.log("...Finished-Ready")
        
        def _cancel(self):
            self.destroy()
        
        def _RepInd (self):
            dirName = filedialog.askdirectory(title=u"Merci de choisir le repertoire SOURCE des PDF")
            if dirName:
                self.RepIn['text'] = dirName

        def _RepOutd (self):
            dirName = filedialog.askdirectory(title=u"Merci de choisir le repertoire de SORTIE des PDF")
            if dirName:
                self.RepOut['text'] = dirName
        
        def _MergePdfCCOnClick(self):
            None
        
        def _stampPdfCCOnClick(self):
            None
        
        def log(self, message):
            logging.info(message)
            self.logOutputLabel['text'] = self.logOutputLabel['text'] + message + "\n"

class cli():
    
    def __init__(self, application):
        self.application = application
        
    def merger(self, args):
        # SET mypath=%~dp0
        # cd %mypath:~0,-1%
        # set PYTHONPATH=%cd%\src
        # python .\src\gui\stamperFs.py -M --inDir U:\23-4406\03-PROJET\02-CAO\DELIVRE -i PL001-S532A2321052_S6503-NOTAS-BPF-INDA2.pdf PL002-S532A2321052_S6503-NOMENCLATURE-BPF-INDA2.pdf PL003-S532A2321052_S6503-ENV+OUTILLAGE-BPF-INDA2.pdf -o U:\23-4406\03-PROJET\02-CAO\DELIVRE\merged.pdf

        outpdf = args.outFile
        indir = args.inDir
        infiles = args.inFile
        myMerger = Merger()
        
        #si des fichiers sont specifiées, merge uniquement cela, cherche ces fichiers dans inDir si specifié, sinon file doit etre un chemin complet
        if(len(infiles) > 0):
            if(indir != "" ):
                logging.info("INPUT DIR: " + indir)
            else:
                indir=""
            for f in infiles:
                f = os.path.join(indir, f)
                if(os.path.isfile(f)):
                    logging.info("INPUT FILE: " + f)
                    myMerger.addPdf(f, "ALL")
                else:
                    logging.info("FILE NOT FOUND: " + f)
        elif(indir != "" ):
            logging.info("INPUT DIR: " + indir)
            myMerger.addFromDirectory(indir)

        if myMerger.save(outpdf) == True:
            logging.info("OUTPUT FILE: " + outpdf)
            return True
        else:
            logging.info("OUT FILE IS NOT SAVED")
            return False

    def stamper(self, args):
        
        myStamp.message = args.message
        myStamp.date = args.date
        myStamp.projectNumber = args.project
        myStamp.username = args.user
        myStamp.width = args.tWidth
        myStamp.policeSize = args.pSize
        myStamp.color = args.color  # blue, green, red
        myStamp.backgroundColor = args.bgColor  # beige
        
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
        pdf = myStamper.stampPdf(inpdf, "ALL", [posX, posY])
        pdf.write(outpdf)
        
        logging.info("INPUT DIR: " + inpdf)
        logging.info("OUTPUT DIR: " + outpdf)

#####################################################################
#####################################################################
#####################################################################

if __name__ == '__main__':

    # determine if application is a script file or frozen exe
    if getattr(sys, 'frozen', False):
        srcPath = os.path.dirname((os.path.dirname(sys.executable)))
        dataPath = os.path.join(os.path.dirname(srcPath), "data")
    elif __file__:
        srcPath = os.path.dirname(os.path.dirname(__file__))
        dataPath = os.path.join(os.path.dirname(srcPath), "data")
    
    app = Application()
    app.SRC_PATH = srcPath
    app.DATA_PATH = dataPath
    
    logging.info("SOURCE PATH: " + srcPath)
    logging.info("DATA PATH: " + dataPath)
    
    parser = argparse.ArgumentParser('placards')
    parser.description = 'macro de tamponnage des plans pdf'
    parser.epilog = 'for sier'
    
    myStamp = Stamp()
    parser.add_argument('-M', "--merger", help='MERGER', action="store_true")
    parser.add_argument('-S', "--stamper", help='STAMPER', action="store_true")
    parser.add_argument('-a','--inDir', help='Input Directory', default = "")
    parser.add_argument('-b','--outDir', help='Output Directory', default = tempfile.gettempdir())
    parser.add_argument('-i', "--inFile", help='Input File', nargs='*', default = "")
    parser.add_argument('-o', "--outFile", help='Output File', default = os.path.join(tempfile.gettempdir(), "out.pdf"))
    parser.add_argument('-m', "--message", help='Message', default = myStamp.message)
    parser.add_argument('-d', "--date", help='Date', default = myStamp.date)
    parser.add_argument('-p', "--project", help='Project number', default = myStamp.projectNumber)
    parser.add_argument('-u', "--user", help='Username', default = myStamp.username)
    parser.add_argument('-w', "--tWidth", help='table Width', default = myStamp.width)
    parser.add_argument('-s', "--pSize", help='police Size', default = myStamp.policeSize)
    parser.add_argument('-x', "--posX", help='position X', default =0)
    parser.add_argument('-y', "--posY", help='position Y', default =0)
    parser.add_argument('-c', "--color", help='Color', default = myStamp.color)
    parser.add_argument('-bc', "--bgColor", help='Background Color', default=myStamp.backgroundColor)
    parser.add_argument("-v", "--version", help="Display infos and version", action="store_true")
    
    args = parser.parse_args()
    print(args)
    
    if args.version == 1:
        print("Stamper for pdf SIER, See source code and help: " +  Application.WEB_SITE)
        print("Version: " +  Application.VERSION)
        exit()
    
    if args.merger == 1:
        cli = cli(app)
        cli.merger(args)
    elif args.stamper == 1:
        cli = cli(app)
        cli.stamper(args)
    else:
        gui = stamperGui(app)  # Instanciation de la classe
        gui.mainloop()  # Boucle pour garder le programme en vie
        gui.quit()  # Fermeture propre à la sortie de la boucle
