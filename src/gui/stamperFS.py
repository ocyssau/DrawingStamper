# -*- coding:utf-8 -*-
import os
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from Application.Application import Stamp, Stamper, Merger, Application
from reportlab.lib.units import mm

class stamperGui(Tk):
        """ Mon programme graphique utilisant Python3 et Tkinter """
 
        statusBPF = "BON pour Fabrication"
        statusNPF = "NON VALIDE pour Fabrication"
        statusBPC = "BON pour Consultation"
        statusBPA = "BON pour Approvisionnement"
        
        def __init__(self):
            Tk.__init__(self)  # On dérive de Tk, on reprend sa méthode d'instanciation
            
            self.application = Application()
            
            # Widgets
            
            ##frame 0 : ACTIONS
            self.Frame0 = LabelFrame(self, relief=GROOVE, borderwidth=2, text="Selectionnez les tâches")
            self.Frame0.grid(row=0 , column=0, columnspan=8, sticky=W)

            # case a cocher
            ## stamp CC
            self.stampPdfVal = IntVar()
            self.stampPdfVal.set(1)
            self.stampPdfCC = Checkbutton(self.Frame0,text = "Tamponner les PDFs",command = self._stampPdfCCOnClick, variable = self.stampPdfVal)
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
            statusListe = (self.statusBPF, self.statusNPF, self.statusBPA, self.statusBPC)
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
            posXVal.set('50')
            self.PosXInLabel = Label(self.Frame3, text=u" X (mm)= ")
            self.PosXInLabel.grid(row=4 , column=0, sticky=W)
            self.PosXIn = Entry(self.Frame3, textvariable=posXVal)
            self.PosXIn.grid(row=4 , column=1)
            
            ##position Y
            posYVal = StringVar()
            posYVal.set('30')
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
                myStamp.saveToFile(os.path.join(inpdf, "stamp.pdf"))

            except Exception as e:
                self.log(str(e))
            
            ## STAMP
            try:
                #init the stamper
                myStamper = Stamper(myStamp)
                
                #stamp the pdf
                fileList = Application.getPdfFromDirectory(inpdf)
                for filepath in fileList:
                    outpdf = filepath
                    self.log("Stamp " + outpdf)
                    myStamper.stampPdf(filepath, outpdf, "ALL", position)
            except Exception as e:
                self.log(str(e))
            
            ## MERGE
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
            self.logOutputLabel['text'] = self.logOutputLabel['text'] + message + "\n"
            #self.logOutputLabel['text'] = message

if __name__ == '__main__':
    application = stamperGui()  # Instanciation de la classe
    application.mainloop()  # Boucle pour garder le programme en vie
    application.quit()  # Fermeture propre à la sortie de la boucle
