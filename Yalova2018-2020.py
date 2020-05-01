import matplotlib.pyplot as plt
import pandas as pd
def sinif(kalite):
    if kalite <= 50:
        return "İYİ"
    elif kalite <=100:
        return "ORTA"
    elif kalite <=150:
        return "HASSAS"
    elif kalite <=200:
        return "SAĞLIKSIZ"
    
    elif kalite <=300:
        return "KÖTÜ"
    elif kalite <=500:
        return "TEHLİKELİ"
    else:
        return "-"

isgunu=[]
tatilgunu=[]


hava=pd.read_csv("hava.csv" )
gunler=hava.groupby("Tarih")
gunler=gunler.mean()

gunler=gunler.sort_values(["Tarih"], ascending = True)
y=gunler[["PM10"]].iloc[::-1]
x= range(0,len(gunler))
plt.subplot(221),
plt.plot(x,y,"r"),
plt.ylabel("PM10"),
plt.title("Günlere göre ortalama PM10 değerleri")

y=gunler[["NO2"]].iloc[::-1]
x= range(0,len(gunler))
plt.subplot(222),
plt.plot(x,y,"b"),
plt.ylabel("NO2"),
plt.title("Günlere göre ortalama NO2 değerleri")

y=gunler[["SO2"]].iloc[::-1]
x= range(0,len(gunler))
plt.subplot(223),
plt.plot(x,y,"y"),
plt.xlabel("2018/10/29 - 2020/4/12"),
plt.ylabel("SO2"),
plt.title("Günlere göre ortalama SO2 değerleri")

y=gunler[["O3"]].iloc[::-1]
x= range(0,len(gunler))
plt.subplot(224),
plt.plot(x,y,"g"),
plt.xlabel("2018/10/29 - 2020/4/12"),
plt.ylabel("O3"),
plt.title("Günlere göre ortalama O3 değerleri")
plt.show()
kalite=gunler.max(axis=1).apply(sinif)
secilen=gunler.idxmax(axis=1)


gunler["Secilen"]=secilen
gunler["Kalite"]=kalite

for x in enumerate(gunler.iloc[:,-1]):
   
    if x[0]%7==0 or x[0]%7==6:
        tatilgunu.append(gunler.iloc[x[0],-2]+":"+x[1])
    else:
        isgunu.append(gunler.iloc[x[0],-2]+":"+x[1])


tgunu={"PM10":0,"NO2":0,"SO2":0,"O3":0}
igunu={"PM10":0,"NO2":0,"SO2":0,"O3":0}
for i in isgunu:
    veri=i.split(':')
    if veri[0]=="PM10":
        igunu["PM10"]+=1
    elif veri[0]=="NO2":
        igunu["NO2"]+=1
    elif veri[0]=="SO2":
        igunu["SO2"]+=1
    else:
        igunu["O3"]+=1

                        
for i in tatilgunu:
    veri=i.split(':')
    if veri[0]=="PM10":
        tgunu["PM10"]+=1
    elif veri[0]=="NO2":
        tgunu["NO2"]+=1
    elif veri[0]=="SO2":
        tgunu["SO2"]+=1
    else:
        tgunu["O3"]+=1





#---------------------------------------GiniSol, GiniSağ ve Gini J değerlerinin Hesaplanması-------------------------------------------

GiniSol=GiniSag=Gini_J={"PM10":0,"NO2":0,"SO2":0,"O3":0}

#PM10 için
isGunuSayisi=isgunu.count("PM10:İYİ")
tatilGunuSayisi=tatilgunu.count("PM10:İYİ")
tsol=isGunuSayisi+tatilGunuSayisi
tsag=igunu["PM10"]-isGunuSayisi+tgunu["PM10"]-tatilGunuSayisi
if isGunuSayisi==0 and tatilGunuSayisi==0:
    GiniSol["PM10"]=0
else:
    GiniSol["PM10"]=1-(((isGunuSayisi/tsol)**2)+(tatilGunuSayisi/tsol)**2)


GiniSag["PM10"]=1-((((igunu["PM10"]-isGunuSayisi)/tsag)**2)+((tgunu["PM10"]-tatilGunuSayisi)/tsag)**2)
Gini_J["PM10"]=1/(tsol+tsag)*((tsol*GiniSol["PM10"])+(tsag*GiniSag["PM10"]))


#NO2 için
isGunuSayisi=isgunu.count("NO2:İYİ")
tatilGunuSayisi=tatilgunu.count("NO2:İYİ")
tsol=isGunuSayisi+tatilGunuSayisi
tsag=igunu["NO2"]-isGunuSayisi+tgunu["NO2"]-tatilGunuSayisi
if isGunuSayisi==0 and tatilGunuSayisi==0:
    GiniSol["NO2"]=0
else:
    GiniSol["NO2"]=1-(((isGunuSayisi/tsol)**2)+(tatilGunuSayisi/tsol)**2)


GiniSag["NO2"]=1-((((igunu["NO2"]-isGunuSayisi)/tsag)**2)+((tgunu["NO2"]-tatilGunuSayisi)/tsag)**2)
Gini_J["NO2"]=1/(tsol+tsag)*((tsol*GiniSol["NO2"])+(tsag*GiniSag["NO2"]))

          
#SO2 için
isGunuSayisi=isgunu.count("SO2:İYİ")
tatilGunuSayisi=tatilgunu.count("SO2:İYİ")
tsol=isGunuSayisi+tatilGunuSayisi
tsag=igunu["SO2"]-isGunuSayisi+tgunu["SO2"]-tatilGunuSayisi
if isGunuSayisi==0 and tatilGunuSayisi==0:
    GiniSol["SO2"]=0
else:
    GiniSol["SO2"]=1-(((isGunuSayisi/tsol)**2)+(tatilGunuSayisi/tsol)**2)


GiniSag["SO2"]=1-((((igunu["SO2"]-isGunuSayisi)/tsag)**2)+((tgunu["SO2"]-tatilGunuSayisi)/tsag)**2)
Gini_J["SO2"]=1/(tsol+tsag)*((tsol*GiniSol["SO2"])+(tsag*GiniSag["SO2"]))


          
#O3 için
isGunuSayisi=isgunu.count("O3:İYİ")
tatilGunuSayisi=tatilgunu.count("O3:İYİ")

tsol=isGunuSayisi+tatilGunuSayisi
tsag=igunu["O3"]-isGunuSayisi+tgunu["O3"]-tatilGunuSayisi
if isGunuSayisi==0 and tatilGunuSayisi==0:
    GiniSol["O3"]=0
else:
    GiniSol["O3"]=1-(((isGunuSayisi/tsol)**2)+(tatilGunuSayisi/tsol)**2)


GiniSag["O3"]=1-((((igunu["O3"]-isGunuSayisi)/tsag)**2)+((tgunu["O3"]-tatilGunuSayisi)/tsag)**2)
Gini_J["O3"]=1/(tsol+tsag)*((tsol*GiniSol["O3"])+(tsag*GiniSag["O3"]))
#----------------------------------------------------------------------------------



print("İş Günleri")
print(isgunu)
print("\nTatil Günleri")
print(tatilgunu)
print("\nGini j:")
print(Gini_J)

















