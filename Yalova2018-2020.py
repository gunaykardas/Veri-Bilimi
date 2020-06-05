from PyQt5.QtWidgets import*
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.uic import loadUi
from matplotlib.backends.backend_qt5agg import (NavigationToolbar2QT as NavigationToolbar)
import numpy as np
import pandas as pd
import random
from sklearn.preprocessing import LabelEncoder
import sys
from datetime import date
import os
from sklearn.model_selection import train_test_split
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense

class Window(QtWidgets.QMainWindow):
    resized = QtCore.pyqtSignal()
    def  __init__(self, parent=None):
        super(Window, self).__init__(parent=parent)
        ui = Ui_MainWindow()
        ui.setupUi(self)
        self.resized.connect(self.islem)
        loadUi("form.ui",self)
        self.setWindowTitle("Veri Bilimi")
        self.widget1.setVisible(False)
        self.widget2.setVisible(False)
        self.widget3.setVisible(False)
        self.widget4.setVisible(False)
        self.kaydet()
        self.btnsonuc.clicked.connect(self.cizim)
        self.btnkaydet.clicked.connect(self.kaydet)
        self.btnmax.clicked.connect(lambda:self.maxmin("max"))
        self.btnmin.clicked.connect(lambda:self.maxmin("min"))
        self.btnolusturegit.clicked.connect(self.modelolustur)
        self.tarihbaslangic.dateChanged.connect(self.baslangicTarih)
        #self.addToolBar(NavigationToolbar(self.widget1.canvas, self)) 

    def resizeEvent(self, event):
        self.resized.emit()
        return super(Window, self).resizeEvent(event)

    def islem(self):
        self.yenidenboyutlandir()

    def sinif(self,kalite):
        if kalite <= 100:
            return 1 #"İYİ"
        elif kalite >100:
            return 2 #"ORTA"
        """
        elif kalite <=150:
            return 3 #"HASSAS"
        elif kalite <=200:
            return 4 #"SAĞLIKSIZ"
        
        elif kalite <=300:
            return 5 #"KÖTÜ"
        elif kalite <=500:
            return 6 #"TEHLİKELİ"
        else:
            return 0 #"-"
        """
     
    def cizim1(self):
        h=self.h.sort_values(["Tarih"], ascending = True)
        y=h[["PM10"]].iloc[self.gunBaslangic:self.gunBaslangic+self.gunfarki+1]
        x= range(0,len(y))
        self.widget1.canvas.axes.plot(x,y,"r")   
        self.widget1.canvas.axes.set_title('PM10 değerleri')
        self.widget1.canvas.draw()
        
    def cizim2(self):
        h=self.h.sort_values(["Tarih"], ascending = True)
        y=h[["NO2"]].iloc[self.gunBaslangic:self.gunBaslangic+self.gunfarki+1]
        x= range(0,len(y))
        self.widget2.canvas.axes.plot(x,y,"b")   
        self.widget2.canvas.axes.set_title('NO2 değerleri')
        self.widget2.canvas.draw()
        
    def cizim3(self):
        h=self.h.sort_values(["Tarih"], ascending = True)
        y=h[["SO2"]].iloc[self.gunBaslangic:self.gunBaslangic+self.gunfarki+1]
        x= range(0,len(y))
        self.widget3.canvas.axes.plot(x,y,"y")   
        self.widget3.canvas.axes.set_title('SO2 değerleri')
        self.widget3.canvas.draw()
        
    def cizim4(self):
        h=self.h.sort_values(["Tarih"], ascending = True)
        y=h[["O3"]].iloc[self.gunBaslangic:self.gunBaslangic+self.gunfarki+1]
        x= range(0,len(y))
        self.widget4.canvas.axes.plot(x,y,"g")   
        self.widget4.canvas.axes.set_title('O3 değerleri')
        self.widget4.canvas.draw()
        
    def yenidenboyutlandir(self):
        self.widget1.move(20,100)
        self.widget2.move((self.frameGeometry().width()/2)+20,100)
        self.widget3.move(20,(self.frameGeometry().height()/2)+40)
        self.widget4.move((self.frameGeometry().width()/2)+20,(self.frameGeometry().height()/2)+40)
        self.widget1.resize((self.frameGeometry().width()/2)-20,(self.frameGeometry().height()/2)-100)
        self.widget2.resize((self.frameGeometry().width()/2)-20,(self.frameGeometry().height()/2)-100)
        self.widget3.resize((self.frameGeometry().width()/2)-20,(self.frameGeometry().height()/2)-100)
        self.widget4.resize((self.frameGeometry().width()/2)-20,(self.frameGeometry().height()/2)-100)
        sayi=self.sayi
        if self.pm10durum:
            if sayi==1:
                self.widget1.resize(self.frameGeometry().width()-20,self.frameGeometry().height()-100)
            elif sayi==2:
                self.widget1.resize((self.frameGeometry().width()/2)-20,self.frameGeometry().height()-100)
        if self.no2durum:
             if sayi==1:
                 self.widget2.move(20,100) 
                 self.widget2.resize(self.frameGeometry().width()-20,self.frameGeometry().height()-100)
             elif sayi==2:
                if self.pm10durum==False:
                    self.widget2.move(20,100)
                self.widget2.resize((self.frameGeometry().width()/2)-20,self.frameGeometry().height()-100)
        if self.so2durum:
             if sayi==1:
                 self.widget3.move(20,100) 
                 self.widget3.resize(self.frameGeometry().width()-20,self.frameGeometry().height()-100)
             elif sayi==2:
                 if self.o3durum:
                     self.widget3.move(20,100)
                 else:
                     self.widget3.move((self.frameGeometry().width()/2)+20,100)
                 self.widget3.resize((self.frameGeometry().width()/2)-20,self.frameGeometry().height()-100)
        if self.o3durum:
             if sayi==1:
                 self.widget4.move(20,100) 
                 self.widget4.resize(self.frameGeometry().width()-20,self.frameGeometry().height()-100)
             elif sayi==2:
                 self.widget4.move(self.frameGeometry().width()/2+20,100) 
                 self.widget4.resize((self.frameGeometry().width()/2)-20,self.frameGeometry().height()-100)

    def cizim(self):
         d0 = date( self.tarihbaslangic.date().year(),  self.tarihbaslangic.date().month(), self.tarihbaslangic.date().day())
         d1 = date( self.tarihbitis.date().year(),  self.tarihbitis.date().month(), self.tarihbitis.date().day())
         self.gunfarki=(d1-d0).days
         self.gunBaslangic=(d0-date(self.ilkYil, self.ilkAy, self.ilkGun)).days
         self.pm10durum=False
         self.no2durum=False
         self.so2durum=False
         self.o3durum=False
         self.widget1.canvas.axes.clear()
         self.widget2.canvas.axes.clear()
         self.widget3.canvas.axes.clear()
         self.widget4.canvas.axes.clear()
         self.widget1.setVisible(False)
         self.widget2.setVisible(False)
         self.widget3.setVisible(False)
         self.widget4.setVisible(False)
         self.sayi=0
         if self.pm10.isChecked():
             self.pm10durum=True
             self.widget1.setVisible(True)
             self.sayi+=1
             self.cizim1()
         if self.no2.isChecked():
             self.no2durum=True
             self.widget2.setVisible(True)
             self.sayi+=1
             self.cizim2()
         if self.so2.isChecked():
             self.so2durum=True
             self.widget3.setVisible(True)
             self.sayi+=1
             self.cizim3()
         if self.o3.isChecked():
             self.o3durum=True
             self.widget4.setVisible(True)
             self.sayi+=1
             self.cizim4()
         self.yenidenboyutlandir()
         
    def baslangicTarih(self,tarih):
        self.tarihbitis.setMinimumDate(tarih.addDays(1))
        
    def kaydet(self):
        self.lblcsv.setText(" "+self.csvyol.text())
        self.h=pd.read_csv(self.csvyol.text())
        self.hava=self.h.bfill().ffill()
        #self.hava.to_csv('/hava2.csv', index=False)
        self.sayi=0
        self.pm10durum=False
        self.no2durum=False
        self.so2durum=False
        self.o3durum=False
        self.gunfarki=0
        self.h=self.hava
        self.gunBaslangic=0
        ilkTarih=str(self.hava.sort_values(["Tarih"], ascending = True)["Tarih"].iloc[0:1].values).replace('[','').replace(']','').replace("'",'')
        self.ilkYil=int(ilkTarih.split("/")[0])
        self.ilkAy=int(ilkTarih.split("/")[1])
        self.ilkGun=int(ilkTarih.split("/")[2])
        sonTarih=str(self.hava.sort_values(["Tarih"], ascending = False)["Tarih"].iloc[0:1].values).replace('[','').replace(']','').replace("'",'')
        self.sonYil=int(sonTarih.split("/")[0])
        self.sonAy=int(sonTarih.split("/")[1])
        self.sonGun=int(sonTarih.split("/")[2])
        self.ilksonayarla()
        
    def maxmin(self,deger):
        if(deger=="max"):
            self.tarihbitis.setDateTime(QtCore.QDateTime.currentDateTime())
        else:
            self.tarihbaslangic.setDateTime(QtCore.QDateTime.currentDateTime().addYears(-1000))
            
    def ilksonayarla(self):
        self.tarihbitis.setMaximumDate(QtCore.QDate(self.sonYil, self.sonAy, self.sonGun))
        self.tarihbaslangic.setMaximumDate((QtCore.QDate(self.sonYil, self.sonAy, self.sonGun)).addDays(-1))
        self.tarihbaslangic.setMinimumDate(QtCore.QDate(self.ilkYil, self.ilkAy, self.ilkGun))
        self.maxmin("max")
        self.maxmin("min")

    def modelolustur(self):
        
        self.controlpanel.setVisible(False)
        self.bekle.setVisible(True)
       
        yazi="Lütfen Bekleyin"
        self.bekle.setText(yazi)
        
        gunler=self.h.sort_values(["Tarih"], ascending = True)
        kalite=gunler.max(axis=1).apply(self.sinif)
        secilen=gunler.drop(["Tarih"],axis=1).idxmax(axis=1)
        
        gunler["Secilen"]=secilen
        gunler["Kalite"]=kalite
        veri=[]
        sayi=0
        
        for x in enumerate(gunler.iloc[:,-1]):
         
          haftasonumu= x[0]%7==0 or x[0]%7==6
          
          if kalite[sayi]!=1 and haftasonumu==False:
            artis=1
          elif kalite[sayi]==1 and haftasonumu==False:
            artis=2
          elif kalite[sayi]!=1 and haftasonumu==True: 
            artis=3
          elif kalite[sayi]==1 and haftasonumu==True:
            artis=4

         
          sayi+=1
          veri.append(artis)
        gunler["Durum"]=veri
           
        veri=gunler.drop(['Secilen'],axis=1)
       
        
        
        #sınıf sayısının belirlenmesi
        label_encoder=LabelEncoder().fit(veri.Durum)
        labels=label_encoder.transform(veri.Durum)
        classes=list(label_encoder.classes_)

        
        #girdi ve çıktı verilerinin hazırlanması
        X=veri.drop(["Durum","Tarih"],axis=1)
        y=labels
        self.bekle.setText(yazi)
       
       
        #eğitim ve doğrulama verilerinin hazırlanması
        
        
        X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.2)#test yüzdesi %20
        
        
        #çıktı değerlerinin kategorileştirilmesi
        
        
       
        y_train=to_categorical(y_train)
        y_test=to_categorical(y_test)
        
        
        #modelin oluşturulması

        model=Sequential()
        model.add(Dense(4,input_dim=5,activation="relu"))
        model.add(Dense(4,activation="relu"))
        model.add(Dense(4,activation="softmax"))
        model.summary()
        
        #modelin derlenmesi
        model.compile(loss="categorical_crossentropy",optimizer="Adam",metrics=["accuracy"])
        
        
        #modelin eğitilmesi
        model.fit(X_train,y_train,validation_data=(X_test,y_test),epochs = int(self.epoksayisi.text()))
        
        yazi="\nortalama eğitim başarımı: "+str(np.mean(model.history.history["accuracy"]))+"\nortalama doğrulama başarımı: "+str(np.mean(model.history.history["val_accuracy"]))
        self.bekle.setText(yazi)
       
        
        
        """
        plt.plot(model.history.history["accuracy"])
        plt.plot(model.history.history["val_accuracy"])
        plt.title("Model Başarımları")
        plt.ylabel("Başarım")
        plt.xlabel("Epok sayısı")
        plt.legend(["Eğitim","Test"],loc="upper left")
        plt.show()"""
        self.controlpanel.setVisible(True)
        #self.bekle.setVisible(False)
        
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("Veri Bilimi")
        MainWindow.setWindowTitle("Veri Bilimi")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        MainWindow.setCentralWidget(self.centralwidget)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        
app = QtWidgets.QApplication(sys.argv)
window = Window()
window.show()
app.exec_()
