# -*- coding:utf-8 -*-
import os
from Tkinter            import *        
import ttk
import tkFileDialog
import Watermark_0_09 as Wt


class MonProgramme(Tk):
        """ Mon programme graphique utilisant Python3 et Tkinter """
 
        def __init__(self):
                Tk.__init__(self)  # On dérive de Tk, on reprend sa méthode d'instanciation
                # Définition des variables
                self.RepIn_value = StringVar()
                self.RepIn_value.set(os.getcwd())
                
                self.RepOut_value = StringVar()
                self.RepOut_value.set(u"C:\TEMP")
                
                self.liste = ('BON pour Fabrication', 'APPROVED for Production', 'NON VALIDE pour Fabrication', 'NOT VALID for Production')
                self.Txt_value = StringVar()
                self.x_value = StringVar()
                self.x_value.set('5')
                self.y_value = StringVar()
                self.y_value.set('3')
                self.StatusValue = StringVar()
                self.StatusValue.set("Status :")
 
                # Widgets
                self.title("Sier - BonPourFab")
                self.geometry('800x400+100+100')
                self.Frame1 = LabelFrame(self, relief=GROOVE, borderwidth=2, text="PDF : Choix des répertoires", padx=5, pady=5)
                self.Frame1.grid(row=0 , column=0, columnspan=2)
                
                self.RepInBTxt = Label(self.Frame1, justify='left', text=u" Répertoire Source :")
                self.RepInBTxt.grid(row=0 , column=0)
                self.RepInB = Button(self.Frame1, text=u" Select " , command=self._RepInd)
                self.RepInB.grid(row=1 , column=1)
                self.RepIn = Label(self.Frame1, textvariable=self.RepIn_value, justify='left', relief=SUNKEN)
                self.RepIn.grid(row=1 , column=0)

                self.RepOutBTxt = Label(self.Frame1, text=u" Répertoire Destination :", justify='left')
                self.RepOutBTxt.grid(row=2 , column=0)
                self.RepOutB = Button(self.Frame1, text=u" Select ", command=self._RepOutd)
                self.RepOutB.grid(row=3 , column=1)
                self.RepOut = Label(self.Frame1, textvariable=self.RepOut_value, justify='left', relief=SUNKEN)
                self.RepOut.grid(row=3 , column=0)

                # TAMPON
                self.Frame2 = LabelFrame(self, relief=GROOVE, borderwidth=2, text="TAMPON", padx=5, pady=5)
                self.Frame2.grid(row=1 , column=0, columnspan=2)
                self.Txt = Label(self.Frame2, text=u" Texte du tampon :")
                self.Txt.grid(row=0 , column=0, sticky=W, columnspan=2)
           
                self.listeTxt = ttk.Combobox(self.Frame2, textvariable=self.Txt_value, \
                                                values=self.liste)  # , state = 'readonly')
                self.listeTxt.set(self.liste[0])
                self.listeTxt.grid(row=1 , column=0, sticky=W, columnspan=4)
                self.label3 = Label(self.Frame2, text=u" Position du tampon (Ref : Bas-Gauche de la page):")
                self.label3.grid(row=2 , column=0)
                self.labelx = Label(self.Frame2, text=u" X (cm)= ")
                self.labelx.grid(row=3 , column=0, sticky=W)
                self.Entryx = Entry(self.Frame2, textvariable=self.x_value)
                self.Entryx.grid(row=3 , column=1)
                self.labely = Label(self.Frame2, text=u" Y (cm)= ")
                self.labely.grid(row=3 , column=2, sticky=W)
                self.Entryy = Entry(self.Frame2, textvariable=self.y_value)
                self.Entryy.grid(row=3 , column=3)

                self.OKB = Button(self, text=u" OK ", command=self._validate)
                self.OKB.grid(row=2 , column=0)

                self.ExitB = Button(self, text=u" Cancel ", command=self._cancel)
                self.ExitB.grid(row=2 , column=1)
                self.Status = Label(self, textvariable=self.StatusValue)
                self.Status.grid(row=3 , column=0, sticky="W")

        def _validate(self):
               # print self.RepIn_value.get(),self.RepOut_value.get(),self.Txt_value.get(),self.x_value.get(),self.y_value.get()
                self.StatusValue.set("Status : En cours,....")
                Wat = Wt.WaterRep(self.RepIn_value.get(), self.RepOut_value.get(), self.Txt_value.get(), float(self.x_value.get()), float(self.y_value.get()), self.StatusValue)
                if Wat.status == 0:
                      self.destroy()  

        def _cancel(self):
                self.destroy()

        def _RepInd (self):
                dirName = tkFileDialog.askdirectory(title=u"Merci de choisir le repertoire SOURCE des PDF")
                if dirName:
                    # self.RepIn.config(  text=dirName)
                     self.RepIn_value.set(dirName)

        def _RepOutd (self):
                dirName = tkFileDialog.askdirectory(title=u"Merci de choisir le repertoire de SORTIE des PDF")
                if dirName:
                    # self.RepOut.config(  text=dirName)
                     self.RepOut_value.set(dirName)

if __name__ == '__main__':
    application = MonProgramme()  # Instanciation de la classe
    application.mainloop()  # Boucle pour garder le programme en vie
    application.quit()  # Fermeture propre à la sortie de la boucle
